
from abc import abstractmethod


class AST(type):...


class BinOp(AST):
    """
        Binary operator
    """
    def __new__(cls, left, right):
        print(f'\n{cls.__name__}_Node')
        return super().__new__(cls, f'{cls.__name__}_Node', (), {})

    def __init__(self, left, right):
        print(f'\nINIT={self} LEFT={left} RIGHT={right}\n')
        self.left  = left
        self.right = right

    @abstractmethod
    def eval(self):...

class BitOr(BinOp):
    
    def __lt__(self, other) -> AST:
        self.right = Lt(self.right, other)
        return self

    def __gt__(self, other) -> AST:
        self.right = Gt(self.right, other)
        return self

class Lt(BinOp):
    def eval(self):
        return self.left.value < self.right.value

class Gt(BinOp):
    def eval(self):
        return self.left.value > self.right.value

class Le(BinOp):...

class Ge(BinOp):...

class Eq(BinOp):...

class Ne(BinOp):...

class Add(BinOp):...

class Sub(BinOp):...

class Mul(BinOp):...

class TrueDiv(BinOp):...

class FloorDiv(BinOp):...

class Mod(BinOp):...
    
class Pow(BinOp):...
