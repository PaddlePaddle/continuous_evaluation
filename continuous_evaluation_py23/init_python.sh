export LD_LIBRARY_PATH=/opt/_internal/cpython-3.7.0/lib/:${LD_LIBRARY_PATH}
export PATH=/opt/_internal/cpython-3.7.0/bin/:${PATH}
export PYTHON_FLAGS='-DPYTHON_EXECUTABLE:FILEPATH=/opt/_internal/cpython-3.7.0/bin/python3.7
            -DPYTHON_INCLUDE_DIR:PATH=/opt/_internal/cpython-3.7.0/include/python3.7m
            -DPYTHON_LIBRARIES:FILEPATH=/opt/_internal/cpython-3.7.0/lib/libpython3.so'
