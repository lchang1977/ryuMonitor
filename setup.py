from ryu.base import app_manager
from ryu.ofproto.ofproto_v1_2 import OFPG_ANY

from config_reader import Reader


class OVS_lan_type(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(OVS_lan_type, self).__init__(*args, **kwargs)
        # read config file
        self.config = Reader()
        self._old_port = self.config.old_port()
        self._local = 'LOCAL'

    def initialize(self, datapath):
        parser = datapath.ofproto_parser

        # from physical port to local
        actions = [parser.OFPActionOutput(self._local)]
        match = parser.OFPMatch(in_port=self._old_port)
        self.add_flow(datapath, 3, match, actions)

        # from LOCAL to physical port
        actions = [parser.OFPActionOutput(self._old_port)]
        match = parser.OFPMatch(in_port=self._local)
        self.add_flow(datapath, 3, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
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

