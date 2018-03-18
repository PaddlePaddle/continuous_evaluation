from __future__ import absolute_import
import os
import config
pjoin = os.path.join

class GState:
    ''' A file based state database for information persistance. '''
    root = config.global_state_root()

    @staticmethod
    def set(key, value):
        if not os.path.isdir(GState.root):
            os.mkdir(GState.root)
        with open(pjoin(GState.root, key), 'w') as f:
            f.write(value)

    @staticmethod
    def get(key):
        if not os.path.isfile(pjoin(GState.root, key)): return None
        with open(pjoin(GState.root, key)) as f:
            return f.read().strip()

    @staticmethod
    def clear(key):
        path = pjoin(GState.root, key)
        if os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def set_evaluation_result(content):
        GState.set(config._evaluation_result_, content)
    @staticmethod
    def get_evaluation_result():
        return GState.get(config._evaluation_result_)

