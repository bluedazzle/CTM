# coding: utf-8
from __future__ import unicode_literals

from unittest import TestCase

import os

class TestMain(TestCase):
    def setUp(self):
        pass

    def test_main(self):
        output = os.popen('cd ..;ls;python src/ctm/main.py --f SampleInput.txt').readlines()
        self.assertIn('Track2\n', output)