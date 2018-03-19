#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

import os
import json
import logging
import sys; sys.path.insert(0, '')
import config
from gstate import gstate


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
    for line in gstate.get_evaluation_result().split('\n'):
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
    log.info('write initial model factors to gstate')
    with PathRecover():
        models_ = [
            ('prepare', [
                ('update_baseline', 1, ''),
                ('update_source_code', 0, ''),
                ('compile', 0, ''),
                ('install_whl', 0, ''),
            ])
        ] # model.name -> factors
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
            models_.append((model, [(factor.name, 0, '') for factor in env['tracking_factors']],))
        gstate.set(config._model_factors_, json.dumps(models_))

def write_init_progress_to_gstate():
    status = json.loads(gstate.get(config._model_factors_))
    progress = []
    for model in status:
        for factor in model[1]:
            progress.append('%s/%s' % (model[0], factor[0]))
    gstate.set_progress_list(json.dumps(progress))

def update_model_factors_status(model, factor, status):
    ''' update _model_factors_ to tell the frontend the current status

    model: model name.
    factor: factor name.
    status: 'pass' or 'error info'.
    '''
    commit = gstate.get(config._state_paddle_code_commit_)
    state = json.loads(gstate.get(config._model_factors_))
    for model_ in state:
        if model_[0] == model:
            for factor_ in model_[1]:
                if factor_[0] == factor:
                    if status != 'pass':
                        factor_[1] = -1
                        factor_[2] = status
                    else:
                        factor_[1] = 1
                    break
            break
    gstate.set(config._model_factors_, json.dumps(state))
    gstate.set_current_progress("%s/%s" % (model, factor))

def init_progress_list_to_gstate():
    pass

def update_fail_commit_to_gstate():
    commit = gstate.get(config._state_paddle_code_commit_)
    gstate.set(config._fail_commit_, commit)

def update_success_commit_to_gstate(commit):
    gstate.set(config._success_commit_, commit)


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
