from __future__ import absolute_import
import os
import config
pjoin = os.path.join

class gstate:
    ''' A file based state database for information persistance. '''
    root = config.global_state_root()

    @staticmethod
    def set(key, value):
        if not os.path.isdir(gstate.root):
            os.mkdir(gstate.root)
        with open(pjoin(gstate.root, key), 'w') as f:
            f.write(value)

    @staticmethod
    def get(key):
        if not os.path.isfile(pjoin(gstate.root, key)): return None
        with open(pjoin(gstate.root, key)) as f:
            return f.read().strip()

    @staticmethod
    def clear(key):
        path = pjoin(gstate.root, key)
        if os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def set_evaluation_result(content):
        gstate.set(config._evaluation_result_, content)
    @staticmethod
    def get_evaluation_result():
        return gstate.get(config._evaluation_result_)

    progress_list = 'progress_list'
    @staticmethod
    def set_progress_list(li=['prepare/clone_code', 'prepare/compile']):
        '''
        list of str,
        '''
        gstate.set(gstate.progress_list, li)
    @staticmethod
    def get_progress_list():
        return gstate.get(gstate.progress_list)

