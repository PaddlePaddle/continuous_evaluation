#!/usr/bin/env xonsh
import os
import logging

workspace = $(pwd).strip()
pjoin = os.path.join

############################# OFFICIAL CONFIGS #############################

# repo address of PaddlePaddle
repo_url = 'https://github.com/PaddlePaddle/Paddle.git'

# the place to clone paddle source code
local_repo_path = pjoin(workspace, 'paddle_code')

# the compiled paddle whl to test
compiled_whl_path = '/usr/local/opt/paddle/share/wheels/paddlepaddle_gpu-0.11.1a1-cp27-cp27mu-linux_x86_64.whl'

# TODO change a official repo
# NOTE make sure that the evaluator machine has the access rights.
# the repo to store history baselines, by default, the latest will be pulled as the baseline.
baseline_repo_url = 'https://github.com/Superjomn/paddle-modelci-baseline.git'

baseline_local_repo_path = pjoin(workspace, 'models')

############################# CUSTOM CONFIGS #############################
# just do anything here
success_flag_file = pjoin(workspace, 'success.flag')

############################# DONT CHANGE BELOW #############################
tmp_root = pjoin(workspace, "tmp")
whl_path = pjoin(tmp_root, os.path.basename(compiled_whl_path))
models_path = pjoin(workspace, 'models')

log_path = pjoin(workspace, 'modelci.log')

test_root = pjoin(workspace, "_test_tmp_dir")


############################# DETAILS BELOW #############################
mkdir -p @(tmp_root)

# set logging
_log_format_ = '[%(asctime)-15s] %(message)s'
_log_level_ = logging.DEBUG
logging.basicConfig(format=_log_format_, level=_log_level_, filename=log_path)

def switch_to_test_mode():
    '''
    - set ci's workspace to test_root
    - clear test_root
    '''
    assert "_test_tmp_dir" in test_root
    if os.path.isdir(test_root):
        rm -rf @(test_root)
    mkdir @(test_root)

    global workspace
    workspace = test_root

    logging.basicConfig(format=_log_format_, level=_log_level_, filename=None)
