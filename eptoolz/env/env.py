"""
Global config class
This class contains all the information about runtime
includes path to EnergyPlus, output path, E+ parameters etc.
"""
import tempfile
import os.path as path
import sys
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

        def __init__(self, env: str, idf: str, epw: str,
                     output=None, idd=None,  **kwargs):
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

            sys.path.insert(1, env)  # add env to path.
            self.env = env
            self.idd = idd
            self.idf = idf
            self.epw = epw
            self.output = output

        def check(self, env) -> bool:
            envcheck = EnvCheck(envpath=env)
            return envcheck.check_health()

        # properties below are readonly.
        # property setters are only used in the constructor.
        # no properties are allowed to be set outside the class.
        @property
        def env(self):
            return self.__env

        @env.setter
        def env(self, value):
            """ check env before set it into config """
            try:
                if self.check(value):
                    self.__env = value
            except Exception as e:
                logging.error(e)

        @property
        def output(self):
            return self.__output

        @output.setter
        def output(self, value):
            """
            if no output path is defined then create a tempdir for output.
            """
            if '__output' in self.__dict__ and self.__output is None:
                tmp = tempfile.TemporaryDirectory()
                self.__output = tmp.name
                logging.warning("no output file is specified,"
                                + f" output will goes to {tmp.name}")
            elif isinstance(value, str) and not path.exists(value):
                with open(path.abspath(value), 'w'):
                    self.__output = value
            else:
                raise ValueError("Unexpected value for output.")

        @property
        def idd(self):
            """
            If no idd file specified use jdd comes with E+ installation
            by default.
            """
            if '__idd' in self.__dict__ and self.__idd is None:
                self.__idd = path.join(self.env, "Energy+.schema.epJson")
            return self.__idd

        @idd.setter
        def idd(self, value):
            if not path.exists(value):
                raise FileExistsError("idd is not a real path")
            self.__idd = value

        @property
        def idf(self):
            return self.__idf

        @idf.setter
        def idf(self, value):
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
                raise FileExistsError("epw is not a real path")
            self.__epw = value

    instance: Optional[__EPEnvironment] = None

    def __init__(self, *args, **kwargs):
        if not type(self).instance:
            type(self).instance = type(self).__EPEnvironment(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        raise SetAfterCreateError("environment is not settable")

    def __del__(self):
        if self.instance is not None and self.instance.env in sys.path:
            sys.path.remove(self.instance.env)
