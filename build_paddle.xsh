#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True
$XONSH_SHOW_TRACEBACK = True

import sys; sys.path.insert(0, '')
import config
import subprocess
import os

cd @(config.paddle_path)
mkdir -p build
cd build
rm -rf python/dist/*
rm -rf python/build

#WITH_TESTING = os.environ.get('WITH_TESTING', 'OFF')

subprocess.call("WITH_TESTING=ON "
    "WITH_GOLANG=OFF "
    "CMAKE_BUILD_TYPE=Release "
    "WITH_GPU=ON "
    "WITH_STYLE_CHECK=OFF "
    "WITH_FLUID_ONLY=ON "
    "WITH_MKL=ON "
    "WITH_MKLDNN=ON "
    "WITH_DISTRIBUTE=ON "
    "WITH_ANAKIN=OFF "
    "WITH_INFERENCE_API_TEST=OFF "
    "paddle/scripts/paddle_build.sh build",
    shell=True,
    cwd=config.paddle_path
)


cd @(config.paddle_path)
cd build
pip install --upgrade python/dist/*.whl
