import os
import sys
from flask import Flask, redirect, send_from_directory, render_template
import logics

SERVER_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
STATIC_DIR = os.path.join(SERVER_PATH, "static")
TEMPLATE_DIR = os.path.join(SERVER_PATH, "template")

app = Flask(
    "modelce", static_url_path=STATIC_DIR, template_folder=TEMPLATE_DIR)

baseline_commit_url = "https://github.com/Superjomn/paddle-modelci-baseline/commit"


@app.route('/')
def index():
    return render_template(
        'dashboard.html',
        baseline_commit_url=baseline_commit_url,
        last_success_commit=logics.last_success_commit(),
        last_fail_commit=logics.last_fail_commit(),
        current_working_on_commit=logics.current_working_on_commit(),
        current_progress=int(logics.current_progress() * 100),
        init_model_factors=logics.model_evaluation_status(), )


@app.route('/history')
def history():
    return render_template(
        'history.html',
        baseline_commit_url=baseline_commit_url,
        baseline_history=logics.baseline_history())


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(STATIC_DIR, path)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8080
    app.run(debug=True, host=host, port=port)
