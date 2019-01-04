#!/bin/bash

args=""
if [ $# -gt 0 ]; then
    args=$*
fi    

python main.py ${args}
