from .generic import GenericVisitor, visualizer
from dtypes.ranges import Range, RangeSet
from copy import deepcopy
from dtypes.ast import Attr, Constant
from sys import maxsize as oo

class CheckTypeComposition(GenericVisitor):

    @visualizer()
    def visit(self, dtype, ctx={}):
        return super().visit(dtype, ctx)

    def visit_Gt(self, dtype, ctx = {}):

        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):

            ctx_copy = deepcopy(ctx)
            if dtype.left.attr not in ctx_copy['vars']:
                ctx_copy['vars'][dtype.left.attr] = f'var_{len(ctx_copy["vars"])}'

            var = ctx_copy['vars'][dtype.left.attr]
            ctx_copy['ranges'][var] = Range(dtype.right.value, oo, include_start=False)
            
            return ctx_copy

    # def visit_Or(self, dtype, ctx = {}):
    #     ...

    # def visit_Lt(self, dtype, ctx = {}):
    #     ...

    # def visit_Attr(self, dtype, ctx = {}):
    #     ...

    # def visit_Mul(self, dtype, ctx = {}):
    #     ...

    # def visit_And(self, dtype, ctx = {}):
    #     ...

    # def visit_Ne(self, dtype, ctx = {}):
    #     ...
