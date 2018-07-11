import unittest
from ce.utils import __, log, local
from ce import data_view as dv
from ce.config_util import Config


class MainUnittest(unittest.TestCase):
    def setUp(self):
        with local.cwd('../test_env'):
            Config.Global('../default.conf')
            dv.init_shared_db(True)
            __('python ../ce/main.py --config ../default.conf --is_test 1')

    def test_add_record(self):
        pass

    def tearDown(self):
        log.warn('delete test db')

        dv.shared_db.client.drop_database('test')


if __name__ == '__main__':
    unittest.main()
