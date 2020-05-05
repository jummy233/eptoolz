"""
Global config class
This class contains all the information about runtime
includes path to EnergyPlus, output path, E+ parameters etc.
"""
import tempfile
from eptoolz.config.envcheck import EnvCheck


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
        def __init__(self, env: str, output: str = ""):
            """Create environment config
            and prepare for executation

            @param output:  path for E+ output files.
            @param env:     energyplus install folder path.
            """
            self.output = output
            self.env = env

        def check(self) -> bool:
            envcheck = EnvCheck(envpath=self.__env)
            return envcheck.check_health()

        @property
        def output(self):
            """ if no output file is specified then create tmp folder """
            if not self.output:
                self.output = tempfile.TemporaryDirectory()
            return self.__output

        @output.setter
        def output(self, value):
            self.__output = value

        @property
        def env(self):
            return self.__env

        @env.setter
        def env(self, value):
            """ check env before set it into config """
            if self.check():
                self.__env = value

    instance = None

    def __init__(self, *args, **kwargs):
        if not type(self).instance:
            type(self).instance = type(self).EPEnvironment(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)

