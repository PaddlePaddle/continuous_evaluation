#!/usr/bin/env python
'''
some utils for clone repo, commit.
'''
import sys; sys.path.insert(0, '')
from utils import PathRecover
import _config
import os
import subprocess


def clone(url, dst):
    '''
    url: url of a git repo.
    dst: a abstract path in local file system.
    '''
    cmd = "git clone url dst"
    os.system(cmd)


def get_commit(local_repo_path, short=False):
    with PathRecover():
        os.chdir(local_repo_path)
        flags = '%h' if short else '%H'
        if short:
            cmd = "git log -1 --pretty=format:%h"
            if os.system(cmd):
                commit = []
                return commit
            output = subprocess.check_output(cmd, shell=True)
            output = output.decode()
            commit = output.strip()
        else:
            cmd = "git log -1 --pretty=format:%H"
            if os.system(cmd):
                commit = []
                return commit
            output = subprocess.check_output(cmd, shell=True)
            output = output.decode()
            commit = output.strip()
            
        return commit


def get_commit_date(local_repo_path):
    ''' get UNIX timestamp '''
    with PathRecover():
        os.chdir(local_repo_path)
        cmd = "git log -1 --pretty=format:%ct"
        if os.system(cmd):
            return ""
        output = subprocess.check_output(cmd, shell=True)
        output = output.decode()
        date = output

        return date
