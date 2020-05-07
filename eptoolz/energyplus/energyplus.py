"""
Wrapper on energyplus executable.
"""
from typing import Dict
from collections import UserDict


class EnergyPlus:
    """
    Main entrance
    """

    def __init__(self, **kwargs):
        self.config: Config = kwargs

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value: Dict):
        """
        config setter.

        @raise e:  KeyError
        """
        tmp = Config()
        if not value == {}:
            tmp.update(value)
        self.__config = tmp


class Config(UserDict):
    """
    default config, can override already existed items.
    Config includes extra energyplus argument flags.
    """

    def __init__(self):
        super().__init__()

        # because the __setitem__ is override, to set new item
        # just use the super's __setitem__

        super().__setitem__('convert', False)
        super().__setitem__('annual', False)
        super().__setitem__('design_day', False)
        super().__setitem__('expandobjects', False)
        super().__setitem__('readvars', False)
        super().__setitem__('output_prefix', '')
        super().__setitem__('output_sufix', '')

    def __setitem__(self, key, value):
        if key not in self.keys():
            raise KeyError("Unsupported config field")
        super().__setitem__(key, value)


