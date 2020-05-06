"""
wrappers for energy plus input and out put file
Each wrapper will read the file path from the env,
and create corresponding python object for easier access.
"""
from abc import ABC, abstractmethod


class EPWrapper(ABC):

    @abstractmethod
    @staticmethod
    def parse(cls, path) -> 'EPWrapper':
        """
        Parse the raw txt file into wrapper object
        """


