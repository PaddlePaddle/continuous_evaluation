import os
import sys
from flask import Flask, request, redirect, send_from_directory, render_template_string
from flask_cache import Cache
sys.path.append('..')
from db import MongoDB
from datetime import datetime, timedelta
import _config
import json
import pprint
from kpi import Kpi
from view import *
from api import *
import pyecharts

SERVER_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
STATIC_DIR = os.path.join(SERVER_PATH, "static")
TEMPLATE_DIR = os.path.join(SERVER_PATH, "template")

app = Flask(
    "modelce", static_url_path=STATIC_DIR, template_folder=TEMPLATE_DIR)
cache = Cache(
    app, config={'CACHE_TYPE': 'filesystem',
                 'CACHE_DIR': './_cache'})
db = MongoDB(_config.db_name, _config.db_host, _config.db_port)


@app.route('/')
@cache.cached(timeout=120)
def index():
    '''
    build index page
    '''
    page, snips = build_index_page()
    tables = CommitRecord.get_all_tables()
    logics = merge_logics(snips[0].logic())
    return render_template_string(page, **logics)

@app.route('/main', methods=["GET"])
#@cache.cached(timeout=120)
def main():
    '''
    Show the status, the contents:

    a list of commitids and their status(passed or not, the info)
    '''
    table_name = request.args.get('table')
    page, snips = build_main_page(table_name)
    commits = CommitRecord.get_all(table_name)
    latest_commit = commits[-1].commit
    logics = merge_logics(snips[0].logic(table_name), snips[1].logic(table_name, latest_commit))
    print('commits', snips[0].logic(table_name))
    return render_template_string(page, **logics)


@app.route('/commit/details', methods=["GET"])
#@cache.cached(timeout=5)
def commit_details():
    table_name = request.args.get('table')
    commit = request.args.get('commit')

    page, snips = build_commit_detail_page(table_name)

    logics = snips[0].logic(table_name, commit)
    return render_template_string(page, **logics)


@app.route('/commit/compare', methods=["GET"])
#@cache.cached(timeout=5)
def commit_compare():
    if 'cur' not in request.args:
        commits = CommitRecord.get_all()
        latest_commit = commits[-1]
        success_commits = [v for v in filter(lambda r: r.passed, commits)]
        latest_success_commit = success_commits[
            -1] if not latest_commit.passed else success_commits[-2]
        cur = latest_commit.commit
        base = latest_success_commit.commit
    else:
        cur = request.args.get('cur')
        base = request.args.get('base')

    page, (select_snip, result_snip) = build_compare_page()
    logics = merge_logics(select_snip.logic(), result_snip.logic(cur, base))
    return render_template_string(page, **logics)

#@cache.cached(timeout=120)
@app.route('/commit/draw_scalar', methods=["GET"])
def draw_scalar():
    table_name = request.args['table']
    task_name = request.args['task']

    page, (scalar_snap,) = build_scalar_page(task_name)
    logics = merge_logics(scalar_snap.logic(table_name))
    return render_template_string(page, **logics)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='CE Web')
    parser.add_argument('--port', type=int, default=80, required=False,
                    help='web service port')

    parser.add_argument('--host', type=str, default='0.0.0.0', required=False,
                    help='web service host')
    args = parser.parse_args()
    app.run(debug=True, host=args.host, port=args.port, threaded=True)
