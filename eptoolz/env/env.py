"""
Global config class
This class contains all the information about runtime
includes path to EnergyPlus, output path, E+ parameters etc.
"""
import tempfile
import os.path as path
from eptoolz.env.envcheck import EnvCheck
from eptoolz.exceptions import SetAfterCreateError
from collections import UserDict
from typing import Dict, Optional


class EPEnvironment:
    """
    Singlton class for enviroment config

    This class provides path to:
        input:
            idd,
            idf,
        output:
            eso,
            htm,
            err,
    """

    class __EPEnvironment:
        def __init__(self, env: str, idd: str, idf: str, epw: str,
                     output: str = "", **kwargs):
            """
            Prepare the enssential environment for execution
            Except conifg, once the environment is created its properties
            cannot be changed.

            config can only be modified but not replaced.

            @param env:     energyplus install folder path.
            @param idd:     idd file path.
            @param idf:     idf file path.
            @param epw:     epw file path.
            @param output:  path for E+ output files.
            """

            self.env = env
            self.idd = idd
            self.idf = idf
            self.epw = epw
            self.output = output

        def check(self) -> bool:
            envcheck = EnvCheck(envpath=self.__env)
            return envcheck.check_health()

        @property
        def config(self):
            return self.__config

        @config.setter
        def config(self, value: Dict):
            tmp = Config()
            if value == {}:
                self.__config = tmp
            elif all(key in tmp.keys() for key in value):
                tmp.update(value)
                self.__config = tmp
            else:
                raise ValueError("Unsupported config argument")

        @property
        def is_created(self):
            return True

        @property
        def env(self):
            return self.__env

        @env.setter
        def env(self, value):
            """ check env before set it into config """
            if self.is_created:
                raise SetAfterCreateError
            if self.check():
                self.__env = value

        @property
        def output(self):
            """ if no output file is specified then create tmp folder """
            if not self.output:
                self.output = tempfile.TemporaryDirectory()
            return self.__output

        @output.setter
        def output(self, value):
            if self.is_created:
                raise SetAfterCreateError
            if not path.exists(value):
                with open(path.abspath(value), 'w'):
                    ...
            self.__output = value

        @property
        def idd(self):
            return self.__idd

        @idd.setter
        def idd(self, value):
            if self.is_created:
                raise SetAfterCreateError
            if not path.exists(value):
                raise FileExistsError("idd is not a real path")
            return self.idd

        @property
        def idf(self):
            return self.__idf

        @idf.setter
        def idf(self, value):
            if self.is_created:
                raise SetAfterCreateError
            if not path.exists(value):
                raise FileExistsError("idf is not a real path")
            return self.idf

        @property
        def epw(self):
            return self.__epw

        @epw.setter
        def epw(self, value):
            if self.is_created:
                raise SetAfterCreateError
            if not path.exists(value):
                raise FileExistsError("epw is npot a real path")
            return self.__epw

    instance = None

    def __init__(self, *args, **kwargs):
        if not type(self).instance:
            type(self).instance = type(self).EPEnvironment(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)


class Config(UserDict):
    """
    default config, it can be override at any time.
    Config includes extra energyplus argument flags.
    """

    def __init__(self):
        super().__init__()
        self['convert'] = False
        self['annual'] = False
        self['design_day'] = False
        self['expandobjects'] = False
        self['readvars'] = False
        self['output_prefix'] = ''
        self['output_sufix'] = ''

    def __setitem__(self, key, value):
        if key not in self.keys():
            raise KeyError("Config doesn't allow arbitrary keys.")
        super().__setitem__(key, value)
