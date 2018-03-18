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
            content = '\n'.join([
                    'model0\tpass',
                    'model1\tpass',])
            utils.GState.set(config._evaluation_result_, content)
            self.assertTrue(utils.evaluation_succeed())

    def test_evaluation_succeed_fail(self):
        with utils.PathRecover():
            # prepare data

            content = '\n'.join([
                    'model0\tpass',
                    'model1\tfail',])
            utils.GState.set(config._evaluation_result_, content)
            self.assertFalse(utils.evaluation_succeed())

    def test_global_state_set(self):
        with utils.PathRecover():
            utils.GState.set("name", "jomn")
            self.assertEqual(utils.GState.get("name"), "jomn")

unittest.main(module='utils_test')
