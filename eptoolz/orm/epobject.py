from typing import Tuple, List, Dict
from inspect import Parameter, Signature, BoundArguments
from collections import OrderedDict
from eptoolz.orm.types import Field


class EPObjectMeta(type):
    """
    Magic class.
    """
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, clsname, bases, clsdict: OrderedDict):
        fields = [key for key, val in clsdict.items()
                  if isinstance(val, Field)]
        for name in fields:
            clsdict[name].name = name
        clsobj = super().__new__(cls, clsname, bases, dict(clsdict))
        sig = Signature([Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
                         for name in fields])
        setattr(clsobj, '__signature__', sig)
        return clsobj


class EPObject(metaclass=EPObjectMeta):
    """
    Python representation of Idf input objects.
    """

    def __init__(self, *args, **kwargs):
        bound: BoundArguments = self.__signature__.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            setattr(self, name, value)

    def __eq__(self, other) -> bool:
        """
        Two EPObject are equal if their has the same attributes and
        values of the attributes are the same.
        """
        return self.__dict__ == other.__dict__

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        try:
            name = getattr(self, 'name')
            return(f"<EPObject {name}>")
        except AttributeError:
            return("<Anynomous EPObject>")
