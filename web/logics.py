from __future__ import division
import sys
sys.path.append('..')
import config
import json
from gstate import gstate

bootstrap_status = {
    -1: 'danger',
    0: 'light',
    1: 'success',
}

progress = [
    # phrase, weight
    ('prepare/update source code', 1),
    ('prepare/compile', 2),
]

preparation = ('preparation', [
    ('update source code', 0),
    ('compile', 0),
])


def last_success_commit():
    commit = gstate.get(config._success_commit_)
    return commit if commit else 'none'


def last_fail_commit():
    commit = gstate.get(config._fail_commit_)
    return commit if commit else 'none'


def current_working_on_commit():
    commit = gstate.get(config._state_paddle_code_commit_)
    return commit if commit else 'none'


def current_progress():
    if not source_code_updated(): return 0
    progresses = json.loads(gstate.get_progress_list())
    progress = gstate.get_current_progress()
    if progress:
        offset = progresses.index(progress)
        assert offset != -1
        ratio = (offset + 1) / len(progresses)
    else:
        ratio = 0
    return ratio


def model_evaluation_status():
    model_factor_status = gstate.get(config._model_factors_)
    model_factor_status = json.loads(
        model_factor_status) if model_factor_status else []
    for model in model_factor_status:
        for factor in model[1]:
            factor[1] = bootstrap_status[factor[1]]
    # model_factor_status.insert(0, preparation)
    return model_factor_status


def baseline_history():
    history = json.loads(gstate.get_baseline_history())
    return history


def source_code_updated():
    return gstate.get_source_code_updated()

def evaluation_records():
    history = gstate.get_evaluation_records()
    reversed(history)
    return history
