from .generic import GenericVisitor
from dependent_types.ranges import RangeSet
from dependent_types.utils import Contraints, AttributeDict
from copy import deepcopy
from dependent_types.ast import Attr, Constant, Eq, Ne, Lt, Gt, Le, Ge, Or, And
from sys import maxsize as oo


class TypeInference(GenericVisitor):

    # @visualizer(True)
    def visit(self, dtype, ctx={}):
        return super().visit(dtype, ctx)

    def visit_Gt(self, dtype, ctx = {}):

        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            attr, value = dtype.left.attr, dtype.right.value
            attrDict = AttributeDict()
            attrDict[attr] = RangeSet(f'({value}, {oo})')
            ctx_copy['contraints'] = Contraints(attrDict)
            
            return ctx_copy

    def visit_Lt(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            attr, value = dtype.left.attr, dtype.right.value
            attrDict = AttributeDict()
            attrDict[attr] = RangeSet(f'({-oo}, {value})')
            ctx_copy['contraints'] = Contraints(attrDict)

            return ctx_copy

    def visit_Ge(self, dtype, ctx = {}):

        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            attr, value = dtype.left.attr, dtype.right.value
            attrDict = AttributeDict()
            attrDict[attr] = RangeSet(f'[{value},{oo})')
            ctx_copy['contraints'] = Contraints(attrDict)

            return ctx_copy

    def visit_Le(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            attr, value = dtype.left.attr, dtype.right.value
            attrDict = AttributeDict()
            attrDict[attr] = RangeSet(f'({-oo},{value}]')
            ctx_copy['contraints'] = Contraints(attrDict)
           
            return ctx_copy

    def visit_Eq(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            attr, value = dtype.left.attr, dtype.right.value
            attrDict = AttributeDict()
            attrDict[attr] = RangeSet(f'[{value}, {value}]')
            ctx_copy['contraints'] = Contraints(attrDict)
                      
            return ctx_copy

    def visit_Ne(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            attr, value = dtype.left.attr, dtype.right.value
            attrDict = AttributeDict()
            attrDict[attr] = RangeSet(f"({-oo},{value})",f"({value},{oo})")
            ctx_copy['contraints'] = Contraints(attrDict)

            return ctx_copy    

    def visit_Or(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, (Attr, Eq, Ne, Lt, Gt, Le, Ge, Or, And)) \
        and isinstance(dtype.right, (Attr, Eq, Ne, Lt, Gt, Le, Ge, Or, And)):
            ctx_copy  = deepcopy(ctx)
            
            ctx_left = self.visit(dtype.left, ctx_copy)
            ctx_right = self.visit(dtype.right, ctx_copy)
            
            ctx_copy['contraints']  = (ctx_left['contraints'] | ctx_right['contraints'])

            return ctx_copy

    def visit_And(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, (Attr, Eq, Ne, Lt, Gt, Le, Ge, Or, And)) \
        and isinstance(dtype.right, (Attr, Eq, Ne, Lt, Gt, Le, Ge, Or, And)):
            ctx_copy  = deepcopy(ctx)
            
            ctx_left  = self.visit(dtype.left, ctx_copy)
            ctx_right = self.visit(dtype.right, ctx_copy)

            ctx_copy['contraints'] = ctx_left['contraints'] & ctx_right['contraints']

            return ctx_copy
