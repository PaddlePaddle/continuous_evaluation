#!/usr/bin/env xonsh
import os
import sys; sys.path.insert(0, '')

import prepare
import config
import repo
import baseline
from utils import *
from core import TestError

# set environ for tests to load core.py
# TODO no need two ways to set environment
$modelci_root = config.workspace
os.environ['modelci_root'] = config.workspace

def test_released_whl():
    prepare.get_whl()
    prepare.install_whl()
    test_models()

def test_latest_source():
    log.warn('init local paddle repo %s' % config.local_repo_path())
    if not os.path.isdir(config.local_repo_path()):
        repo.clone(config.repo_url(), config.local_repo_path())
    repo.pull(config.local_repo_path())
    prepare.compile()
    prepare.install_whl()
    test_models()

def test_models():
    cd @(config.workspace)
    baseline.strategy.refresh_workspace()
    evaluate_status = []
    log.info('begin to evaluate model')
    for path in $(ls models).split():
        log.info('get model path', path)
        status = 'fail'
        if not path.startswith('__'):
            model_path = pjoin(config.workspace, path)
            try:
                test_model(path)
                status = 'pass'
            except TestError:
                log.warn('test model %s failed' % path)
            except Exception as e:
                log.warn('model %s execute error' % path)
                status = 'exec error: %s' % sys.exc_info()[0]
            evaluate_status.append((path, status))

    update_evaluation_status(evaluate_status, config.success_flag_file())
    log.warn('evaluation result:\n%s' % open(config.success_flag_file()).read())

    baseline.strategy()


def test_model(model_name):
    model_dir = pjoin(config.models_path(), model_name)
    log.info('model dir', model_dir)
    def run_model():
        log.warn('running model ', model_name)
        ./train.xsh
        log.warn('finish running model')
    def evaluate_model():
        log.warn('evaluating model ', model_name)
        log.info('models_path', config.models_path())
        model_root = pjoin(config.models_path(), model_name)
        log.info('model_root', model_root)
        cd @(config.workspace)
        env = {}
        exec('from models.%s.continuous_evaluation import tracking_factors' % model_name, env)
        tracking_factors = env['tracking_factors']
        for factor in tracking_factors:
            factor.evaluate(model_root)

    with PathRecover():
        cd @(model_dir)
        run_model()
        evaluate_model()

def update_evaluation_status(status, path):
    ''' persist the evaluation status to path '''
    with PathRecover():
        with open(path, 'w') as f:
            lines = ['%s\t%s' % kv for kv in status]
            f.write('\n'.join(lines))

test_latest_source()
# test_model('resnet30')
# test_models()
