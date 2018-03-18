#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

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

    def error(*args):
        log.logger().error(' '.join([str(s) for s in args]))

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
    for line in GState.get_evaluation_result().split('\n'):
        model, status = line.strip().split('\t')
        if status != 'pass':
            return False
    return True

def models():
    with PathRecover():
        cd @(config.workspace)
        return filter(lambda x : not x.startswith('__'), $(ls models).strip().split())


class GState:
    ''' A file based state database for information persistance. '''
    root = config.global_state_root()

    @staticmethod
    def set(key, value):
        with open(pjoin(GState.root, key), 'w') as f:
            f.write(value)

    @staticmethod
    def get(key):
        if not os.path.isfile(pjoin(GState.root, key)): return None
        with open(pjoin(GState.root, key)) as f:
            return f.read().strip()

    @staticmethod
    def clear(key):
        path = pjoin(GState.root, key)
        if os.path.isfile(path):
            rm -f @(path)

    @staticmethod
    def set_evaluation_result(content):
        GState.set(config._evaluation_result_, content)
    @staticmethod
    def get_evaluation_result():
        return GState.get(config._evaluation_result_)


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
