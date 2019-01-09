#!/usr/bin/env python
#coding: utf-8
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This class is used to run remote command

Authors: guochaorong(guochaorong@baidu.com)
Date: 2018/07/11
"""

import sys
sys.path.append('pypage')
sys.path.append('..')
import _config
import json
import time
from db import MongoDB
from datetime import datetime, timedelta
from kpi import Kpi

import sys
db = MongoDB(_config.db_name)
from web.api import CommitRecord
from html import Html
from datetime import datetime

period = 7
today = datetime.now().strftime("%Y%m%d")


def gettimestamp(dd_str):
    timeArray = time.strptime(dd_str + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def get_target_commits(records):
    """get commits for this week"""
    need_commit = []
    for record in records:
        print(record.date)
        begin = datetime.now() - timedelta(days=period)
        print(begin)
        if record.date > begin:
            need_commit.append(record)
    return need_commit


def get_all_tasks(need_commit):
    """get details task info of this week"""
    print(need_commit)
    all_tasks = {}
    for commit in need_commit:
        print(commit.commit)
        print(commit.date)
        tasks = CommitRecord.get_tasks(commit.commit)
        for task, values in tasks.items():
            if not task in all_tasks.keys():
                all_tasks[task] = {'times': 0, 'commits': [], 'date': []}

            if not values['passed']:
                all_tasks[task]['times'] += 1
                all_tasks[task]['date'].append(commit.date.strftime("%Y-%m-%d"))
                all_tasks[task]['commits'].append(commit.commit)
            print(all_tasks)
    return all_tasks


def gen_html(all_tasks, build_dict, sums):
    """gen html for summary and model infos section"""
    hh = Html()
    with open('wiki.txt', 'r') as f:
        duty = f.read()
    failed_commit = get_failed_commit(all_tasks)
    suc = sums - len(failed_commit)
    hh.html_create(period, duty, sums, suc)

    for task, values in all_tasks.items():
        print(task, values)
        res = ''
        if values['times'] == 0:
            res += '''result: &emsp;\t<font color="blue">pass</font>\t<br>'''
        else:
            cm_str = ''
            for cm in values['commits']:
                if cm in build_dict.keys():
                    cm_str += build_dict[cm]['weburl'] + ' '
            status = "unsolved"
            if values['date'][-1] != today:
                status = "solved"
            res += '''result: failed <br> \t<font color="red">jobs: %s <br>status: %s</font>\t<br>''' \
                   %(cm_str, status)
        hh.html_add_param(task, res, task)


def get_failed_commit(all_tasks):
    """get failed commits for this week"""
    failed_commit = []
    for task, values in all_tasks.items():
        for cm in values['commits']:
            if cm not in failed_commit:
                failed_commit.append(cm)
    return failed_commit


if __name__ == '__main__':
    import traceback
    try:
        with open('teamcity.json') as json_file:
            build_dict = json.load(json_file)

        records = CommitRecord.get_all()
        need_commits = get_target_commits(records)
        all_tasks = get_all_tasks(need_commits)
        gen_html(all_tasks, build_dict, len(need_commits))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
