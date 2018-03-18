#!/usr/bin/env xonsh

rsync --port 8082 -O --no-perms -azP --exclude '/home/superjom/project/paddle3/contrib/modelci/paddle_code' \
                                     --exclude '/home/superjom/project/paddle3/contrib/modelci/models' \
                                     ../modelci rsync://172.19.61.250/projects/
