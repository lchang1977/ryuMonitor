import ryu.app.ofctl.api as api
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import MAIN_DISPATCHER


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
        self.old_port = None
        self._parser = None
        self._datapath = None

    def change_interface(self, datapath, old_port):
        self._datapath = datapath
        self.old_port = old_port
        self._parser = datapath.ofproto_parser
        req = self._parser.OFPFlowStatsRequest(datapath)
        result = api.send_msg(
            self, req,
            reply_cls=self._parser.OFPFlowStatsReply,
            reply_multi=True)
        #datapath.send_msg(req)
        print('Sent request')
        print(result)
        
    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):

        body = ev.msg.body
        print('Handler')
        actions = [self._parser.OFPActionOutput(self.new_out_port)]

        for flow in body:
            if flow.action == self._parser.OFPActionOutput(1):
                match = self._parser.OFPMatch(in_port=flow.in_port, eth_dst=flow.dst, eth_src=flow.src)
                self._add_flow(self._datapath, 2, match, actions)

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
