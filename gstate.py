from __future__ import absolute_import
import os
import config
import json
pjoin = os.path.join


class gstate:
    ''' A file based state database for information persistance. '''
    root = config.global_state_root()

    @staticmethod
    def set(key, value):
        if not os.path.isdir(gstate.root):
            os.mkdir(gstate.root)
        with open(pjoin(gstate.root, key), 'w') as f:
            f.write(str(value))

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

    progress_list = 'progress_list.json'

    @staticmethod
    def set_progress_list(li=['prepare/clone_code', 'prepare/compile']):
        '''
        list of str,
        '''
        gstate.set(gstate.progress_list, li)

    @staticmethod
    def get_progress_list():
        return gstate.get(gstate.progress_list)

    current_progress = 'current_progress.json'

    @staticmethod
    def set_current_progress(v):
        gstate.set(gstate.current_progress, v)

    @staticmethod
    def get_current_progress():
        return gstate.get(gstate.current_progress)

    baseline_history = 'baseline_history'

    @staticmethod
    def update_baseline_history(history):
        gstate.set(gstate.baseline_history, history)

    @staticmethod
    def get_baseline_history():
        return gstate.get(gstate.baseline_history)

    source_code_updated = 'source_code_updated'
    @staticmethod
    def set_source_code_updated(updated):
        ''' updated: bool, yes/no '''
        gstate.set(gstate.source_code_updated, 'yes' if updated else 'no')
    @staticmethod
    def get_source_code_updated():
        return gstate.get(gstate.source_code_updated) == 'yes'

    evaluation_records = 'evaluation_records'
    @staticmethod
    def add_evaluation_record(commitid, passed, time):
        history = gstate.get(gstate.evaluation_records)
        if not history:
            history = []
        history.append((commitid, passed, time))
        gstate.set(gstate.evaluation_records, json.dumps(history))
    @staticmethod
    def get_evaluation_records():
        history = gstate.get(gstate.evaluation_records)
        if not history:
            return []
        return json.loads(history)
