from eptoolz.env import EPEnvironment
from eptoolz.wrapper import EPWrapper
from eptoolz.orm.epobject import EPObject
from collections import OrderedDict


class EPIdf(OrderedDict[str, EPObject], EPWrapper):

    def __init__(self, env: EPEnvironment = None):
        super().__init__()
        self.env = env

    @staticmethod
    def parse(self, path: str) -> 'EPIdf':
        ...


