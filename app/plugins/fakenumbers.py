#!/usr/bin/python
# =======================================
#
#  File Name :
#
#  Purpose :
#
#  Creation Date : 30-03-2016
#
#  Last Modified : Thu 05 Jan 2017 03:57:45 PM CST
#
#  Created By : Brian Auron
#
# ========================================

class NoNumberError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class NumberString(object):
    @classmethod
    def from_str(cls, s):
        for i in [IntString, BinString, HexString, FloatString]:
            try:
                _ = i(s).num
                return i(s)
            except ValueError:
                continue
        raise NoNumberError()

class IntString(object):
    def __init__(self, s):
        self._str = s
        self._num = None
        self._base = 10
        self._tonum = int
        self._tostr = str

    def __add__(self, x):
        return self.__class__(str(self.num + x))

    def __sub__(self, x):
        return self.__class__(str(self.num - x))

    def __iadd__(self, x):
        self.num += x
        return self

    def __isub__(self, x):
        self.num -= x
        return self


    def __repr__(self):
        return self._tostr(self.num)

    def __str__(self):
        return self._tostr(self.num)

    @property
    def num(self):
        if not self._num:
            self._num = self._tonum(self._str, self._base)
        return self._num

    @num.setter
    def num(self, x):
        self._num = x
        return self.num

    @property
    def str(self):
        return self._tostr(self.num)

class BinString(IntString):
    def __init__(self, s):
        super(BinString, self).__init__(s)
        try:
            assert s.startswith('0b')
        except AssertionError:
            raise ValueError()
        self._base = 2
        self._tostr = bin

class HexString(IntString):
    def __init__(self, s):
        super(HexString, self).__init__(s)
        try:
            assert s.startswith('0x')
        except AssertionError:
            raise ValueError()
        self._base = 16
        self._tostr = hex

class FloatString(IntString):
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
