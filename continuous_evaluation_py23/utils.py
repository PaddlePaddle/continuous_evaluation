import logging
import os


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


class PathRecover(object):
    ''' will jump back to the original path. '''
    def __enter__(self):
        pwd = os.path.dirname(os.path.abspath(__file__))
        self.pre_path = pwd.strip()

    def __exit__(self, type, value, trace):
        pwd = os.path.dirname(os.path.abspath(__file__))
        if pwd.strip() != self.pre_path:
            os.chdir(self.pre_path)
