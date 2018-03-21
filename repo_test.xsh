#!/usr/bin/env xonsh

import repo

import os
import unittest
import config

class TestMain(unittest.TestCase):
    def setUp(self):
        config.switch_to_test_mode()

    def test_clone(self):
        pass

unittest.main(module='repo_test')
