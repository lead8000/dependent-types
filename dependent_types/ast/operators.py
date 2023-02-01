from .base import AST
import dependent_types.ast as ast

class BinOp(AST):
    """
        Binary operator
    """
    def __new__(cls, right, left, **dict):
        name = f'{cls.__name__}_Node'
        return super().__new__(cls, name, right=right, left=left, **dict)

    def __init__(self, left, right):
        self.left = left
        self.right = right

class BitOr(BinOp):

    def __eq__(self, other) -> AST:
        self.right = Eq(self.right, other)
        return self

    def __ne__(self, other) -> AST:
        self.right = Ne(self.right, other)
        return self

    def __lt__(self, other) -> AST:
        self.right = Lt(self.right, other)
        return self

    def __gt__(self, other) -> AST:
        self.right = Gt(self.right, other)
        return self

    def __le__(self, other) -> AST:
        self.right = Le(self.right, other)
        return self

    def __ge__(self, other) -> AST:
        self.right = Ge(self.right, other)
        return self

    def __and__(self, other) -> AST:
        self.right = And(self.right, other)
        return self

class And(BinOp):

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)
    
    def __ror__(self, other):
        return Or(self, other)

class Or(BinOp):

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __ror__(self, other):
        if isinstance(other, (int, float)):
            other = ast.Constant(other)
            return BitOr(other, self)

class Statement(BinOp):
    """
        Binary operator for declaring truth values.
    """

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __ror__(self, other):
        if isinstance(other, (int, float)):
            other = ast.Constant(other)
        return BitOr(other, self)

class Lt(Statement):...

class Gt(Statement):...

class Le(Statement):... 

class Ge(Statement):...

class Eq(Statement):...

class Ne(Statement):...

class Add(BinOp):...

class Sub(BinOp):...

class Mul(BinOp):...

class TrueDiv(BinOp):...

class FloorDiv(BinOp):...

class Mod(BinOp):...

class Pow(BinOp):...
