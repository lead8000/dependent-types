import ast
from functools import reduce
from metaclass import LengthVar
from copy import deepcopy
from ranges import Range 
from ranges import Inf as oo

def visualizer(func):

    def decorator(_, node, ctx = {}):        
        print(f'\n<--- {node.__class__.__name__.upper()} --->\n\nCONTEXT: {ctx}\n')
        print(f'{ast.dump(node)}')
        func(_, node, ctx)
    
    return decorator

class GenericVisitor(ast.NodeVisitor):

    def visit(self, node, ctx = {}):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, ctx)

    def generic_visit(self, node, ctx = {}):
        """Called if no explicit visitor function exists for a node."""
        for _, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, ctx)
            elif isinstance(value, ast.AST):
                self.visit(value, ctx)
    
    def visit_Constant(self, node: ast.Constant, ctx = {}):
        value = node.value
        type_name = ast._const_node_type_names.get(type(value))
        if type_name is None:
            for cls, name in ast._const_node_type_names.items():
                if isinstance(value, cls):
                    type_name = name
                    break
        if type_name is not None:
            method = 'visit_' + type_name
            try:
                visitor = getattr(self, method)
            except AttributeError:
                pass
            else:
                import warnings
                warnings.warn(f"{method} is deprecated; add visit_Constant",
                              DeprecationWarning, 2)
                return visitor(node, ctx)
        return self.generic_visit(node, ctx) 

class Visitor(GenericVisitor):

    @visualizer
    def visit_FunctionDef(self, node: ast.FunctionDef, ctx = {}):
        childCtx = deepcopy(ctx)
        if reduce( # check if function is an axiom
            lambda Bool, dec: Bool or dec.id == 'axiom', 
            node.decorator_list, 
            False):
            if 'axioms' not in ctx:
                ctx['axioms'] = set()
            ctx['axioms'].add(node.name)
        else:
            if 'unchecked' not in ctx:
                ctx['unchecked'] = set()
            ctx['unchecked'].add(node.name)
            for arg in node.args.args:
                dtype = childCtx[f'{arg.annotation.slice.id}']
                # print(dtype)
                # print(f'{ arg.annotation.value.id }[{dtype}]')
                childCtx[arg.arg] = deepcopy(dtype) 
            print(ast.dump(node))
            print(ctx)    

        print()

        return self.generic_visit(node, childCtx)

    @visualizer
    def visit_For(self, node: ast.For, ctx = {}):
        for _node in node.body:
            if isinstance(_node, ast.Assign):
                ctx['numberOfTimes'] = ctx[node.iter.id]
            print(f'{ctx[node.iter.id]} veces --- ', ast.dump(_node))
            print(_node.targets)
        print()
        return self.generic_visit(node, ctx)

    @visualizer
    def visit_Assign(self, node: ast.Assign, ctx = {}):
        if node.value.func.id == 'LengthVar':
            lenVar = eval(f'LengthVar(\'{node.value.args[0].value}\')')
            varName=f'{node.targets[0].id}'
            ctx[varName] = lenVar
        else: 
            # check if there is cyclic dependency
            varAssign = node.targets[0].id
            if varAssign in [arg.id for arg in node.value.args]:
                numberOfTimes = LengthVar('1')
                # check if it executes various times
                if 'numberOfTimes' in ctx:
                    numberOfTimes = ctx['numberOfTimes']
                    if isinstance(ctx['numberOfTimes'], str):
                        numberOfTimes = ctx[numberOfTimes] 
                    # ctx.__delattr__('numberOfTimes')
                ctx[varAssign] = ctx[varAssign] + numberOfTimes
                print(ctx)

        print()
        return self.generic_visit(node, ctx)

    @visualizer
    def visit_Return(self, node: ast.Return, ctx = {}):
        return self.generic_visit(node, ctx)

class CheckPredicates(GenericVisitor):

    @visualizer
    def visit(self, type_a, ctx={}):
        return super().visit(type_a, ctx)

    def visit_Expr(self, node: ast.Expr, ctx={}):
        return self.generic_visit(node, ctx)

# def visualizer2(func):

#     def decorator(_, type_a, type_b, ctx = {}):        
#         print(f'\n<--- {type_a.__class__.__name__.upper()} --->\n\nCONTEXT: {ctx}\n')
#         print(f'{ast.dump(type_a)}')
#         print(f'\n<--- {type_b.__class__.__name__.upper()} --->\n\nCONTEXT: {ctx}\n')
#         print(f'{ast.dump(type_b)}\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n')
#         func(_, type_a, type_b, ctx)
    
#     return decorator

# from itertools import zip_longest

# class CheckTypeComposition:

#     @visualizer2
#     def visit(self, type_a, type_b, ctx = {}):
#         """Visit a node."""
#         method = f'visit_{type_a.__class__.__name__}_{type_b.__class__.__name__}'
#         visitor = getattr(self, method, self.generic_visit)
#         return visitor(type_a, type_b, ctx)

#     def generic_visit(self, type_a, type_b, ctx = {}):
#         """Called if no explicit visitor function exists for a node."""
#         if type(type_a) == type(type_b):

#             for t in zip_longest(ast.iter_fields(type_a), ast.iter_fields(type_b)):
#                 a, b = t
#                 if a:
#                     field_a, value_a = a
#                 if b:
#                     field_b, value_b = b

#                 if field_a == field_b:
#                     ...

#                 if isinstance(value_a, list) and isinstance(value_b, list):
#                     for item_a, item_b in zip_longest(value_a, value_b):
#                         if isinstance(item_a, ast.AST) and isinstance(item_b, ast.AST):
#                             self.visit(item_a, item_b, ctx)
#                 elif isinstance(value_a, ast.AST) and isinstance(value_b, ast.AST):
#                     self.visit(value_a, value_b, ctx)
    
#     def visit_Constant_Constant(self, type_a: ast.Constant, type_b: ast.Constant, ctx = {}):
#         value = type_a.value
#         type_name = ast._const_node_type_names.get(type(value))
#         if type_name is None:
#             for cls, name in ast._const_node_type_names.items():
#                 if isinstance(value, cls):
#                     type_name = name
#                     break
#         if type_name is not None:
#             method = 'visit_' + type_name
#             try:
#                 visitor = getattr(self, method)
#             except AttributeError:
#                 pass
#             else:
#                 import warnings
#                 warnings.warn(f"{method} is deprecated; add visit_Constant",
#                               DeprecationWarning, 2)
#                 return visitor(type_a, ctx)
#         return self.generic_visit(type_a, ctx) 

#     def visit_Expr_Expr(self, type_a, type_b, ctx={}):
#         return self.generic_visit(type_a, type_b, ctx)

#     def visit_BinOp_BinOp(self, dtype_a, dtype_b, ctx={}):
#         if type(dtype_a.op) == type(dtype_b.op) == ast.BitOr \
#             and subtype(dtype_a.left,dtype_b.left):
#             self.visit(dtype_a.left, dtype_b.left, ctx)
#             self.visit(dtype_a.right, dtype_b.right, ctx)
        
#         return self.generic_visit(dtype_a, dtype_b, ctx)

#     def visit_Name_BinOp(self, type_a, type_b, ctx = {}):
#         print('!!!!!!!!!')
#         return self.generic_visit(type_a, type_b, ctx)

#     def visit_BinOp_Name(self, type_a, type_b, ctx = {}):
#         print('?????????')
#         return self.generic_visit(type_a, type_b, ctx)


def subtype(type_a, type_b):
    return True 

def subrestriction(lambda_a, lambda_b):
    print(f"\n{ast.dump(lambda_a)}\n\n{ast.dump(lambda_b)}")

    return True

def subdependenttype(dt_a, dt_b):
    """
        Dependent type A composes dependent type B.
    """
    if isinstance(dt_a, ast.BinOp) and isinstance(dt_b, ast.BinOp) \
        and isinstance(dt_a.op, ast.BitOr) and isinstance(dt_b.op, ast.BitOr):
        if subtype(dt_a.left, dt_b.left) and subrestriction(dt_a.right, dt_b.right):
            return True
    elif isinstance(dt_a, ast.BinOp) and isinstance(dt_b, ast.Name) \
        and isinstance(dt_a.op, ast.BitOr):...
    elif isinstance(dt_a, ast.Name) and isinstance(dt_b, ast.BinOp) \
        and isinstance(dt_b.op, ast.BitOr):...
    elif isinstance(dt_a, ast.BinOp) and isinstance(dt_b, ast.BoolOp) \
        and isinstance(dt_a.op, ast.BitOr):...
    elif isinstance(dt_a, ast.BoolOp) and isinstance(dt_b, ast.BinOp) \
        and isinstance(dt_b.op, ast.BitOr):...

    raise Exception("Invalid dependent types.")

def composes(dt_a, dt_b):
    """
        Dependent type A composes dependent type B.
    """
    ast_a = ast.parse(dt_a)
    ast_b = ast.parse(dt_b)
    # print(dump(ast_a))
    # print()
    # print(dump(ast_b))
    # CheckTypeComposition().generic_visit(ast_a, ast_b)
    # print(
    #     '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',
    #     '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    # )
    # CheckTypeComposition().generic_visit(ast_b)

    dt_a = ast_a.body[0].value
    dt_b = ast_b.body[0].value
    # slice_a = ast_a.body[0].value.slice
    # slice_b = ast_b.body[0].value.slice

    print(ast.dump(dt_a))
    print()
    print(ast.dump(dt_b))

    
    # types_a = slice_a.left
    # types_b = slice_b.left
    # assert type(slice_a.op) == type(slice_b.op) == BitOr    
    # print(dump(slice_a))

    return subdependenttype(dt_a, dt_b)

class CheckTypeComposition(GenericVisitor):

    # @visualizer
    def visit(self, dtype, ctx={}):
        return super().visit(dtype, ctx)

    def visit_Lambda(self, dtype: ast.Lambda, ctx={}):
        for arg in dtype.args.args:
            ctx[arg.arg] = { "range": Range(-oo, oo) }
        return self.visit(dtype.body, ctx)

    def visit_Compare(self, dtype: ast.Compare, ctx={}):
        print(ast.dump(dtype))
        if isinstance(dtype.left, ast.Attribute):
            ... #TODO
        elif isinstance(dtype.left, ast.Name):
            if isinstance(dtype.ops[0], ast.Lt):
                rng = Range(-oo, dtype.comparators[0].value)
                ctx[dtype.left.id]["range"] &= rng
            elif isinstance(dtype.ops[0], ast.Gt):
                rng = Range(dtype.comparators[0].value, oo)
                ctx[dtype.left.id]["range"] &= rng
        elif isinstance(dtype.left, ast.Constant):
            if isinstance(dtype.comparators[0], ast.Attribute):
                ... #TODO
            elif isinstance(dtype.comparators[0], ast.Name):
                if isinstance(dtype.ops[0], ast.Lt):
                    rng = Range(dtype.left.value, oo)
                    ctx[dtype.comparators[0].id]["range"] &= rng
                elif isinstance(dtype.ops[0], ast.Gt):
                    rng = Range(-oo, dtype.left.value)
                    ctx[dtype.comparators[0].id]["range"] &= rng

    def visit_BoolOp(self, dtype: ast.BoolOp, ctx={}):
        if isinstance(dtype.op, ast.And):
            for value in dtype.values:
                self.visit(value, ctx)
