#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True
import os
import sys; sys.path.insert(0, '')
import unittest
import config
from utils import *
from baseline_strategy import GitStrategy


class TestMain(unittest.TestCase):
    def setUp(self):
        config.switch_to_test_mode()
        assert "_test" in config.workspace
        self.obj = GitStrategy(config.baseline_repo_url(),
                               config.baseline_local_repo_path())

    def test_refresh_workspace(self):
        self.obj.refresh_workspace()
        self.assertEqual(self.obj.cur_branch, "develop")

    # def test_update_baseline(self):
    #     self.obj.refresh_workspace()
        # TODO use some toy branch to test
        # self.obj.update_baseline()


unittest.main(module='baseline_strategy_test')
