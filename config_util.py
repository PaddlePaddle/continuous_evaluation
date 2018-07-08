from utils import dictobj, log
import configparser

config_path = './default.conf'


class Config(object):
    def __init__(self, path):
        log.warn('Loading config from %s' % path)
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get(self, session, key):
        return self.config.get(session, key)

    def get_int(self, session, key):
        return self.config.getint(session, key)

    def get_float(self, session, key):
        return self.config.getfloat(session, key)

    def get_bool(self, session, key):
        return self.config.getboolean(session, key)

    @staticmethod
    def Global(path=config_path):
        return Config(path)
