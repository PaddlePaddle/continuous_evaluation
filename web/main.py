import os
import sys
import logging
from flask import Flask, redirect, send_from_directory, render_template
from flask.ext.cache import Cache
import logics

logging.basicConfig()

SERVER_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
STATIC_DIR = os.path.join(SERVER_PATH, "static")
TEMPLATE_DIR = os.path.join(SERVER_PATH, "template")

app = Flask(
    "modelce", static_url_path=STATIC_DIR, template_folder=TEMPLATE_DIR)
cache = Cache(
    app, config={'CACHE_TYPE': 'filesystem',
                 'CACHE_DIR': './_cache'})

baseline_commit_url = "https://github.com/Superjomn/paddle-modelci-baseline/commit"
paddle_commit_url = "https://github.com/PaddlePaddle/Paddle/commit"


@app.route('/')
@cache.cached(timeout=10)
def index():
    return render_template(
        'dashboard.html',
        current_module='dashboard',
        paddle_commit_url=paddle_commit_url,
        source_code_updated=logics.source_code_updated(),
        baseline_commit_url=baseline_commit_url,
        last_success_commit=logics.last_success_commit(),
        last_fail_commit=logics.last_fail_commit(),
        current_working_on_commit=logics.current_working_on_commit(),
        current_progress=int(logics.current_progress() * 100),
        init_model_factors=logics.model_evaluation_status(),
        evaluation_records=logics.evaluation_records())


@app.route('/history')
@cache.cached(timeout=30)
def history():
    return render_template(
        'history.html',
        current_module='history',
        baseline_commit_url=baseline_commit_url,
        baseline_history=logics.baseline_history())


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(STATIC_DIR, path)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8080
    app.run(debug=False, host=host, port=port)
