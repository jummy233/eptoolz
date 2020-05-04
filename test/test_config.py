from unittest import TestCase
from eptoolz.config.envcheck import EnvCheck
from eptoolz.config.config import EPConfig
import tempfile
import os
import sys


class TestEnvCheckFail(TestCase):

    def setUp(self):
        self.envck = EnvCheck('./tmpep')

    def test_check_path_fail(self):
        self.assertRaises(FileNotFoundError, self.envck.check_path)

    def test_check_idd_fail(self):
        self.assertRaises(FileNotFoundError, self.envck.check_idd)

    def test_check_expandobjects_fail(self):
        self.assertRaises(FileNotFoundError, self.envck.check_expandobjects)

    def test_check_convertinputformat_fail(self):
        self.assertRaises(FileNotFoundError,
                          self.envck.check_convertinputformat)

    def test_check_pyenergyplus_fail(self):
        sys.path.insert(0, self.envck.envpath)
        self.assertRaises(FileNotFoundError,
                          self.envck.check_pyenergyplys)

    def test_check_health_fail(self):
        self.assertRaises(FileNotFoundError,
                          self.envck.check_health)


class TestEnvCheckSuccess(TestCase):
    def setUp(self):

        self.tmp = tempfile.TemporaryDirectory()
        self.envck = EnvCheck(self.tmp.name)
        with open(os.path.join(self.tmp.name, "ExpandObjects"), 'w'):
            ...
        with open(os.path.join(
                self.tmp.name, "Energy+.schema.epJson"), 'w'):
            ...
        with open(os.path.join(self.tmp.name, "ConvertInputFormat"), 'w'):
            ...

        os.mkdir(os.path.join(self.tmp.name, "pyenergyplus"))

        with open(os.path.join(self.tmp.name,
                  "pyenergyplus", "__init__.py"), 'w'):
            ...
        with open(os.path.join(self.tmp.name, "pyenergyplus", "api.py"), 'w'):
            ...

    def test_check_path_success(self):
        self.assertTrue(self.envck.check_path())

    def test_check_idd_success(self):
        self.assertTrue(self.envck.check_idd())

    def test_check_expandobjects_success(self):
        self.assertTrue(self.envck.check_expandobjects())

    def test_check_convertinputformat_success(self):
        self.assertTrue(self.envck.check_convertinputformat())

    def test_check_pyenergyplus_success(self):
        sys.path.insert(0, self.envck.envpath)
        self.assertTrue(self.envck.check_pyenergyplys())

    def test_check_health_success(self):
        self.assertTrue(self.envck.check_health())

    def tearDown(self):
        self.tmp.cleanup()
