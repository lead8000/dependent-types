from .base import AST, visualizer
from .operators import BitOr, Add, Sub, Mul, TrueDiv, FloorDiv, Eq, Ne, Lt, Le, Gt, Ge, Mod, Pow

class Constant(AST):
    """
        Constant node.
    """
    def __new__(self, literal):
        return super().__new__(self, f'Constant_{literal}', (), {'value': literal})
    @visualizer
    def eval(self):
        return self
    @visualizer
    def __add__(self, other: 'Constant') -> 'Constant':
        return Constant(self.value + other.value)
    @visualizer
    def __sub__(self, other: 'Constant') -> 'Constant':
        return Constant(self.value - other.value)
    @visualizer
    def __mul__(self, other: 'Constant') -> 'Constant':
        return Constant(self.value * other.value)
    @visualizer
    def __truediv__(self, other: 'Constant') -> 'Constant':
        return Constant(self.value / other.value)
    @visualizer
    def __floordiv__(self, other: 'Constant') -> 'Constant':
        return Constant(self.value // other.value)
    @visualizer
    def __mod__(self, other: 'Constant') -> 'Constant':
        return Constant(self.value % other.value)
    @visualizer
    def __pow__(self, other: 'Constant') -> 'Constant':
        return Constant(self.value ** other.value)
    @visualizer
    def __eq__(self, other: 'Constant') -> bool:
        #print(self, other)
        return self.value == other.value
    @visualizer
    def __ne__(self, other: 'Constant') -> bool:
        return self.value != other.value
    @visualizer
    def __lt__(self, other: 'Constant') -> bool:
        return self.value < other.value
    @visualizer
    def __gt__(self, other: 'Constant') -> bool:
        #print(self, other)
        return self.value > other.value
    @visualizer
    def __le__(self, other: 'Constant') -> bool:
        return self.value <= other.value
    @visualizer
    def __ge__(self, other: 'Constant') -> AST:
        return self.value >= other.value

class Num(Constant):...

class Bool(Constant):...

class Attr(AST):
    """
        Attribute node.
    """
    def __new__(self, attr):
        return super().__new__(self, f"Attr_{attr}", (), {})

    def __init__(self, attr):
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
        #print('YYYYYYYYEEEEEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSSS')
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

class AttrVar(AST):
    """
        Attribute node.
    """
    def __new__(self, name):
        return super().__new__(self, f"AttrVar_{name}", (), {})

    def __init__(self, name):
        self.name = name
