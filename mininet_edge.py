from manageInterfaces import Interfaces


class Configuration:

    def __init__(self):
        self.__ips = {1: '10.0.0.1',       # h1
                      2: '10.0.0.2',       # h2
                      3: '10.0.0.3',       # h3
                      4: '10.0.0.4',       # h4
                      5: '10.0.0.5',       # h5
                      6: '10.0.0.6',       # h6
                      7: '10.0.0.7',       # h7
                      8: '10.0.0.8',       # h8
                      9: '10.0.0.9',       # h9
                      10: '10.0.0.10'}     # h10
        self.__macs = {1: 'f6:c0:28:8f:a5:9a',     # h1
                       2: 'd2:77:87:57:5d:69',     # h2
                       3: '8a:ae:bc:42:55:d8',     # h3
                       4: 'f6:c3:e5:59:2a:6d',     # h4
                       5: '5a:0d:09:aa:cd:f8',     # h5
                       6: '96:f3:f8:b7:84:ab',     # h6
                       7: '72:9e:d8:59:8b:d0',     # h7
                       8: '1e:75:d8:41:51:f9',     # h8
                       9: '4a:e2:74:fa:3e:c7',     # h9
                       10: 'ba:a7:e7:40:7e:95'}    # h10

        # map the inputs to the function blocks
        self.options = {1: self.__s1,
                        2: self.__s2,
                        3: self.__s3,
                        4: self.__s4,
                        5: self.__s5,
                        6: self.__s6,
                        7: self.__s7,
                        8: self.__s8,
                        9: self.__s9,
                        10: self.__s10}

    def config_switch(self, datapath):
        print(datapath.id)
        id = datapath.id
        print(self.__ips[id])
        print(self.__macs[id])
        self.options[id](datapath)

    def __s1(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s1-eth3")
        self.add_l2_flow(datapath, self.__macs[2], "s1-eth4")
        self.add_l2_flow(datapath, self.__macs[3], "s1-eth2")
        self.add_l2_flow(datapath, self.__macs[4], "s1-eth3")
        self.add_l2_flow(datapath, self.__macs[5], "s1-eth1")
        self.add_l2_flow(datapath, self.__macs[6], "s1-eth2")
        self.add_l2_flow(datapath, self.__macs[7], "s1-eth2")
        self.add_l2_flow(datapath, self.__macs[8], "s1-eth2")
        self.add_l2_flow(datapath, self.__macs[9], "s1-eth2")
        self.add_l2_flow(datapath, self.__macs[10], "s1-eth3")

    # IMPORTANT!!
    def __s2(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s2-eth4")
        self.add_l2_flow(datapath, self.__macs[2], "s2-eth4")
        self.add_l2_flow(datapath, self.__macs[3], "s2-eth5")
        self.add_l2_flow(datapath, self.__macs[4], "s2-eth5")
        self.add_l2_flow(datapath, self.__macs[5], "s2-eth4")
        self.add_l2_flow(datapath, self.__macs[6], "s2-eth1")
        self.add_l2_flow(datapath, self.__macs[7], "s2-eth2")
        self.add_l2_flow(datapath, self.__macs[8], "s2-eth5")
        self.add_l2_flow(datapath, self.__macs[9], "s2-eth3")
        self.add_l2_flow(datapath, self.__macs[10], "s2-eth5")

    def __s3(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s3-eth2")
        self.add_l2_flow(datapath, self.__macs[2], "s3-eth2")
        self.add_l2_flow(datapath, self.__macs[3], "s3-eth1")
        self.add_l2_flow(datapath, self.__macs[4], "s3-eth2")
        self.add_l2_flow(datapath, self.__macs[5], "s3-eth2")
        self.add_l2_flow(datapath, self.__macs[6], "s3-eth2")
        self.add_l2_flow(datapath, self.__macs[7], "s3-eth2")
        self.add_l2_flow(datapath, self.__macs[8], "s3-eth2")
        self.add_l2_flow(datapath, self.__macs[9], "s3-eth2")
        self.add_l2_flow(datapath, self.__macs[10], "s3-eth2")

    def __s4(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s4-eth2")
        self.add_l2_flow(datapath, self.__macs[2], "s4-eth2")
        self.add_l2_flow(datapath, self.__macs[3], "s4-eth2")
        self.add_l2_flow(datapath, self.__macs[4], "s4-eth1")
        self.add_l2_flow(datapath, self.__macs[5], "s4-eth2")
        self.add_l2_flow(datapath, self.__macs[6], "s4-eth2")
        self.add_l2_flow(datapath, self.__macs[7], "s4-eth2")
        self.add_l2_flow(datapath, self.__macs[8], "s4-eth2")
        self.add_l2_flow(datapath, self.__macs[9], "s4-eth2")
        self.add_l2_flow(datapath, self.__macs[10], "s4-eth2")

    def __s5(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s5-eth2")
        self.add_l2_flow(datapath, self.__macs[2], "s5-eth2")
        self.add_l2_flow(datapath, self.__macs[3], "s5-eth2")
        self.add_l2_flow(datapath, self.__macs[4], "s5-eth2")
        self.add_l2_flow(datapath, self.__macs[5], "s5-eth2")
        self.add_l2_flow(datapath, self.__macs[6], "s5-eth2")
        self.add_l2_flow(datapath, self.__macs[7], "s5-eth2")
        self.add_l2_flow(datapath, self.__macs[8], "s5-eth1")
        self.add_l2_flow(datapath, self.__macs[9], "s5-eth2")
        self.add_l2_flow(datapath, self.__macs[10], "s5-eth2")

    def __s6(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s6-eth1")
        self.add_l2_flow(datapath, self.__macs[2], "s6-eth4")
        self.add_l2_flow(datapath, self.__macs[3], "s6-eth3")
        self.add_l2_flow(datapath, self.__macs[4], "s6-eth3")
        self.add_l2_flow(datapath, self.__macs[5], "s6-eth2")
        self.add_l2_flow(datapath, self.__macs[6], "s6-eth2")
        self.add_l2_flow(datapath, self.__macs[7], "s6-eth2")
        self.add_l2_flow(datapath, self.__macs[8], "s6-eth3")
        self.add_l2_flow(datapath, self.__macs[9], "s6-eth2")
        self.add_l2_flow(datapath, self.__macs[10], "s6-eth3")

    # IMPORTANT!!
    def __s7(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s7-eth3")
        self.add_l2_flow(datapath, self.__macs[2], "s7-eth3")
        self.add_l2_flow(datapath, self.__macs[3], "s7-eth2")
        self.add_l2_flow(datapath, self.__macs[4], "s7-eth2")
        self.add_l2_flow(datapath, self.__macs[5], "s7-eth3")
        self.add_l2_flow(datapath, self.__macs[6], "s7-eth2")
        self.add_l2_flow(datapath, self.__macs[7], "s7-eth2")
        self.add_l2_flow(datapath, self.__macs[8], "s7-eth2")
        self.add_l2_flow(datapath, self.__macs[9], "s7-eth3")
        self.add_l2_flow(datapath, self.__macs[10], "s7-eth1")

    def __s8(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s8-eth1")
        self.add_l2_flow(datapath, self.__macs[2], "s8-eth1")
        self.add_l2_flow(datapath, self.__macs[3], "s8-eth1")
        self.add_l2_flow(datapath, self.__macs[4], "s8-eth1")
        self.add_l2_flow(datapath, self.__macs[5], "s8-eth1")
        self.add_l2_flow(datapath, self.__macs[6], "s8-eth1")
        self.add_l2_flow(datapath, self.__macs[7], "s8-eth1")
        self.add_l2_flow(datapath, self.__macs[8], "s8-eth2")
        self.add_l2_flow(datapath, self.__macs[9], "s8-eth1")
        self.add_l2_flow(datapath, self.__macs[10], "s8-eth1")

    def __s9(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s9-eth2")
        self.add_l2_flow(datapath, self.__macs[2], "s9-eth1")
        self.add_l2_flow(datapath, self.__macs[3], "s9-eth2")
        self.add_l2_flow(datapath, self.__macs[4], "s9-eth2")
        self.add_l2_flow(datapath, self.__macs[5], "s9-eth2")
        self.add_l2_flow(datapath, self.__macs[6], "s9-eth2")
        self.add_l2_flow(datapath, self.__macs[7], "s9-eth2")
        self.add_l2_flow(datapath, self.__macs[8], "s9-eth2")
        self.add_l2_flow(datapath, self.__macs[9], "s9-eth2")
        self.add_l2_flow(datapath, self.__macs[10], "s9-eth2")

    def __s10(self, datapath):
        self.add_l2_flow(datapath, self.__macs[1], "s10-eth4")
        self.add_l2_flow(datapath, self.__macs[2], "s10-eth1")
        self.add_l2_flow(datapath, self.__macs[3], "s10-eth2")
        self.add_l2_flow(datapath, self.__macs[4], "s10-eth3")
        self.add_l2_flow(datapath, self.__macs[5], "s10-eth1")
        self.add_l2_flow(datapath, self.__macs[6], "s10-eth1")
        self.add_l2_flow(datapath, self.__macs[7], "s10-eth1")
        self.add_l2_flow(datapath, self.__macs[8], "s10-eth5")
        self.add_l2_flow(datapath, self.__macs[9], "s10-eth1")
        self.add_l2_flow(datapath, self.__macs[10], "s10-eth4")

    @staticmethod
    def add_l2_flow(datapath, mac_dst, out_port, in_port=None, mac_src=None):
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(out_port)]

        if in_port and mac_src:
            match = parser.OFPMatch(in_port=in_port, eth_dst=mac_dst, eth_src=mac_src)
        elif in_port:
            match = parser.OFPMatch(in_port=in_port, eth_dst=mac_dst)
        elif mac_src:
            match = parser.OFPMatch(eth_dst=mac_dst, eth_src=mac_src)
        else:
            match = parser.OFPMatch(eth_dst=mac_dst)
        Interfaces.add_flow(datapath, 1, match, actions)
