'''
This file contains all the commands.
'''
import os
import argparse
from ce.utils import local, __, log
from ce.utils import log
from ce.data_view import init_shared_db
from ce.config_util import Config

workspace = os.getcwd()
log.warn("The workspace is %s" % workspace)


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
    if '.' in task_name or task_name.startswith('__'):
        log.warn('skip path', task_name)
        return

    task_dir = os.path.join(workspace, task_name)
    with local.cwd(task_dir):
        if not os.path.isfile('run.xsh'):
            log.warn('Skip no-task path %s' % __('pwd'))
            return

        suc = False

        try:
            logs = __('./run.xsh')
            log.info(logs)
            suc = True
        except:
            pass

        return suc


def parse_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('--config', type=str, default='')
    arg.add_argument('--is_test', type=bool, default=False)
    return arg.parse_args()


if __name__ == '__main__':
    args = parse_args()

    Config.Global(args.config)
    init_shared_db(test=args.is_test)

    evaluate_all_tasks()
