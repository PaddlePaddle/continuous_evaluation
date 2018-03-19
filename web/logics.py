import sys; sys.path.append('..')
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
    return 0.56

def model_evaluation_status():
    model_factor_status = gstate.get(config._model_factors_)
    model_factor_status = json.loads(model_factor_status) if model_factor_status else []
    for model in model_factor_status:
        for factor in model[1]:
            factor[1] = bootstrap_status[factor[1]]
    # model_factor_status.insert(0, preparation)
    return model_factor_status
