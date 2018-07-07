'''
Defines all the data structures in Python, it will make the database data operation easier.
'''

import json
from utils import dictobj
from config_util import Config
from db import RedisDB, escape_bstr

shared_db = None

def init_shared_db(test=False):
    global shared_db
    if not shared_db:
        config = Config.Global()
        shared_db = RedisDB(host=config.get('database', 'host'),
                            port=config.get_int('database', 'port'),
                            db=config.get_int('database', 'id'),
                            test=test)


class Commit:
    def __init__(self, commitid, date=None, tasks=[]):
        '''
        :param commitid: str
            long commit id.
        :param date: None
        :param tasks: list of str
            names of tasks.
        '''
        self.data = dictobj()
        self.data.commitid = commitid
        self.data.date = date
        self.data.tasks = []

        self.record_id = commitid

    def persist(self):
        init_shared_db()
        message = json.dumps(self.data)
        assert shared_db.set(self.record_id, message)
        return self.record_id

    def fetch_info(self):
        '''
        Fetch the commit infomation.
        :return: self
        '''
        init_shared_db()

        message = shared_db.get(self.record_id)
        assert message, 'no record called %s' % self.record_id
        self.data = dictobj(json.loads(message))

    def fetch_tasks(self):
        '''
        :return: list of Task
        '''
        assert self.data.tasks, 'fetch_info first'
        tasks = []
        for task in self.data.tasks:
            info = shared_db.get(Task.gen_record_id(self.data.commitid, task))
            if info:
                info = json.loads(info)
                task = Task()
                task.data = info
                tasks.append(task)
        return tasks


class Task:
    def __init__(self, commit='', name=''):
        self.data = dictobj()
        self.data.name = name
        self.data.commit = commit
        # Execution environment.
        self.data.env_desc = ''
        # list of Kpi
        self.data.kpis = []

    @staticmethod
    def gen_record_id(commitid, task):
        '''
        :param commitid: str
        :param task: str
        :return: str
        '''
        return "%s/%s" % (commitid, task)

    @property
    def record_id(self):
        assert self.commit
        assert self.name
        return Task.gen_record_id(self.data.commitid, self.data.name)

    def persist(self):
        init_shared_db()
        message = json.dumps(self.data)
        shared_db.set(self.record_id, message)
        return self.record_id

    def fetch_kpis(self):
        '''
        :return: list of KPI.
        '''
        assert self.data.kpis
        init_shared_db()
        kpis = []
        for kpi in self.data.kpis:
            info = shared_db.get(kpi)
            if info:
                data = json.loads(info)
                kpi = Kpi()
                kpi.data = data
                kpis.append(kpi)
        return kpis

class Kpi:
    '''
    KPI data view.
    '''
    def __init__(self, commitid='', task='', name='', data=None):
        if data:
            self.data = data
        else:
            self.data = dictobj()
            self.data.commitid = commitid
            self.data.task = task
            # str
            self.data.name = name
            # int or bool
            self.data.value = None
            self.data.short_description = ''
            self.data.description = ''

    def set_value(self, val):
        '''
        Set the value of the kpi
        :param val: any kind
        :return: None
        '''
        self.data.value = val

    def fetch_infos(self):
        record = shared_db.get(self.record_id)
        if record:
            record = escape_bstr(record)
            return json.loads(record)

    @staticmethod
    def gen_record_id(commitid, tasks, kpi):
        assert commitid
        assert tasks
        assert kpi
        return "%s/%s/%s" % (commitid, tasks, kpi)

    @property
    def record_id(self):
        return self.gen_record_id(self.data.commitid, self.data.task, self.data.name)

    def persist(self):
        init_shared_db()
        message = json.dumps(self.data)
        shared_db.set(self.record_id, message)
        return self.record_id

