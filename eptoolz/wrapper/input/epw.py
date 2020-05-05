"""
Weather data
"""
from eptoolz.wrapper import EPWrapper
from eptoolz.env import EPEnvironment


class Epw(EPWrapper):

    def __init__(self, env: EPEnvironment):
        super().__init__(env)


