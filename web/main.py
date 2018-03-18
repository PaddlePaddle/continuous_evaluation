import os
import sys
from flask import Flask, redirect, send_from_directory, render_template
import logics

SERVER_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
STATIC_DIR = os.path.join(SERVER_PATH, "static")

app = Flask("modelce", static_url_path=STATIC_DIR, template_folder=STATIC_DIR)


@app.route('/')
def index():
    data = {
        'last_success_commit': logics.last_success_commit(),
        'last_fail_commit': logics.last_fail_commit(),
        'current_working_on_commit': logics.current_working_on_commit(),
        'current_progress': logics.current_progress(),
        'init_model_factors': logics.model_evaluation_status(),
    }
    return render_template('index.html', **data)
