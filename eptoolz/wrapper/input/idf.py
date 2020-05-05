from eptoolz.env import EPEnvironment
from eptoolz.wrapper import EPWrapper
from eptoolz.orm.epobject import EPObject


class EPIdf(EPWrapper):

    def __init__(self, env: EPEnvironment = None):
        super().__init__(env)

    @staticmethod
    def parse(self, path: str) -> 'EPIdf':
        ...

    def add(self, obj: EPObject):
        ...

    def write(self, path):
        ...


env = Env(env, output)
idf = EPIdf(env)

with EPIdf(env) as idf:
    ow1 = WinObject(xx, xx, xx)
    ow2 = WinObject(xx, xx, xx)
    idf.add(ow1)
    idf.add(ow2)








