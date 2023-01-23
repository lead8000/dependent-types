import re
from types import UnionType

def axiom(func):
    func.__is_axiom__ = True
    return func


class LengthVar(type):

    def __new__(cls, name):
        return super().__new__(cls, name, (), {})

    def __add__(self, other):

        if isinstance(other, int):
            other = LengthVar(str(other))

        x = self.__name__.split('+') + other.__name__.split('+')		

        sum = 0
        vars = []

        for i in x:
            if re.match(r'[0-9]+', i):
                sum += int(i)
            else:
                vars.append(i)

        if len(vars) == 0:
            return LengthVar(str(sum))

        vars = sorted(vars)
        vars = '+'.join(vars)

        if sum != 0:
            vars += '+' + str(sum)

        return LengthVar(vars)

    def __eq__(self, other):
        return self.__name__ == other.__name__


class Predicate(type):

    def __new__(cls, predicate):
        return super().__new__(cls, "Predicate", (), { 
            '__call__': predicate
        })

    def __call__(self, *args, **kwds):
        return self.__call__(*args, **kwds)


class Attribute(type):

    def __new__(self, cls, attr):
        return super().__new__(self, f"{cls.__name__}_{attr}", (), {})

    def __init__(self, cls, attr):
        self.cls = cls
        self.attr = attr

    def __eq__(self, other: 'Attribute') -> bool:
        print(self.attr_value, other.attr_value)
        return self.attr_value == other.attr_value

    def __ne__(self, other: 'Attribute') -> bool:
        return self.attr_value != other.attr_value

    def __lt__(self, other: 'Attribute') -> bool:
        return self.attr_value < other.attr_value

    def __gt__(self, other: 'Attribute') -> bool:
        return self.attr_value > other.attr_value

    def __le__(self, other: 'Attribute') -> bool:
        return self.attr_value <= other.attr_value

    def __ge__(self, other: 'Attribute') -> bool:
        return self.attr_value >= other.attr_value

    def __add__(self, other) -> bool:
        if isinstance(other, Attribute):
            self.attr_value += other.attr_value
        elif isinstance(other, int):
            self.attr_value += other
        return self

    def __sub__(self, other) -> bool:
        if isinstance(other, Attribute):
            self.attr_value -= other.attr_value
        elif isinstance(other, int):
            self.attr_value -= other
        return self

    def __mul__(self, other) -> bool:
        if isinstance(other, Attribute):
            self.attr_value *= other.attr_value
        elif isinstance(other, int):
            self.attr_value *= other
        return self

    def __truediv__(self, other) -> bool:
        if isinstance(other, Attribute):
            self.attr_value /= other.attr_value
        elif isinstance(other, int):
            self.attr_value /= other
        return self

    def __floordiv__(self, other) -> bool:
        if isinstance(other, Attribute):
            self.attr_value //= other.attr_value
        elif isinstance(other, int):
            self.attr_value //= other
        return self

    def __mod__(self, other) -> bool:
        if isinstance(other, Attribute):
            self.attr_value %= other.attr_value
        elif isinstance(other, int):
            self.attr_value %= other
        return self

    def __pow__(self, other) -> bool:
        if isinstance(other, Attribute):
            self.attr_value **= other.attr_value
        elif isinstance(other, int):
            self.attr_value **= other
        return self


class Checkable(type):
    def __instancecheck__(self, __instance) -> bool:
        for dtype in self.dtypes:
            dtype.attr_value = __instance.__getattribute__(dtype.attr)
        predicate = self.predicate()
        dtype.attr_value = None
        return predicate


class Subcriptable(type):    

    def __class_getitem__(cls, item):
        i = 0
        dtypes = []
        predicate = None      
        while isinstance(item[i], Attribute):
            dtypes.append(item[i])
            i += 1
        else:
            if isinstance(item[i], UnionType):
                if isinstance(item[i].__args__[0], Attribute) \
                    and isinstance(item[i].__args__[1], Predicate):
                    dtypes.append(item[i].__args__[0])
                    predicate = item[i].__args__[1]

        newcls = DependentType.__new__(cls, cls.__name__, (), {
            'dtypes': dtypes,
            'predicate': predicate
        })

        return newcls


class DependentType(Checkable,Subcriptable):
    def __new__(cls, name, *subclasses):
        return super().__new__(cls, name, *subclasses)

