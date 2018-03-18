#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

import os
import unittest
import sys; sys.path.insert(0, '')

import config
import core
from utils import PathRecover, pjoin

class GreaterWorseFactorTester(unittest.TestCase):
    def setUp(self):
        config.switch_to_test_mode()
        self.factor = core.GreaterWorseFactor("train", diff_thre=0.1)
        mkdir -p @(config.test_root)
        cd @(config.test_root)
        mkdir -p history

    def test_evaluate_success(self):
        # prepare data
        with open(self.factor.out_file, 'w') as f:
            f.write('\n'.join([
                '[0.1]',
                '[0.2]',
                '[0.31]',
            ]))
        with open(self.factor.his_file, 'w') as f:
            f.write('\n'.join([
                '[0.1]',
                '[0.2]',
                '[0.3]',
            ]))
        self.assertTrue(self.factor.evaluate(config.test_root))

    def test_evaluate_fail(self):
        # prepare data
        with open(self.factor.out_file, 'w') as f:
            f.write('\n'.join([
                '[0.1]',
                '[0.2]',
                '[0.35]',
            ]))
        with open(self.factor.his_file, 'w') as f:
            f.write('\n'.join([
                '[0.1]',
                '[0.2]',
                '[0.3]',
            ]))
        self.assertFalse(self.factor.evaluate(config.test_root))

    def test_persist(self):
        for i in range(3):
            self.factor.add_record(i)
        self.factor.persist()

        path = pjoin(config.test_root, 'train_factor.txt')
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
            self.assertEqual(content, '\n'.join([
                "[0]",
                "[1]",
                "[2]",
            ]))

    def error_info(self):
        err = self.factor.error_info
        self.assertTrue(err)


unittest.main(module='core_test')
