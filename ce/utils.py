import logging
from plumbum import local


class log:
    @staticmethod
    def logger():
        mylogger = logging.getLogger(__name__)
        mylogger.setLevel(logging.INFO)
        if not mylogger.handlers:
            ch = logging.StreamHandler()
            mylogger.addHandler(ch)
        return mylogger

    @staticmethod
    def info(*args):
        log.logger().info(' '.join([str(s) for s in args]))

    @staticmethod
    def warn(*args):
        log.logger().warning(' '.join([str(s) for s in args]))

    def error(*args):
        log.logger().error(' '.join([str(s) for s in args]))

    def debug(*args):
        log.logger().debug(' '.join([str(s) for s in args]))


class dictobj(dict):
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        if item in self:
            return self[item]
        else:
            raise AttributeError("No such attribute: %s" % item)


def __(cmd):
    fs = cmd.split()
    cmd = local[fs[0]]
    args = fs[1:]
    return cmd(*args).strip()
