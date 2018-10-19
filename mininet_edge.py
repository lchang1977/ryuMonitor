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
        switch_id = datapath.id
        print(self.__ips[switch_id])
        print(self.__macs[switch_id])
        self.options[switch_id](datapath)

    def __s1(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 3)
        self.add_l2_flow(datapath, self.__macs[2], 4)
        self.add_l2_flow(datapath, self.__macs[3], 2)
        self.add_l2_flow(datapath, self.__macs[4], 3)
        self.add_l2_flow(datapath, self.__macs[5], 1)
        self.add_l2_flow(datapath, self.__macs[6], 2)
        self.add_l2_flow(datapath, self.__macs[7], 2)
        self.add_l2_flow(datapath, self.__macs[8], 2)
        self.add_l2_flow(datapath, self.__macs[9], 2)
        self.add_l2_flow(datapath, self.__macs[10], 3)

    # IMPORTANT!!
    def __s2(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 4)
        self.add_l2_flow(datapath, self.__macs[2], 4)
        self.add_l2_flow(datapath, self.__macs[3], 5)
        self.add_l2_flow(datapath, self.__macs[4], 5)
        self.add_l2_flow(datapath, self.__macs[5], 4)
        self.add_l2_flow(datapath, self.__macs[6], 1)
        self.add_l2_flow(datapath, self.__macs[7], 2)
        self.add_l2_flow(datapath, self.__macs[8], 5)
        self.add_l2_flow(datapath, self.__macs[9], 3)
        self.add_l2_flow(datapath, self.__macs[10], 5)

    def __s3(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 2)
        self.add_l2_flow(datapath, self.__macs[2], 2)
        self.add_l2_flow(datapath, self.__macs[3], 1)
        self.add_l2_flow(datapath, self.__macs[4], 2)
        self.add_l2_flow(datapath, self.__macs[5], 2)
        self.add_l2_flow(datapath, self.__macs[6], 2)
        self.add_l2_flow(datapath, self.__macs[7], 2)
        self.add_l2_flow(datapath, self.__macs[8], 2)
        self.add_l2_flow(datapath, self.__macs[9], 2)
        self.add_l2_flow(datapath, self.__macs[10], 2)

    def __s4(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 2)
        self.add_l2_flow(datapath, self.__macs[2], 2)
        self.add_l2_flow(datapath, self.__macs[3], 2)
        self.add_l2_flow(datapath, self.__macs[4], 1)
        self.add_l2_flow(datapath, self.__macs[5], 2)
        self.add_l2_flow(datapath, self.__macs[6], 2)
        self.add_l2_flow(datapath, self.__macs[7], 2)
        self.add_l2_flow(datapath, self.__macs[8], 2)
        self.add_l2_flow(datapath, self.__macs[9], 2)
        self.add_l2_flow(datapath, self.__macs[10], 2)

    def __s5(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 2)
        self.add_l2_flow(datapath, self.__macs[2], 2)
        self.add_l2_flow(datapath, self.__macs[3], 2)
        self.add_l2_flow(datapath, self.__macs[4], 2)
        self.add_l2_flow(datapath, self.__macs[5], 2)
        self.add_l2_flow(datapath, self.__macs[6], 2)
        self.add_l2_flow(datapath, self.__macs[7], 2)
        self.add_l2_flow(datapath, self.__macs[8], 1)
        self.add_l2_flow(datapath, self.__macs[9], 2)
        self.add_l2_flow(datapath, self.__macs[10], 2)

    def __s6(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 1)
        self.add_l2_flow(datapath, self.__macs[2], 4)
        self.add_l2_flow(datapath, self.__macs[3], 3)
        self.add_l2_flow(datapath, self.__macs[4], 3)
        self.add_l2_flow(datapath, self.__macs[5], 2)
        self.add_l2_flow(datapath, self.__macs[6], 2)
        self.add_l2_flow(datapath, self.__macs[7], 2)
        self.add_l2_flow(datapath, self.__macs[8], 3)
        self.add_l2_flow(datapath, self.__macs[9], 2)
        self.add_l2_flow(datapath, self.__macs[10], 3)

    # IMPORTANT!!
    def __s7(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 3)
        self.add_l2_flow(datapath, self.__macs[2], 3)
        self.add_l2_flow(datapath, self.__macs[3], 2)
        self.add_l2_flow(datapath, self.__macs[4], 2)
        self.add_l2_flow(datapath, self.__macs[5], 3)
        self.add_l2_flow(datapath, self.__macs[6], 2)
        self.add_l2_flow(datapath, self.__macs[7], 2)
        self.add_l2_flow(datapath, self.__macs[8], 2)
        self.add_l2_flow(datapath, self.__macs[9], 3)
        self.add_l2_flow(datapath, self.__macs[10], 1)

    def __s8(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 1)
        self.add_l2_flow(datapath, self.__macs[2], 1)
        self.add_l2_flow(datapath, self.__macs[3], 1)
        self.add_l2_flow(datapath, self.__macs[4], 1)
        self.add_l2_flow(datapath, self.__macs[5], 1)
        self.add_l2_flow(datapath, self.__macs[6], 1)
        self.add_l2_flow(datapath, self.__macs[7], 1)
        self.add_l2_flow(datapath, self.__macs[8], 2)
        self.add_l2_flow(datapath, self.__macs[9], 1)
        self.add_l2_flow(datapath, self.__macs[10], 1)

    def __s9(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 2)
        self.add_l2_flow(datapath, self.__macs[2], 1)
        self.add_l2_flow(datapath, self.__macs[3], 2)
        self.add_l2_flow(datapath, self.__macs[4], 2)
        self.add_l2_flow(datapath, self.__macs[5], 2)
        self.add_l2_flow(datapath, self.__macs[6], 2)
        self.add_l2_flow(datapath, self.__macs[7], 2)
        self.add_l2_flow(datapath, self.__macs[8], 2)
        self.add_l2_flow(datapath, self.__macs[9], 2)
        self.add_l2_flow(datapath, self.__macs[10], 2)

    def __s10(self, datapath):
        self.add_default_flow(datapath)
        self.add_l2_flow(datapath, self.__macs[1], 4)
        self.add_l2_flow(datapath, self.__macs[2], 1)
        self.add_l2_flow(datapath, self.__macs[3], 2)
        self.add_l2_flow(datapath, self.__macs[4], 3)
        self.add_l2_flow(datapath, self.__macs[5], 1)
        self.add_l2_flow(datapath, self.__macs[6], 1)
        self.add_l2_flow(datapath, self.__macs[7], 1)
        self.add_l2_flow(datapath, self.__macs[8], 5)
        self.add_l2_flow(datapath, self.__macs[9], 1)
        self.add_l2_flow(datapath, self.__macs[10], 4)

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

    @staticmethod
    def add_default_flow(datapath):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        Interfaces.add_flow(datapath, 0, match, actions)
