
from abc import abstractmethod

def visualizer(fn):
    def inner(*args):
        print('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(f'\nFUNCTION {fn.__name__.upper()}\n\n')
        print(f'ARGS:\n')
        for arg in args:
            print(f'TYPEOF({arg})={type(arg)}') 
            print(f'dict({arg})={arg.__dict__}\n')
        result = fn(*args)
        print(f'\n\nRESULT ==> {result}\n\n')
        print(f'\nENDED {fn.__name__.upper()}\n\n')
        return result
    return inner

class AST(type):
    @abstractmethod
    def eval(self):...

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
    def __add__(self, other):
        return Constant(self.value + other.value)
    @visualizer
    def __eq__(self, other) -> bool:
        print(self, other)
        return self.value == other.value
    

class Num(Constant):...

class Bool(Constant):...

class BinOp(AST):
    """
        Binary operator
    """
    def __new__(cls, *_):
        #print(f'\n{cls.__name__}_Node')
        return super().__new__(cls, f'{cls.__name__}_Node', (), {})

    def __init__(self, left, right):
        #print(f'\nINIT={self} LEFT={left} RIGHT={right}\n')
        self.left  = left
        self.right = right

class BitOr(BinOp):
    @visualizer
    def __eq__(self, other) -> AST:
        self.right = Eq(self.right, other)
        return self
    @visualizer
    def __ne__(self, other) -> AST:
        self.right = Ne(self.right, other)
        return self
    @visualizer
    def __lt__(self, other) -> AST:
        self.right = Lt(self.right, other)
        return self
    @visualizer
    def __gt__(self, other) -> AST:
        self.right = Gt(self.right, other)
        return self
    @visualizer
    def __le__(self, other) -> AST:
        self.right = Le(self.right, other)
        return self
    @visualizer
    def __ge__(self, other) -> AST:
        self.right = Ge(self.right, other)
        return self

class Lt(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() < self.right.eval()

class Gt(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() > self.right.eval()

class Le(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() <= self.right.eval()

class Ge(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() >= self.right.eval()

class Eq(BinOp):
    @visualizer
    def eval(self):
        print(f'LEFT: {self.left.eval()} RIGHT: {self.right.eval()}')
        return self.left.eval() == self.right.eval()

class Ne(BinOp):
    @visualizer
    def eval(self):
        #print(self.left, self.right)
        return self.left.eval() != self.right.eval()

class Add(BinOp):
    @visualizer
    def eval(self):
        print(f'LEFT: {self.left.eval()} RIGHT: {self.right.eval()}')
        return self.left.eval() + self.right.eval()

class Sub(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() - self.right.eval()

class Mul(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() * self.right.eval()

class TrueDiv(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() / self.right.eval()

class FloorDiv(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval // self.right.eval()

class Mod(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() % self.right.eval()
    
class Pow(BinOp):
    @visualizer
    def eval(self):
        return self.left.eval() ** self.right.eval()
