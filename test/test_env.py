from unittest import TestCase
from eptoolz.env.envcheck import EnvCheck
from eptoolz.env.env import EPEnvironment, Config
import tempfile
import os
import sys


class TestEnvCheckFail(TestCase):

    def setUp(self):
        self.envck = EnvCheck('./tmpep')
        sys.path.insert(1, self.envck.envpath)

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
        sys.path.insert(1, self.envck.envpath)
        fake_work_dir(self.tmp.name)

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


class TestConfig(TestCase):

    def setUp(self):
        self.config = Config()

    def test_access(self):
        self.assertFalse(self.config['convert'])
        self.assertFalse(self.config['annual'])
        self.assertFalse(self.config['design_day'])
        self.assertFalse(self.config['expandobjects'])
        self.assertFalse(self.config['readvars'])
        self.assertTrue(self.config['output_prefix'] == '')
        self.assertTrue(self.config['output_sufix'] == '')

    def test_setitem_fail(self):
        """ config doesn't support __setitem__ with arbitray keys """
        with self.assertRaises(KeyError):
            self.config['arbitray key'] = True

    def test_setitem_success(self):
        self.config['convert'] = True
        self.assertTrue(self.config['convert'])


class TestEnv(TestCase):

    def setUp(self):
        self.env = EPEnvironment
        self.tmp = tempfile.TemporaryDirectory()
        fake_work_dir(self.tmp.name)

    def test_output(self):
        ...

    def test_env(self):
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

    with open(os.path.join(tempdir,
                           "pyenergyplus", "__init__.py"), 'w'):
        ...

    for n in ("api.py", "common.py", "func.py", "plugin.py",
              "runtime.py", "dataransfer.py"):
        with open(os.path.join(tempdir,
                               "pyenergyplus", n), 'w') as f:
            f.write("def foo(): print('imported!')")

