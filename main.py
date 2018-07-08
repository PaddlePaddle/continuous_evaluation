'''
This file contains all the commands.
'''
import os
import argparse
from utils import local, __, log
from config_util import Config

workspace = os.curdir()


def evaluate_all_tasks():
    log.info('Evaluate all the tasks in %s' % __('pwd'))
    dirs = __('ls').split()
    dirs = filter(lambda _: _.startswith('__'), dirs)
    sucs = []
    for task_name in dirs:
        suc = evaluate_task(task_name)
        sucs.append(suc)

    return sucs


def evaluate_task(task_name):
    task_dir = os.path.join(workspace, task_name)
    with local.cwd(task_dir):
        if not os.path.isfile('run.xsh'):
            log.warn('Skip no-task path %s' % __('pwd'))
            return

        suc = False

        try:
            log = __('./run.xsh')
            log.info(log)
            suc = True
        except:
            pass

        return suc


def parse_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('config')
    return arg.parse_args()


if __name__ == '__main__':

    args = parse_args()
