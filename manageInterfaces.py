# This class is used for changing routing on the switch,
# in particular it  moves all the traffic of ona flow (L2/L3)
# to a different port. The choice of the new port, is outside this scope

from config_reader import Reader


class Interfaces:

    def __init__(self, *args, **kwargs):
        # read config file
        self.config = Reader()

    @staticmethod
    def change_interface_l2(datapath, old_port, eth_src, eth_dst, new_port):
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(eth_dst=eth_dst, eth_src=eth_src)

        print('Moving from {} to {} the flow {}'.format(old_port, new_port, match))

        actions = [parser.OFPActionOutput(new_port)]

        Interfaces._add_flow(datapath, 4, match, actions)
        # in the future remove this
        match = parser.OFPMatch(eth_dst=eth_dst, eth_src=eth_src, out_port=old_port)
        Interfaces._remove_flows(datapath, match, old_port)

    @staticmethod
    def change_interface_l3(datapath, old_port, ip_src, ip_dst, new_port):
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(ip_dst=ip_dst, ip_src=ip_src)

        print('Moving from {} to {} the flow {}'.format(old_port, new_port, match))

        actions = [parser.OFPActionOutput(new_port)]

        Interfaces._add_flow(datapath, 4, match, actions)
        # in the future remove this
        match = parser.OFPMatch(ip_dst=ip_dst, ip_src=ip_src, out_port=old_port)
        Interfaces._remove_flows(datapath, match, old_port)

    @staticmethod
    def _add_flow(datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
        print('Added new flow')

    @staticmethod
    def _remove_flows(datapath, match, out_port=None):
        """Create OFP flow mod message to remove flows from table."""
        ofproto = datapath.ofproto
        # Delete the flow
        if out_port:
            flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, command=ofproto.OFPFC_DELETE,
                                                          out_port=out_port, out_group=ofproto.OFPG_ANY,
                                                          match=match)
        else:
            flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, command=ofproto.OFPFC_DELETE,
                                                          out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
                                                          match=match)

        datapath.send_msg(flow_mod)
