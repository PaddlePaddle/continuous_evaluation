import os
import logging
import shutil

workspace = os.path.dirname(os.path.realpath(__file__))  # pwd
pjoin = os.path.join

# the directory structure
# Paddle/
#   modelce/
#     tasks
# DEBUG
relative_path = os.environ.get('relative_path', '..')
paddle_path = pjoin(workspace, relative_path)
#paddle_path = '/chunwei/Paddle'

baseline_repo_url = os.environ.get('repo_url', 'git@github.com:PaddlePaddle/paddle-ce-latest-kpis.git')

baseline_path = pjoin(workspace, 'tasks')

tmp_root = pjoin(workspace, "tmp")

# if the latest kpi is better than best kpi by 1%, update the best kpi.
kpi_update_threshold = 0.3

# mongodb config
#db_name = "ce"
db_name = os.environ.get('db_name', 'ce')
# for test, use following config
# db_host = 'ce.paddlepaddle.org'
# db_port = 8006

db_host = os.environ.get('db_host', '127.0.0.1')
db_port = os.environ.get('db_port', 27017)
table_name = os.environ.get('table_name', 'logs')

develop_evaluate = os.environ.get('develop_evaluate', 'False')

develop_db_name = os.environ.get('develop_db_name', 'ce_develop')
develop_db_host = os.environ.get('develop_db_host', '127.0.0.1')
develop_db_port = os.environ.get('develop_db_port', 27017)
develop_table_name = os.environ.get('develop_table_name', 'develop_logs')
