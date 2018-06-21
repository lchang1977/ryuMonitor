import ryu.app.ofctl.api as api
from ryu.base import app_manager
from ryu.ofproto.ofproto_v1_2 import OFPG_ANY


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
        # In this case we are using a new physical port
        self.new_out_port = 'enp6s0f1'
        self.new_out_port = 3
        self._parser = None
        self._datapath = None

    def change_interface(self, datapath, old_port, old_flows):
        self._datapath = datapath
        self._parser = datapath.ofproto_parser

        actions = [self._parser.OFPActionOutput(self.new_out_port)]

        for rule in sorted([flow for flow in old_flows if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            if rule.instructions[0].actions[0].port == old_port:
                match = self._parser.OFPMatch(in_port=rule.match['in_port'],
                                              eth_dst=rule.match['eth_dst'],
                                              eth_src=rule.match['eth_src'])
                self._add_flow(self._datapath, 3, match, actions)
                self._remove_flows(self._datapath, match, old_port)

    def _add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    def remove_previous(self, ofproto, parser):

        match = parser.OFPMatch(in_port=1, eth_src="aa:aa:aa:aa:aa:aa", eth_dst="bb:bb:bb:bb:bb:bb")
        actions = [parser.OFPActionOutput(2)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

    def _remove_flows(self, datapath, match, out_port):
        """Create OFP flow mod message to remove flows from table."""
        ofproto = datapath.ofproto
        # Delete the flow
        flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath=dp, command=ofproto.OFPFC_DELETE,
                                out_port=out_port, out_group=ofproto.OFPG_ANY,
                                match=match)

        return flow_mod
