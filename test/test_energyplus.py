from unittest import TestCase
from eptoolz.energyplus.energyplus import EnergyPlus, Config


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
        """ config doesn't support __setitem__ with arbitrary keys """
        with self.assertRaises(KeyError):
            self.config['arbitrary key'] = True

    def test_setitem_success(self):
        self.config['convert'] = True
        self.assertTrue(self.config['convert'])

    def test_update_fail(self):
        with self.assertRaises(KeyError):
            self.config.update({'arbitrary key': True})

    def test_update_success(self):
        self.config.update({'convert': True})
        self.assertTrue(self.config['convert'])


