#!/usr/bin/python
""" Module for representing other bases of numbers as strings and vice versa
"""

class NoNumberError(Exception):
    """ Custom exception
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

# pylint: disable=too-few-public-methods
class NumberString:
    """ Abstract way to use any fake number
    """
    @classmethod
    def from_str(cls, numstr):
        """ Create a fake number instance from a string
        """
        for i in [IntString, BinString, HexString, FloatString]:
            try:
                _ = i(numstr).num
                return i(numstr)
            except ValueError:
                continue
        raise NoNumberError()

class IntString:
    """ Integer variante of a number string
    """
    def __init__(self, s):
        self._str = s
        self._num = None
        self._base = 10
        self._tonum = int
        self._tostr = str

    def __add__(self, other):
        return self.__class__(str(self.num + other))

    def __sub__(self, other):
        return self.__class__(str(self.num - other))

    def __iadd__(self, other):
        self.num += other
        return self

    def __isub__(self, other):
        self.num -= other
        return self

    def __repr__(self):
        return self._tostr(self.num)

    def __str__(self):
        return self._tostr(self.num)

    @property
    def num(self):
        """ Propertize num
        """
        if not self._num:
            self._num = self._tonum(self._str, self._base)
        return self._num

    @num.setter
    def num(self, newnum):
        """ Override num
        """
        self._num = newnum
        return self.num

    @property
    def str(self):
        """ Create string property
        """
        return self._tostr(self.num)

class BinString(IntString):
    """ Binary variant of a number string
    """
    def __init__(self, s):
        super(BinString, self).__init__(s)
        try:
            assert s.startswith('0b')
        except AssertionError:
            raise ValueError()
        self._base = 2
        self._tostr = bin

class HexString(IntString):
    """ Hex variant of a number string
    """
    def __init__(self, s):
        super(HexString, self).__init__(s)
        try:
            assert s.startswith('0x')
        except AssertionError:
            raise ValueError()
        self._base = 16
        self._tostr = hex

class FloatString(IntString):
    """ Float variant of a number string
    """
    def __init__(self, s):
        super(FloatString, self).__init__(s)
        self._tonum = float

    @property
    def num(self):
        if not self._num:
            self._num = self._tonum(self._str)
        return self._num

    @num.setter
    def num(self, x):
        self._num = x
        return self.num
