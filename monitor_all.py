from operator import attrgetter
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

from algorithms.history_based.sarima_fixed import SarimaBest
from cloudlab import Cloudlab
from config_reader import Reader
from mininet_edge import Configuration

import pandas as pd
import datetime
import matplotlib
matplotlib.use('Agg')


class SimpleMonitor13(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        # limit for bandwidth, if over react
        self.threshold = 2000.00
        self.max_training_size = 200
        # perform a prediction every X packets(measures)
        self.freq_prediction = 18
        # forecast horizon
        self.forecast_size = 15
        self.num_measure = 0
        self.interested_port = [1]
        self.filename = 'bandwidth'
        self.last_flows = None
        self.last_timestamp = {}
        # perform request to switch every X second
        self.time_interval = 1
        self.bws = {}
        self.datapaths = {}
        self.prev = {}
        self.monitor_thread = hub.spawn(self._monitor)
        # change if different network topology
        # self.setup = OVS_lan_type()
        self.setup = Configuration()
        # read config file
        self.config = Reader()

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
                # initialize datapath with default flows
                # self.setup.initialize(datapath)
                self.setup.config_switch(datapath)

        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(self.time_interval)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        self.last_flows = body

        self.logger.info('datapath         '
                         'in-port  eth-dst           '
                         'out-port packets  bytes')
        self.logger.info('---------------- '
                         '-------- ----------------- '
                         '-------- -------- --------')
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            self.logger.info('%016x %8x %17s %8x %8d %8d',
                             ev.msg.datapath.id,
                             stat.match['in_port'], stat.match['eth_dst'],
                             stat.instructions[0].actions[0].port,
                             stat.packet_count, stat.byte_count)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        datapath_id = ev.msg.datapath.id

        self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error '
                         'rx-bndwth[B/s]    tx-bndwth[B/s]')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- -------- '
                         '--------------    -------------')
        for stat in sorted(body, key=attrgetter('port_no')):
            rx_bytes = stat.rx_bytes
            tx_bytes = stat.tx_bytes
            key = (datapath_id, stat.port_no)

            # check if first packet
            if key not in self.prev:
                self.logger.info('First packet')
                self.bws[key] = pd.DataFrame(data=[], columns=['BW'])
                self.last_timestamp[key] = datetime.datetime.now()
                self.prev[key] = {}
                self.prev[key]['prev_rx'] = rx_bytes
                self.prev[key]['prev_tx'] = tx_bytes
            # else calculate bandwidth
            else:
                current = datetime.datetime.now()
                dt = current - self.last_timestamp[key]
                s = ((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0) / 1000.0
                print('Elapsed : {} s'.format(s))
                rx_bw = (rx_bytes - self.prev[key]['prev_rx']) / s
                tx_bw = (tx_bytes - self.prev[key]['prev_tx']) / s
                self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d %.2f %.2f',
                                 datapath_id, stat.port_no,
                                 stat.rx_packets, rx_bytes, stat.rx_errors,
                                 stat.tx_packets, tx_bytes, stat.tx_errors,
                                 rx_bw, tx_bw)
                self.prev[key]['prev_rx'] = rx_bytes
                self.prev[key]['prev_tx'] = tx_bytes
                self.last_timestamp[key] = current

                if stat.port_no in self.interested_port:
                    self.__add_item(rx_bw, datapath_id, stat.port_no, ev.msg.datapath)

    def _predict_arima(self, values):
        arima = SarimaBest(values, self.config)
        # comment out here for choosing best params
        # arima = Sarima(values, self.config.save_aic())
        arima.fit()
        return arima.predict(self.forecast_size, self.time_interval)

    def check_maximum(self, prediction, datapath, port):
        if max(prediction) > self.threshold:
            print('Excessive load in the future')
            cl = Cloudlab()
            cl.change_interface(datapath, port, self.last_flows)

    def _predict_and_react(self, datapath, port):
        key = (datapath.id, port)
        prediction = self._predict_arima(self.bws[key])

        # use the predicted values for changing routing
        self.check_maximum(prediction, datapath, port)

    def _predict_and_save(self, datapath, port):
        key = (datapath.id, port)
        prediction = self._predict_arima(self.bws[key])
        first_ts = prediction.index[0]

        # save on file the predicted values
        prediction.to_csv('prediction-{}-{}-{}.csv'.format(first_ts, datapath.id, port), sep=',')

        # save on file the predicted values for logging purpose
        prediction.to_csv('prediction-{}-{}.csv'.format(datapath.id, port), mode='a', header=False, sep=',')

    def _save_history(self, data, switch_id, port):
        data.to_csv('{}-{}-{}.csv'.format('history', switch_id, port),
                                  mode='a', header=False, sep=',')

    def _predict(self, datapath, port):
        # read file for next method
        if self.config.react():
            self._predict_and_react(datapath, port)
        else:
            self._predict_and_save(datapath, port)

    def __add_item(self, item, switch_id, port, datapath):
        key = (switch_id, port)
        self.bws[key] = self.bws[key].append(
            pd.DataFrame(data=[item], index=[datetime.datetime.now()], columns=['BW'])
        )

        if len(self.bws[key]) == self.max_training_size + 1:
            self.bws[key] = self.bws[key].iloc[1:]
            # write on csv file all the elements
            self.bws[key].to_csv('{}-{}-{}.csv'.format(self.filename, switch_id, port), sep=',')
        else:
            self.bws[key][-1:].to_csv('{}-{}-{}.csv'.format(self.filename, switch_id, port),
                                      mode='a', header=False, sep=',')

        # save value for logging
        self._save_history(self.bws[key][-1:], switch_id, port)

        if not self.config.log_only():
            # increment number updates and check if time to perform prediction
            self.num_measure += 1
            if self.num_measure == self.freq_prediction:
                self.num_measure = 0

                # create a new thread for ARIMA prediction
                self.prediction_thread = hub.spawn(self._predict, datapath, port)
                '''print('Starting new thread')
                thread = Thread(target=self._predict, args=(datapath, port))
                thread.start()'''



