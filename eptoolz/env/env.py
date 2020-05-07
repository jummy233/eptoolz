"""
Global config class
This class contains all the information about runtime
includes path to EnergyPlus, output path, E+ parameters etc.
"""
import tempfile
import os.path as path
from eptoolz.env.envcheck import EnvCheck
from eptoolz.exceptions import SetAfterCreateError
from typing import Dict, Optional, cast
import logging


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

            @param env:      energyplus install folder path.
            @param idd:      idd file path.
            @param idf:      idf file path.
            @param epw:      epw file path.
            @param output:   path for E+ output files.
            @param **kwargs: dictionary, used to initialize Config
            """

            self.env = env
            self.idd = idd
            self.idf = idf
            self.epw = epw
            self.output = output

        def check(self, env) -> bool:
            envcheck = EnvCheck(envpath=env)
            return envcheck.check_health()

        # properties below are readonly.
        @property
        def env(self):
            return self.__env

        @env.setter
        def env(self, value):
            """ check env before set it into config """
            if self.__dict__.get('__env'):
                raise SetAfterCreateError
            try:
                __import__('pdb').set_trace()
                if self.check(value):
                    self.__env = value
            except AttributeError as e:
                logging.error(e)
            except Exception as e:
                logging.error(e)

        @property
        def output(self):
            """ if no output file is specified then create tmp folder """
            if not self.__dict__.get('__output'):
                self.output = tempfile.TemporaryDirectory()
            return self.__output

        @output.setter
        def output(self, value):
            print("asd")
            if self.__dict__.get('__output'):
                raise SetAfterCreateError
            if isinstance(value, tempfile.TemporaryDirectory):
                self.__output = cast(tempfile.TemporaryDirectory, value).name
            elif isinstance(value, str) and not path.exists(value):
                with open(path.abspath(value), 'w'):
                    self.__output = value
            else:
                raise ValueError("Unexpected value for output.")

        @property
        def idd(self):
            return self.__idd

        @idd.setter
        def idd(self, value):
            if self.__dict__.get('__idd'):
                raise SetAfterCreateError
            if not path.exists(value):
                raise FileExistsError("idd is not a real path")
            self._idd = value

        @property
        def idf(self):
            return self.__idf

        @idf.setter
        def idf(self, value):
            if self.__dict__.get('__idf'):
                raise SetAfterCreateError
            if not path.exists(value):
                raise FileExistsError("idf is not a real path")
            self.__idf = value

        @property
        def epw(self):
            return self.__epw

        @epw.setter
        def epw(self, value):
            if self.__dict__.get('__epw'):
                raise SetAfterCreateError
            if not path.exists(value):
                raise FileExistsError("epw is npot a real path")
            self.__epw = value

    instance = None

    def __init__(self, *args, **kwargs):
        if not type(self).instance:
            type(self).instance = type(self).__EPEnvironment(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        setattr(self.instance, name, value)


