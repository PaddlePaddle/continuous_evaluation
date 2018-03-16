#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True
import os
import logging

workspace = $(pwd).strip()
mode = "production"

############################# OFFICIAL CONFIGS #############################
pjoin = os.path.join

# repo address of PaddlePaddle
repo_url = lambda: 'https://github.com/PaddlePaddle/Paddle.git'

# the place to clone paddle source code
local_repo_path = lambda: pjoin(workspace, 'paddle_code')

# the compiled paddle whl to test
compiled_whl_path = lambda: '/usr/local/opt/paddle/share/wheels/paddlepaddle_gpu-0.11.1a1-cp27-cp27mu-linux_x86_64.whl'

# TODO change a official repo
# NOTE make sure that the evaluator machine has the access rights.
# the repo to store history baselines, by default, the latest will be pulled as the baseline.
baseline_repo_url = lambda: 'git@github.com:Superjomn/paddle-modelci-baseline.git'

baseline_local_repo_path = lambda: pjoin(workspace, 'models')

############################# CUSTOM CONFIGS #############################
# just do anything here
success_flag_file = lambda: pjoin(workspace, 'success.flag')

############################# DONT CHANGE BELOW #############################
tmp_root = lambda: pjoin(workspace, "tmp")
whl_path = lambda: pjoin(tmp_root(), os.path.basename(compiled_whl_path()))
models_path = lambda: pjoin(workspace, 'models')

log_path = lambda: pjoin(workspace, 'modelci.log')

test_root = pjoin(workspace, "_test_tmp_dir")

global_state_root = lambda: pjoin(workspace, "_states")
mkdir -p @(global_state_root())
_state_paddle_code_commit_ = "paddle_code_commit"

############################# DETAILS BELOW #############################
mkdir -p @(tmp_root())

# set logging
_log_format_ = '[%(asctime)s %(levelname)s] %(message)s'
_log_level_ = logging.DEBUG
$model_ci_log_path=log_path()
logging.basicConfig(format=_log_format_, level=_log_level_, filename=log_path())

def switch_to_test_mode():
    '''
    - set ci's workspace to test_root
    - clear test_root
    '''
    global workspace, mode
    mode = 'test'
    if '_test_' not in workspace:
        workspace = test_root

    assert "_test_tmp_dir" in test_root
    if os.path.isdir(test_root):
        rm -rf @(test_root)
    mkdir @(test_root)

    global baseline_repo_url
    baseline_repo_url = lambda: "https://github.com/Superjomn/paddle-modelci-baseline.git"

    logging.basicConfig(format=_log_format_, level=_log_level_, filename=pjoin(workspace, 'test.log'))
