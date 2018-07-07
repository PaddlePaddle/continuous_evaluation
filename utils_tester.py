from utils import *
import unittest

class LogTester(unittest.TestCase):
    def test_info(self):
        log.info("haha")

    def test_error(self):
        log.error("haha")

    def test_warn(self):
        log.warn("haha")

class dictobject_tester(unittest.TestCase):
    def test(self):
        a = dictobj()
        a.name = 'xxx0'

        self.assertEqual(a.name, 'xxx0')


if __name__ == '__main__':
    unittest.main()