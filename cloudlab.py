import ryu.app.ofctl.api as api
from ryu.base import app_manager
from ryu.ofproto.ofproto_v1_2 import OFPG_ANY
from itertools import cycle

from config_reader import Reader


class Cloudlab(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(Cloudlab, self).__init__(*args, **kwargs)
        self.__ips = {'10.11.10.1': '130.127.133.237',
                      '10.11.10.2': '130.127.134.16',
                      '10.11.10.3': '130.127.133.236',
                      '10.11.10.4': '130.127.134.4'}
        self.__macs = {'3c:fd:fe:55:ff:42': '3c:fd:fe:55:ff:40',
                       '3c:fd:fe:55:f4:62': '3c:fd:fe:55:f4:60',
                       '3c:fd:fe:55:fd:c2': '3c:fd:fe:55:f4:60',
                       '3c:fd:fe:55:fe:62': '3c:fd:fe:55:fe:60'}
        self._parser = None
        self._datapath = None
        # read config file
        self.config = Reader()
        self._old_port = self.config.old_port()
        self._new_port = self.config.new_port()
        self._local = 'LOCAL'
        self._portIterator = cycle([self._old_port, self._new_port])

        # get old, so for next request start from new
        self._get_new_port()

    def change_interface(self, datapath, old_port, old_flows):
        self._datapath = datapath
        self._parser = datapath.ofproto_parser
        new_out_port = self._get_new_port(old_port)

        print('Moving from {} to {}'.format(old_port, new_out_port))

        actions = [self._parser.OFPActionOutput(new_out_port)]

        for rule in sorted([flow for flow in old_flows if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            if rule.instructions[0].actions[0].port == old_port:
                match = self._parser.OFPMatch(in_port=rule.match['in_port'],
                                              eth_dst=rule.match['eth_dst'],
                                              eth_src=rule.match['eth_src'])
                self._add_flow(3, match, actions)
                self._remove_flows(match, old_port)
            elif rule.match['in_port'] == old_port:
                old_actions = rule.instructions[0].actions
                old_match = self._parser.OFPMatch(in_port=rule.match['in_port'],
                                                  eth_dst=rule.match['eth_dst'],
                                                  eth_src=rule.match['eth_src'])
                new_match = self._parser.OFPMatch(in_port=new_out_port,
                                                  eth_dst=rule.match['eth_dst'],
                                                  eth_src=rule.match['eth_src'])
                self._add_flow(3, new_match, old_actions)
                self._remove_flows(old_match)

    def _get_new_port(self, old_port):
        # Prime the pump
        notFound = True

        nextelem = next(self._portIterator)
        while notFound:
            thiselem, nextelem = nextelem, next(self._portIterator)
            if thiselem == old_port:
                return nextelem

    def _add_flow(self, priority, match, actions, buffer_id=None):
        ofproto = self._datapath.ofproto

        inst = [self._parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        if buffer_id:
            mod = self._parser.OFPFlowMod(datapath=self._datapath, buffer_id=buffer_id,
                                          priority=priority, match=match,
                                          instructions=inst)
        else:
            mod = self._parser.OFPFlowMod(datapath=self._datapath, priority=priority,
                                          match=match, instructions=inst)
        self._datapath.send_msg(mod)

    def _remove_flows(self, match, out_port=None):
        """Create OFP flow mod message to remove flows from table."""
        ofproto = self._datapath.ofproto
        # Delete the flow
        if out_port:
            flow_mod = self._datapath.ofproto_parser.OFPFlowMod(datapath=self._datapath, command=ofproto.OFPFC_DELETE,
                                                                out_port=out_port, out_group=ofproto.OFPG_ANY,
                                                                match=match)
        else:
            flow_mod = self._datapath.ofproto_parser.OFPFlowMod(datapath=self._datapath, command=ofproto.OFPFC_DELETE,
                                                                out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
                                                                match=match)

        self._datapath.send_msg(flow_mod)
