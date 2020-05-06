from __future__ import annotations
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from eptoolz.orm.epobject import EPObject


class Field:
    """
    attribute descriptor for IdfObject fields
    """

    def __init__(self, name=None):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("trying to delete a field from an EPObject")


class Typed(Field):
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError(f"Expected {self.ty}")
        super().__set__(instance, value)


class Integer(Typed):
    ty = int


class Real(Typed):
    ty = float


class Alpha(Typed):
    ty = str


class Choice(Alpha):
    def __init__(self, *args, choices: List[str], **kwargs):
        self.choices = choices
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if value not in self.choices:
            raise ValueError(f"{value} is not an option")
        super().__set__(instance, value)


class ObjectList(Typed):

    def __init__(self, *args, objects: List[EPObject], **kwargs):
        self.objects = objects
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if value not in self.objects:
            raise ValueError("paramter not in object list")
        super().__set__(instance, value)


class ExternalList(Typed):
    def __init__(self, *args, external: str, **kwargs):
        ...

    def __set__(self, instance, value):
        ...


