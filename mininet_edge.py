from manageInterfaces import Interfaces


class Configuration:

    def __init__(self):
        self.__ips = ['10.11.10.1',         # s1
                      '130.127.133.237',    # s2
                      '10.11.10.2',         # s3
                      '130.127.134.16',     # s4
                      '10.11.10.3',         # s5
                      '130.127.133.236',    # s6
                      '10.11.10.4',         # s7
                      '130.127.134.4',      # s8
                      '10.10.10.10',        # s9
                      '12.12.12.12']        # s10
        self.__macs = ['3c:fd:fe:55:ff:42',     # s1
                       '3c:fd:fe:55:ff:40',     # s2
                       '3c:fd:fe:55:f4:62',     # s3
                       '3c:fd:fe:55:f4:60',     # s4
                       '3c:fd:fe:55:fd:c2',     # s5
                       '3c:fd:fe:55:f4:60',     # s6
                       '3c:fd:fe:55:fe:62',     # s7
                       '3c:fd:fe:55:fe:60',     # s8
                       '3c:fd:fe:55:fe:60',     # s9
                       '3c:fd:fe:55:fe:60']     # s10

    def config_switche(self, datapath):
        print(datapath.id)
        id = datapath.id - 1
        print(self.__ips[id])
        print(self.__macs[id])


    @staticmethod
    def add_l2_flow(datapath, mac_src, in_port, mac_dst, out_port):
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        match = parser.OFPMatch(in_port=in_port, eth_dst=mac_dst, eth_src=mac_src)
        Interfaces.add_flow(datapath, 1, match, actions)
