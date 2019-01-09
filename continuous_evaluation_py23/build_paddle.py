#!/usr/bin/env python
RAISE_SUBPROC_ERROR = True
XONSH_SHOW_TRACEBACK = True

import sys; sys.path.insert(0, '')
import _config
import subprocess
import os
import shutil


os.chdir(_config.paddle_path)
build = "build"
if os.path.exists(build):
    shutil.rmtree(build)
os.makedirs(build)
os.chdir(build)
if os.path.exists("python/dist"):
    shutil.rmtree("python/dist")
os.makedirs("python/dist_zy")
if os.path.exists("python/build"):
    shutil.rmtree("python/build")

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
    cwd=_config.paddle_path
)


os.chdir(_config.paddle_path)
os.chdir(build)
cmd = "pip install --upgrade python/dist/*.whl"
os.system(cmd)
