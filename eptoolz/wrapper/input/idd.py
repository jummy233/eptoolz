from eptoolz.env import EPEnvironment
from eptoolz.wrapper import EPWrapper


class EPIdd(EPWrapper):

    def __init__(self, env: EPEnvironment):
        self.env = env

    @staticmethod
    def parse(cls, path: str) -> 'EPIdd':
        ...

