#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

import os
import json
import logging
import sys; sys.path.insert(0, '')
import config
from gstate import GState


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

def write_init_models_factors_to_gstate():
    ''' Detact the test factors for the models and save to gstate. '''
    with PathRecover():
        models_ = [] # model.name -> factors
        for model in models():
                model_root = pjoin(config.models_path(), model)
                if not os.path.isfile(pjoin(model_root, 'continuous_evaluation.py')):
                    continue
                cd @(config.workspace)
                env = {}
                exec('from models.%s.continuous_evaluation import tracking_factors' % model, env)
                # status: 0 not start
                #         1 pass
                #        -1 fail
                models_.append((model, [(factor.name, 0) for factor in env['tracking_factors']],))
        GState.set(config._model_factors_, json.dumps(models_))

def update_model_factors_status():
    ''' update from _evaluation_result_. '''
    result = GState.get(config._evaluation_result_)

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
