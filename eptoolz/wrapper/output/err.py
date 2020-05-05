"""
wrapper for .err output, provide in script error message.
"""
from eptoolz.env import EPEnvironment
from eptoolz.wrapper import EPWrapper


class EPErr(EPWrapper):

    def __init__(self, env: EPEnvironment):
        super().__init__(env)

    @staticmethod
    def parse(cls, path):
        ...

    @property
    def fatal(self):
        ...

    @property
    def severve(self):
        ...

    @property
    def warning(self):
        ...

    @property
    def information(self):
        ...

    @property
    def summary(self):
        ...
