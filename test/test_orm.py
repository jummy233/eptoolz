from unittest import TestCase

from eptoolz.orm.epobject import EPObject
from eptoolz.orm.types import (Alpha, Choice, Field, Integer, ObjectList, Real,
                               Typed)


class TestBasicType(TestCase):
    """ the descriptor _ should set variable bar in obj dict """
    def test_field(self):
        class Foo:
            _ = Field('bar')
        foo = Foo()
        foo._ = 'value'
        self.assertTrue(foo.__dict__['bar'] == 'value')

    def test_typed(self):
        class Foo:
            _ = Typed('bar')
        foo = Foo()
        foo._ = 'value'
        self.assertTrue(foo.__dict__['bar'] == 'value')

    def test_basic_types(self):
        class Foo:
            _1 = Integer('t1')
            _2 = Real('t2')
            _3 = Alpha('t3')
        foo = Foo()
        foo._1 = 1
        foo._2 = 1.0
        foo._3 = 'a'
        self.assertTrue(foo.t1 == 1 and foo.t2 == 1.0 and foo.t3 == 'a')

        with self.assertRaises(TypeError):
            foo._1 = 'str'
        with self.assertRaises(TypeError):
            foo._2 = 'str'
        with self.assertRaises(TypeError):
            foo._3 = 1


class TestEPObejectBasic(TestCase):
    class Foo(EPObject):
        name = Alpha()
        num1 = Integer()
        num2 = Real()

    def test_create_raise(self):

        foo = type(self).Foo(name='somename', num1=1, num2=1.0)
        with self.assertRaises(TypeError):
            foo.name = 1
        with self.assertRaises(TypeError):
            foo.num1 = 'str'
        with self.assertRaises(TypeError):
            foo.num2 = 'str'

    def test_create(self):
        foo = type(self).Foo(name='somename', num1=1, num2=1.0)
        foo.name = "good"
        foo.num1 = 1
        foo.num2 = 1.0
        self.assertTrue(
            foo.name == "good" and foo.num1 == 1 and foo.num2 == 1.0)


class TestCompoundType(TestCase):
    def test_choice(self):
        choices = ["Rought", "Smooth"]

        class Foo(EPObject):
            surface = Choice(choices=choices)

        foo = Foo(surface="Smooth")
        self.assertTrue(foo.surface == "Smooth")

        with self.assertRaises(ValueError):
            foo.surface = "Not in the List Element"

    def test_object_list(self):
        class Foo1(EPObject):
            name = Alpha()

        class Foo2(EPObject):
            num1 = Integer()

        foo1 = Foo1(name="name")
        foo2 = Foo2(num1=2)
        foo1 == foo2
        objlist = [Foo1(name="name"), Foo2(num1=1)]

        class Foo(EPObject):
            ref = ObjectList(objects=objlist)

        foo = Foo(ref=Foo2(num1=1))
        with self.assertRaises(ValueError):
            foo.ref = Foo2(num1=10)

