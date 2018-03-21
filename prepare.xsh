#!/usr/bin/env xonsh
from utils import *
import config

def get_whl():
    log.warn("downloading %s from %s" % (config.whl_url(), config.whl_path()))
    download(config.whl_url(), config.whl_path())

def install_whl():
    log.warn("installing paddle whl %s" % (config.whl_path()))
    cd @(config.tmp_root())
    pip install --upgrade @(config.whl_path())
    # update status
    update_model_factors_status('prepare', 'install_whl', 'pass')

def compile():
    log.warn("compiling paddle source code %s" % config.local_repo_path())
    cd @(config.local_repo_path())
    mkdir -p build
    cd build
    flags = "-DCUDNN_ROOT=/usr -DCUDNN_LIBRARY=/usr/lib/x86_64-linux-gnu"
    log.info("cmake .. %s" % flags)
    cmake .. @(flags)
    flags = "-j10"
    log.info("make install", flags)
    make install @(flags)
    # TODO save the installed whl to paddle.whl
    tmp_whl = None
    cp @(config.compiled_whl_path()) @(config.whl_path())
    # update status
    update_model_factors_status('prepare', 'compile', 'pass')
