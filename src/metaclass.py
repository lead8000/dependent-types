import re
from operators import AST, BitOr, Num, Lt, Gt, Le, Ge, Eq, Ne, Add, Sub, Mul, TrueDiv, FloorDiv, Mod, Pow, Constant

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

class Attr(AST):
    """
        Attribute node.
    """
    def __new__(self, cls, attr):
        #print(self, cls, attr)
        return super().__new__(self, f"{cls.__name__}_{attr}", (), {})

    def __init__(self, cls, attr):
        cls.attrs.append(self)
        self.cls = cls
        self.attr = attr

    def eval(self):
        return Constant(self.value)
    
    def __or__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return BitOr(self, other)
    
    def __eq__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Eq(self, other)
    
    def __ne__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Ne(self, other)
    
    def __lt__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Lt(self, other)
    
    def __gt__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Gt(self, other)
    
    def __le__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Le(self, other)
    
    def __ge__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Ge(self, other)
    
    def __add__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Add(self, other)
    
    def __sub__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Sub(self, other)
    
    def __mul__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Mul(self, other)
    
    def __truediv__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return TrueDiv(self, other)
    
    def __floordiv__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return FloorDiv(self, other)
    
    def __mod__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Mod(self, other)
    
    def __pow__(self, other: 'Attr') -> AST:
        if isinstance(other, (int, float)):
            other = Num(other)
        return Pow(self, other)
    
    def __radd__(self, other: 'Attr') -> AST:
        return self + other
    
    def __rsub__(self, other: 'Attr') -> AST:
        return self - other
    
    def __rmul__(self, other: 'Attr') -> AST:
        return self * other
    
    def __rtruediv__(self, other: 'Attr') -> AST:
        return self / other
    
    def __rfloordiv__(self, other: 'Attr') -> AST:
        return self // other
    
    def __rmod__(self, other: 'Attr') -> AST:
        return self % other
    
    def __rpow__(self, other: 'Attr') -> AST:
        return self ** other

# define an alias
Attribute = Attr

class Checkable(type):
    def __instancecheck__(self, __instance) -> bool:
        #print(f'\n\nCHECK INSTANCE\n\nPREDICATE = {self.predicate.left}\n\nINSTANCE = {__instance}\n\n')
        for dtype in self.dtypes:
            # #print(dtype.__dict__)
            dtype.value = __instance.__getattribute__(dtype.attr)
        #print(f'CHECK PREDICATE: {self.predicate} = {self.predicate.eval()}')
        predicate = self.predicate.eval()
        for dtype in self.dtypes:
            dtype.value = None
        return predicate

class Subcriptable(type):

    def __class_getitem__(self, cls, item):
        i = 0
        dtypes = []
        predicate = None
        #print('SUBCRITABLE')  

        while i < len(item) and isinstance(item[i], AST):
            if isinstance(item[i], BitOr):
                dtypes.append(item[i].left)
                predicate = item[i].right
            else: 
                dtypes.append(item[i])
            i += 1

        #print(f'\n\n000000000000AAAAAAAAAAAAAAAAAAAAAAAAAA \n{dtypes} \n{predicate.__dict__}')
        #print(predicate.left.__dict__)
        #print('\n\n')
        
        _dict = { k: v for k, v in cls.__dict__.items() }
        _dict['dtypes'] = dtypes
        _dict['predicate'] = predicate

        newcls = DependentType.__new__(self, self.__name__, (), _dict)
        #print(self,cls,item)
        #print(newcls.__dict__)
        return newcls

    def __getitem__(cls, item):
        return cls.__class_getitem__(cls, item)

class DependentType(Checkable,Subcriptable):
    def __new__(cls, name, *subclasses):
        return super().__new__(cls, name, *subclasses)
    
    def __init__(cls, name, *subclasses, **dict) -> None:
        # #print(cls, name, *subclasses, **dict)
        cls.attrs = []
        