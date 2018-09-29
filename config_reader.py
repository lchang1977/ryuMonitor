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

    def best_p(self):
        return self.config.getint('SARIMA', 'best_p')

    def best_d(self):
        return self.config.getint('SARIMA', 'best_d')

    def best_q(self):
        return self.config.getint('SARIMA', 'best_q')

    def best_P(self):
        return self.config.getint('SARIMA', 'best_P')

    def best_D(self):
        return self.config.getint('SARIMA', 'best_D')

    def best_Q(self):
        return self.config.getint('SARIMA', 'best_Q')

    def best_S(self):
        return self.config.getint('SARIMA', 'best_S')
