'''
Use a mongodb to persist the status of this framework.
'''
from db import MongoDB
import _config
import json

db = MongoDB(_config.db_name, host=_config.db_host, port=_config.db_port)

develop_db = MongoDB(_config.develop_db_name, host=_config.develop_db_host, port=_config.develop_db_port)


def add_evaluation_record(commitid, date, task, passed, infos, kpis, kpi_values, kpi_types,
                          kpi_objs, detail_infos, develop_infos):
    '''
    persist the evaluation infomation of a task to the database.

    commitid: str
    date: UNIX timestamp
    task: str
    passed: bool
    infos: list of string
    kpis: the kpis in a task, name -> kpivalues
    kpi_objs: objects of KPI.
    '''
    # delete old task record for this commit
    db.remove(_config.table_name, {
        'commitid': commitid,
        'type': 'kpi',
        'task': task,
    })

    # insert new record
    record = {
        'commitid': commitid,
        'date': date,
        'task': task,
        'type': 'kpi',
        'passed': passed,
        'infos': infos,
        'detail_infos': detail_infos,
        'develop_infos': develop_infos,
        'kpis-keys': kpis,
        'kpis-values':
        json.dumps(list(value.tolist() for value in kpi_values)),
        'kpi-types': kpi_types,
        'kpi-activeds': [kpi.actived for kpi in kpi_objs],
        'kpi-unit-reprs': [kpi.unit_repr for kpi in kpi_objs],
        'kpi-descs': [kpi.desc for kpi in kpi_objs],
    }
    db.insert_one(_config.table_name, record)


def get_kpis_from_db(tasks):
    '''
    '''
    sections = {"_id": 0, "kpis-values": 1, "kpis-keys": 1, "date": 1, "task": 1}
    key = [("date", -1)]
    kpis = {}
    for task in tasks:
        cond = {"task": task}
        res = develop_db.find_sections(_config.develop_table_name, cond, sections, key, limit=1)
        for i in res:
            kpis[i["task"]] = {"kpis-keys": i["kpis-keys"], "kpis-values": i["kpis-values"]}
    return kpis


if __name__ == "__main__":
    #tasks = ["model_ce_image_classification", "mnist"]
    tasks = ["model_ce_language_model"]
    tasks = ['resnet50_net_CPU', 'seq2seq', 'language_model', 'object_detection', 'lstm', 'mnist', 'fail_models', 'image_classification', 'vgg16', 'transformer', 'resnet50_net_GPU', 'resnet50']
    tasks = ['mnist']
    res = get_kpis_from_db(tasks)
    for k, v in res.items():
        print(k, v)
    
     
