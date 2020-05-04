from typing import Tuple, List, Dict
from collections import OrderedDict


class Field:
    """
    attributes for IdfObject fields
    """

    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        pass

    def __delete__(self, instance):
        pass


class IdfObjectMeta(type):
    """
    Magic class.
    """
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, bases, clsdict: Dict):
        ...


class IdfObject(metaclass=IdfObjectMeta):
    """
    Python representation of Idf input objects.
    """

    def __init__(self):
        ...

    def __str__(self):
        ...

    def __repr__(self):
        ...

