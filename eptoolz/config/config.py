"""
Global config class
This class contains all the information about runtime
includes path to EnergyPlus, output path, E+ parameters etc.
"""
import tempfile
from eptoolz.config.envcheck import EnvCheck


class EPConfig:

    def __init__(self, output: str, env: str):
        """Create environment config
        and prepare for executation

        @param output:  output file path
        @param env:  energyplus install folder path

        """
        self.output = output
        self.env = env
        self.check()

    def check(self) -> bool:
        envcheck = EnvCheck(envpath=self.__env)
        return envcheck.check_health()

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    @property
    def env(self):
        return self.__env

    @env.setter
    def env(self, value):
        if self.check():
            self.__env = value

