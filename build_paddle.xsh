#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True
$XONSH_SHOW_TRACEBACK = True

import sys; sys.path.insert(0, '')
import config
import subprocess

cd @(config.paddle_path)
cd build
rm -rf python/dist/*
rm -rf python/build

cd @(config.paddle_path)
cd build

# paddle_build.sh hides some flags, and some new flags can't be controlled
# by environment variable, so use cmake and set flag directly.
cmake .. \
  -DWITH_TESTING=OFF \
  -DWITH_GOLANG=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DWITH_GPU=ON \
  -DWITH_STYLE_CHECK=OFF \
  -DWITH_FLUID_ONLY=ON \
  -DWITH_MKL=ON \
  -DWITH_MKLDNN=ON \
  -DWITH_DISTRIBUTE=ON \
  -DWITH_ANAKIN=OFF
  
make -j
make install -j

pip install --upgrade python/dist/*.whl
