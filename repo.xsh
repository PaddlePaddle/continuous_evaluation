#!/usr/bin/env xonsh
'''
some utils for clone repo, commit.
'''
import sys; sys.path.insert(0, '')
import config
from utils import *

def clone(url, dst):
    '''
    url: url of a git repo.
    dst: a abstract path in local file system.
    '''
    git clone @(url) @(dst)

def pull(dst):
    with PathRecover():
        cd @(dst)
        git pull
        log.warn(dst, 'updated')

def reset_commit(dst, commitid):
    with PathRecover():
        cd @(dst)
        git reset --hard dst @(commitid)
        log.warn(dst, 'reset to commit', commitid)

def get_commit(local_repo_path, short=False):
    with PathRecover():
        cd @(local_repo_path)
        flags = '%h' if short else '%H'
        if short:
            commit = $(git log -1 --pretty=format:%h).strip()
        else:
            commit = $(git log -1 --pretty=format:%H).strip()
        return commit

def get_paddle_commit(short=False):
    return get_commit(config.local_repo_path(), short)
