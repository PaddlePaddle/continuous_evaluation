#!/usr/bin/env xonsh
import os
import logging
import config

class log:
    @staticmethod
    def logger():
        return logging.getLogger(__name__)

    @staticmethod
    def info(*args):
        log.logger().info(' '.join([str(s) for s in args]))

    @staticmethod
    def warn(*args):
        log.logger().warning(' '.join([str(s) for s in args]))

    def debug(*args):
        log.logger().debug(' '.join([str(s) for s in args]))

def download(url, dst=None):
    log.warn('download', url, 'to %s' if dst else '')
    curl -o @(dst) @(url)

def pjoin(root, path):
    return os.path.join(root, path)

class PathRecover(object):
    ''' will jump back to the original path. '''
    def __enter__(self):
        self.pre_path = $(pwd).strip()

    def __exit__(self, type, value, trace):
        if $(pwd).strip() != self.pre_path:
            cd @(self.pre_path)

def evaluation_succeed():
    with open(config.success_flag_file) as f:
        for line in f.readlines():
            model, status = line.strip().split('\t')
            if status == 'fail':
                return False
    return True

SUC = True, ""

def CHECK_EQ(a, b, msg=""):
    return CHECK(a, b, "==", msg)
def CHECK_GT(a, b, msg=""):
    return CHECK(a, b, ">", msg)
def CHECK_GE(a, b, msg=""):
    return CHECK(a, b, ">=", msg)
def CHECK_LT(a, b, msg=""):
    return CHECK(a, b, "<", msg)
def CHECK_LE(a, b, msg=""):
    return CHECK(a, b, "<=", msg)

conds = {
    '>' : lambda a,b: a > b,
    '>=': lambda a,b: a >= b,
    '==' : lambda a,b: a == b,
    '<': lambda a,b: a < b,
    '<=': lambda a,b: a <= b,
}
def CHECK(a, b, cond, msg):
    if not conds[cond](a,b):
        return False, "CHECK {} {} {} failed.\n{}".format(a, cond, b, msg)
    return SUC
