import data_view as dv
import unittest

class KpiTester(unittest.TestCase):
    def setUp(self):
        self.commitid = 'dfafa'
        self.task = 'task0'
        self.name = 'kpi0'

        dv.shared_db = None
        dv.init_shared_db(test=True)
        self.kpi = dv.Kpi(commitid=self.commitid, task=self.task, name=self.name)

    def test_persist(self):
        self.kpi.set_value(1.)
        self.kpi.persist()

    def test_query(self):
        self.kpi.set_value(1.)
        self.kpi.persist()

        another_kpi = dv.Kpi(commitid=self.commitid, task=self.task, name=self.name)
        info = another_kpi.fetch_infos()
        self.assertTrue(info)
        self.assertAlmostEqual(info['value'], 1.)

    def test_query_not_exist(self):
        another_kpi = dv.Kpi(commitid='not-exitsts', task=self.task, name=self.name)
        self.assertFalse(another_kpi.fetch_infos())

    def tearDown(self):
        record_id = dv.Kpi.gen_record_id(self.commitid, self.task, self.name)
        dv.shared_db.delete(record_id)


class TaskTester(unittest.TestCase):
    def setUp(self):
        self.commitid = 'dfadfx'
        self.name = 'task0'

        dv.shared_db = None
        dv.init_shared_db(test=True)
        self.task = dv.Task(commit=self.commitid, name=self.name)
        self.kpi = ['kpi0', 'kpi1', 'kpi2']


if __name__ == '__main__':
    unittest.main()

