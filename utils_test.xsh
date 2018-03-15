#!/usr/bin/env xonsh
import config
import unittest
import utils
import os

class TestMain(unittest.TestCase):
    def setUp(self):
        config.switch_to_test_mode()

    def test_log(self):
        utils.log.logger().info("hello")

    def test_PathRecover(self):
        cur = $(pwd).strip()
        with utils.PathRecover():
            cd ../
            print("switched", $(pwd))
            self.assertNotEqual($(pwd).strip(), cur)
        self.assertEqual($(pwd).strip(), cur)

    def test_download(self):
        with utils.PathRecover():
            cd @(config.test_root)
            utils.log.warn('downloading html')
            utils.download('http://www.baidu.com', '1.html')
            self.assertTrue(os.path.isfile('1.html'))
            rm -f 1.html

    def test_evaluation_succeed(self):
        with utils.PathRecover():
            # prepare data
            with open(config.success_flag_file(), 'w') as f:
                f.write('\n'.join([
                    'model0\tpass',
                    'model1\tpass',
                ]))
            self.assertTrue(utils.evaluation_succeed())

    def test_evaluation_succeed_fail(self):
        with utils.PathRecover():
            # prepare data
            with open(config.success_flag_file(), 'w') as f:
                f.write('\n'.join([
                    'model0\tpass',
                    'model1\tfail',
                ]))
            self.assertFalse(utils.evaluation_succeed())

unittest.main(module='utils_test')
