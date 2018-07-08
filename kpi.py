from __future__ import division
import json
import numpy
import data_view as dv
import os


class Kpi(object):
    dic = {}

    def __init__(self,
                 name,
                 desc='',
                 out_file=None,
                 his_file=None,
                 actived=False,
                 unit_repr='',
                 short_description='',
                 description=''):
        ''' Interface for Kpi tracker.
        actived: whether this test is turn on
            The test will yield error if failed only if it is actived.
        unit_repr: the unit of the KPI, for train_duration, ms for example.
        desc: the description of this task. '''
        self.name = name
        self.desc = desc
        self.out_file = out_file
        self.his_file = "latest_kpis/" + out_file if his_file is None else his_file
        self.actived = actived
        self.unit_repr = unit_repr
        self.records = []
        self.short_description = short_description
        self.description = description

        # calculated kpis
        self._kpi = None

    def add_record(self, rcd):
        self.records.append(rcd)

    def evaluate(self):
        ''' Run the evaluation based on the records collected and history records. '''
        raise NotImplementedError

    def persist(self):
        ''' Persist the evalution result in some way. '''
        commitid = os.environ.get('commitid', None)
        task = os.environ.get('task', None)
        assert commitid
        assert task
        assert self._kpi
        kpi = dv.Kpi(
            commitid=commitid,
            task=task,
            name=self.name,
            value=self._kpi,
            unit=self.unit_repr,
            short_description=self.short_description,
            description=self.description, )
        kpi.persist()

    @staticmethod
    def compare_with(cur, other):
        ''' compare `cur` with `other` and return a float ratio to indicate how much
        changes cur based on other.
        The `other` is the denominator, the result is like +/- (other-cur)/other, the
        `+/-` will make the result a positive ratio if `cur` is better, negative other-
        wise.
        '''
        raise NotImplementedError

    @staticmethod
    def cal_kpi(data):
        ''' calculate the KPI(a scalar) based on `self.cur_data`.
        This is just a default implementation, free to customize.  '''
        return np.average(data)

    @property
    def cur_data(self):
        raise NotImplementedError

    @property
    def baseline_data(self):
        raise NotImplementedError

    @staticmethod
    def __register__(factor):
        '''
        factor shoud a subclass inherients Kpi
        '''
        assert issubclass(factor, Kpi)
        key = factor.__name__
        assert Kpi.dic.setdefault(key, factor) is factor, \
            "duplicate register %s with a different class" % key
        Kpi.dic[key] = factor


def get_baseline_kpi(task, kpi):
    '''
    Get the baseline record, the record might be a scalar or a data structure.
    :param task: str
    :param kpi: str
    :return: scalar or data structure.
    '''
    dv.shared_db.get()
