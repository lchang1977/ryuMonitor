import configparser

class Reader:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def react(self):
        return self.config.getboolean('DEFAULT', 'react')

    def save_aic(self):
        return self.config.getboolean('DEFAULT', 'compareAIC')

    def log_only(self):
        return self.config.getboolean('DEFAULT', 'log_only')

    def old_port(self):
        return self.config.getint('OVS', 'old_port')

    def new_port(self):
        return self.config.getint('OVS', 'new_port')
