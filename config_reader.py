import configparser

class Reader:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def react(self):
        return self.config.getboolean('DEFAULT', 'react')

    def save_aic(self):
        return self.config.getboolean('DEFAULT', 'compareAIC')

    def old_port(self):
        return int(self.config.get('OVS', 'old_port'))

    def new_port(self):
        return int(self.config.get('OVS', 'new_port'))
