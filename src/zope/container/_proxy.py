##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

# This is very similar to the code in zope.proxy.__init__, but modified
# to work properly when extending Persistent.

import operator
import sys

from zope.proxy import PyNonOverridable

_MARKER = object()

from persistent import Persistent


def _special_name(name):
    "attribute names we delegate to super for"
    return (name.startswith('_Persistent')
            or name.startswith('_p_')
            or name.startswith('_v_')
            or name in PyContainedProxyBase.__slots__)


class PyContainedProxyBase(Persistent):
    """Persistent proxy
    """
    __slots__ = ('_wrapped', '__parent__', '__name__')

    def __new__(cls, obj):
        inst = Persistent.__new__(cls)
        inst._wrapped = obj
        inst.__parent__ = None
        inst.__name__ = None
        inst._Persistent__flags = None
        return inst

    def __init__(self, obj):
        self._wrapped = obj
        self.__parent__ = None
        self.__name__ = None
        self._Persistent__flags = None

    def __call__(self, *args, **kw):
        return self._wrapped(*args, **kw)

    def __repr__(self):
        return repr(self._wrapped)

    def __str__(self):
        return str(self._wrapped)

    def __unicode__(self):
        return unicode(self._wrapped)

    def __reduce__(self):
        return (type(self),
                (self._wrapped,),
                (self.__parent__, self.__name__))

    def __reduce_ex__(self, protocol):
        return self.__reduce__()

    def __setstate__(self, state):
        before = self._Persistent__flags
        self.__parent__ = state[0]
        self.__name__ = state[1]
        # The C implementation doesn't set itself to changed
        # when the state is loaded from the database,
        # we take care to copy that behaviour
        self._Persistent__flags = before

    def __getstate__(self):
        return (self.__parent__, self.__name__)

    def __getnewargs__(self):
        return self._wrapped,

    def _p_invalidate(self):
        # The superclass wants to clear the __dict__, which
        # we don't have, but we would otherwise delegate
        # to the wrapped object, which is clearly wrong in this case.
        # This method is a copy of the super method with
        # clearing the dict omitted
        if self._Persistent__jar is not None:
            if self._Persistent__flags is not None:
                self._Persistent__flags = None
            try:
                object.__getattribute__(self, '__dict__').clear()
            except AttributeError:
                pass

    def _p_accessed(self):
        # The superclass has issues changing the MRU
        # during initial serialization because we're not
        # yet in the picklecache
        try:
            Persistent._p_accessed(self)
        except KeyError:
            pass

    # Rich comparison protocol
    def __lt__(self, other):
        return self._wrapped < other

    def __le__(self, other):
        return self._wrapped <= other

    def __eq__(self, other):
        return self._wrapped == other

    def __ne__(self, other):
        return self._wrapped != other

    def __gt__(self, other):
        return self._wrapped > other

    def __ge__(self, other):
        return self._wrapped >= other

    def __nonzero__(self):
        return bool(self._wrapped)
    __bool__ = __nonzero__  # Python3 compat

    def __hash__(self):
        return hash(self._wrapped)

    # Attribute protocol
    def __getattribute__(self, name):
        if _special_name(name):
            return super(PyContainedProxyBase, self).__getattribute__(name)

        if name in ('__reduce__', '__reduce_ex__', '__getstate__', '__setstate__', '__getnewargs__'):
            return object.__getattribute__(self, name)

        # Only access this if we need it, otherwise persistence problems
        if name == '_wrapped':
            return super(PyContainedProxyBase, self).__getattribute__('_wrapped')

        try:
            mine = super(PyContainedProxyBase, self).__getattribute__(name)
        except AttributeError:
            mine = _MARKER
        else:  # pragma NO COVER PyPy
            # PyPy returns non-slot attributes for some reason, so we have to
            # doctor things up a bit.
            # if (PYPY and
            #	name in ('__providedBy__', '__provides__', '__implemented__')):
            #	mine = _MARKER
            if isinstance(mine, PyNonOverridable):
                return mine.desc.__get__(self)
        try:
            try:
                wrapped = super(PyContainedProxyBase, self).__getattribute__('_wrapped')
            except KeyError:
                # During commit time of a persistent transaction, we can
                # be in the state where we have an oid, but we are not actually
                # in the picklecache yet. This causes a KeyError when the superclass
                # tries to use _p_accessed; fortunately, it's ignorable as we
                # know we are active
                wrapped = object.__getattribute__(self, '_wrapped')
            return getattr(wrapped, name)
        except AttributeError:
            if mine is not _MARKER:
                return mine
            raise

    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        if _special_name(name):
            return super(PyContainedProxyBase, self).__setattr__(name, value)
        try:
            super(PyContainedProxyBase, self).__getattribute__(name)
        except AttributeError:
            return setattr(self._wrapped, name, value)
        else:
            return super(PyContainedProxyBase, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name in PyContainedProxyBase.__slots__:
            raise AttributeError()
        delattr(self._wrapped, name)

    # Container protocols

    def __len__(self):
        return len(self._wrapped)

    def __getitem__(self, key):
        if isinstance(key, slice):
            if isinstance(self._wrapped, (list, tuple)):
                return self._wrapped[key]
            start, stop = key.start, key.stop
            if start is None:
                start = 0
            if start < 0:
                start += len(self._wrapped)
            if stop is None:
                stop = sys.maxint
            if stop < 0:
                stop += len(self._wrapped)
            return operator.getslice(self._wrapped, start, stop)
        return self._wrapped[key]

    def __setitem__(self, key, value):
        self._wrapped[key] = value

    def __delitem__(self, key):
        del self._wrapped[key]

    def __iter__(self):
        # This handles a custom __iter__ and generator support at the same
        # time.
        return iter(self._wrapped)

    def next(self):
        # Called when we wrap an iterator itself.
        return self._wrapped.next()

    def __next__(self):  # pragma NO COVER Python3
        return self._wrapped.__next__()

    # Python 2.7 won't let the C wrapper support __reversed__ :(
    # def __reversed__(self):
    #	 return reversed(self._wrapped)

    def __contains__(self, item):
        return item in self._wrapped

    # Numeric protocol:	 unary operators
    def __neg__(self):
        return -self._wrapped

    def __pos__(self):
        return +self._wrapped

    def __abs__(self):
        return abs(self._wrapped)

    def __invert__(self):
        return ~self._wrapped

    # Numeric protocol:	 unary conversions
    def __complex__(self):
        return complex(self._wrapped)

    def __int__(self):
        return int(self._wrapped)

    def __long__(self):
        return long(self._wrapped)

    def __float__(self):
        return float(self._wrapped)

    def __oct__(self):
        return oct(self._wrapped)

    def __hex__(self):
        return hex(self._wrapped)

    def __index__(self):
        return operator.index(self._wrapped)

    # Numeric protocol:	 binary coercion
    def __coerce__(self, other):
        left, right = coerce(self._wrapped, other)
        if left == self._wrapped and type(left) is type(self._wrapped):
            left = self
        return left, right

    # Numeric protocol:	 binary arithmetic operators
    def __add__(self, other):
        return self._wrapped + other

    def __sub__(self, other):
        return self._wrapped - other

    def __mul__(self, other):
        return self._wrapped * other

    def __floordiv__(self, other):
        return self._wrapped // other

    def __truediv__(self, other):  # pragma NO COVER
        # Only one of __truediv__ and __div__ is meaningful at any one time.
        return self._wrapped / other

    def __div__(self, other):  # pragma NO COVER
        # Only one of __truediv__ and __div__ is meaningful at any one time.
        return self._wrapped / other

    def __mod__(self, other):
        return self._wrapped % other

    def __divmod__(self, other):
        return divmod(self._wrapped, other)

    def __pow__(self, other, modulus=None):
        if modulus is None:
            return pow(self._wrapped, other)
        return pow(self._wrapped, other, modulus)

    def __radd__(self, other):
        return other + self._wrapped

    def __rsub__(self, other):
        return other - self._wrapped

    def __rmul__(self, other):
        return other * self._wrapped

    def __rfloordiv__(self, other):
        return other // self._wrapped

    def __rtruediv__(self, other):  # pragma NO COVER
        # Only one of __rtruediv__ and __rdiv__ is meaningful at any one time.
        return other / self._wrapped

    def __rdiv__(self, other):  # pragma NO COVER
        # Only one of __rtruediv__ and __rdiv__ is meaningful at any one time.
        return other / self._wrapped

    def __rmod__(self, other):
        return other % self._wrapped

    def __rdivmod__(self, other):
        return divmod(other, self._wrapped)

    def __rpow__(self, other, modulus=None):
        if modulus is None:
            return pow(other, self._wrapped)
        # We can't actually get here, because we can't lie about our type()
        return pow(other, self._wrapped, modulus)  # pragma NO COVER

    # Numeric protocol:	 binary bitwise operators
    def __lshift__(self, other):
        return self._wrapped << other

    def __rshift__(self, other):
        return self._wrapped >> other

    def __and__(self, other):
        return self._wrapped & other

    def __xor__(self, other):
        return self._wrapped ^ other

    def __or__(self, other):
        return self._wrapped | other

    def __rlshift__(self, other):
        return other << self._wrapped

    def __rrshift__(self, other):
        return other >> self._wrapped

    def __rand__(self, other):
        return other & self._wrapped

    def __rxor__(self, other):
        return other ^ self._wrapped

    def __ror__(self, other):
        return other | self._wrapped

    # Numeric protocol:	 binary in-place operators
    def __iadd__(self, other):
        self._wrapped += other
        return self

    def __isub__(self, other):
        self._wrapped -= other
        return self

    def __imul__(self, other):
        self._wrapped *= other
        return self

    def __idiv__(self, other):  # pragma NO COVER
        # Only one of __itruediv__ and __idiv__ is meaningful at any one time.
        self._wrapped /= other
        return self

    def __itruediv__(self, other):  # pragma NO COVER
        # Only one of __itruediv__ and __idiv__ is meaningful at any one time.
        self._wrapped /= other
        return self

    def __ifloordiv__(self, other):
        self._wrapped //= other
        return self

    def __imod__(self, other):
        self._wrapped %= other
        return self

    def __ilshift__(self, other):
        self._wrapped <<= other
        return self

    def __irshift__(self, other):
        self._wrapped >>= other
        return self

    def __iand__(self, other):
        self._wrapped &= other
        return self

    def __ixor__(self, other):
        self._wrapped ^= other
        return self

    def __ior__(self, other):
        self._wrapped |= other
        return self

    def __ipow__(self, other, modulus=None):
        if modulus is None:
            self._wrapped **= other
        else:  # pragma NO COVER
            # There is no syntax which triggers in-place pow w/ modulus
            self._wrapped = pow(self._wrapped, other, modulus)
        return self


def py_getProxiedObject(obj):
    if isinstance(obj, PyContainedProxyBase):
        return obj._wrapped
    return obj


def py_setProxiedObject(obj, new_value):
    if not isinstance(obj, PyContainedProxyBase):
        raise TypeError('Not a proxy')
    old, obj._wrapped = obj._wrapped, new_value
    return old
