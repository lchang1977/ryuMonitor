from operator import attrgetter
from arch import arch_model

import matplotlib
matplotlib.use('Agg')

from ryu.app import simple_switch_13
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

from arima import Arima
from setup import OVS_lan_type
from prediction import Model
from cloudlab import Cloudlab

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import datetime
import csv
import configparser


class SimpleMonitor13(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        # limit for bandwidth, if over react
        self.threshold = 2000.00
        self.max_training_size = 150
        # perform a prediction every X packets(measures)
        self.freq_prediction = 20
        # forecast horizon
        self.forecast_size = 15
        self.num_measure = 0
        self.interested_port = [1]
        self.filename = 'bandwidth'
        self.last_flows = None
        # perform request to switch every X second
        self.time_interval = 1
        self.bws = {}
        self.datapaths = {}
        self.prev = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.switch_type = OVS_lan_type()
        # initialize switch flows, change if different network topology
        self.initialize_br_flat()
        # read config file
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def initialize_br_flat(self):

        for dp in self.datapaths.values():
            self.switch_type.initialize(dp)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
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
            if key not in self.prev :
                self.logger.info('First packet')
                self.bws[key] = pd.DataFrame(data=[], columns=['BW'])
                self.prev[key] = {}
                self.prev[key]['prev_rx'] = rx_bytes
                self.prev[key]['prev_tx'] = tx_bytes
            # else calculate bandwidth
            else:
                rx_bw = (rx_bytes - self.prev[key]['prev_rx']) / self.time_interval
                tx_bw = (tx_bytes - self.prev[key]['prev_tx']) / self.time_interval
                self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d %.2f %.2f',
                                 datapath_id, stat.port_no,
                                 stat.rx_packets, rx_bytes, stat.rx_errors,
                                 stat.tx_packets, tx_bytes, stat.tx_errors,
                                 rx_bw, tx_bw)
                self.prev[key]['prev_rx'] = rx_bytes
                self.prev[key]['prev_tx'] = tx_bytes

                if stat.port_no in self.interested_port:
                    self.__add_item(rx_bw, datapath_id, stat.port_no, ev.msg.datapath)

    def _predict_var_gar(self, values):

        garch11 = arch_model(values, p=1, q=1)
        results = garch11.fit(update_freq=10)

        print(results.summary())

        forecasts = results.forecast(horizon=30, method='simulation')
        sims = forecasts.simulations

        lines = plt.plot(sims.values[-1, ::30].T, alpha=0.33)
        lines[0].set_label('Simulated paths')
        plt.plot()

        print('Percentile')
        print(np.percentile(sims.values[-1, 30].T, 5))
        plt.hist(sims.values[-1, 30], bins=50)
        plt.title('Distribution of Returns')

        plt.show()

    def _predict_arima(self, values):

        arima = Model(values, self.config['DEFAULT']['compareAIC'])
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
        first_ts = prediction.index[1]

        # save on file the predicted values
        prediction.to_csv('prediction-{}-{}-{}.csv'.format(first_ts, datapath.id, port), sep=',')

    def _predict(self, datapath, port):
        # read file for next method
        if self.config['DEFAULT']['react']:
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

        # increment number updates and check if time to perform prediction
        self.num_measure += 1
        if self.num_measure == self.freq_prediction:
            self.num_measure = 0

            # create a new thread for ARIMA prediction
            self.prediction_thread = hub.spawn(self._predict, datapath, port)



