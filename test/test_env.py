from unittest import TestCase
from eptoolz.env.envcheck import EnvCheck
from eptoolz.env.env import EPEnvironment
from eptoolz.exceptions import SetAfterCreateError
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
        self.assertRaises(FileNotFoundError,
                          self.envck.check_pyenergyplys)

    def test_check_health_fail(self):
        self.assertRaises(FileNotFoundError,
                          self.envck.check_health)


class TestEnvCheckSuccess(TestCase):
    def setUp(self):

        self.tmp = tempfile.TemporaryDirectory()
        fake_work_dir(self.tmp.name)
        self.envck = EnvCheck(self.tmp.name)

    def test_check_path_success(self):
        self.assertTrue(self.envck.check_path())

    def test_check_idd_success(self):
        self.assertTrue(self.envck.check_idd())

    def test_check_expandobjects_success(self):
        self.assertTrue(self.envck.check_expandobjects())

    def test_check_convertinputformat_success(self):
        self.assertTrue(self.envck.check_convertinputformat())

    def test_check_pyenergyplus_success(self):
        self.assertTrue(self.envck.check_pyenergyplys())

    def test_check_health_success(self):
        self.assertTrue(self.envck.check_health())

    def tearDown(self):
        self.tmp.cleanup()


class TestEnv(TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        fake_work_dir(self.tmp.name)
        self.idd = os.path.join(self.tmp.name, "E.idd")
        self.idf = os.path.join(self.tmp.name, "E.idf")
        self.epw = os.path.join(self.tmp.name, "E.epw")
        self.output = os.path.join(self.tmp.name, "out")
        print(self.tmp.name)

        self.env = EPEnvironment(
            env=self.tmp.name,
            idd=self.idd,
            idf=self.idf,
            epw=self.epw,
            output=self.output)

    def test_readonly(self):
        """
        Test readonly properties.
        """
        with self.assertRaises(SetAfterCreateError):
            self.env.env = ""

    def test_env(self):
        __import__('pdb').set_trace()
        self.assertTrue(self.env.output == self.output)
        self.assertTrue(self.env.env == self.tmp.name)
        self.assertTrue(self.env.idd == self.idd)
        self.assertTrue(self.env.idf == self.idf)
        self.assertTrue(self.env.epw == self.epw)

    def test_default(self):
        ...


def fake_work_dir(tempdir):
    with open(os.path.join(tempdir, "ExpandObjects"), 'w'):
        ...
    with open(os.path.join(
            tempdir, "Energy+.schema.epJson"), 'w'):
        ...
    with open(os.path.join(tempdir, "ConvertInputFormat"), 'w'):
        ...
    os.mkdir(os.path.join(tempdir, "pyenergyplus"))
    with open(os.path.join(
            tempdir, "pyenergyplus", "__init__.py"), 'w'):
        ...
    for n in ("api.py", "common.py", "func.py", "plugin.py",
              "runtime.py", "dataransfer.py"):
        with open(os.path.join(tempdir,
                               "pyenergyplus", n), 'w') as f:
            f.write("def foo(): print('imported!')")
    with open(os.path.join(tempdir, "E.idd"), 'w'):
        ...
    with open(os.path.join(tempdir, "E.idf"), 'w'):
        ...
    with open(os.path.join(tempdir, "E.epw"), 'w'):
        ...
