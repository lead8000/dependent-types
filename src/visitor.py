import ast
from functools import reduce
from typing import Any, List
from metaclass import LengthVar
from copy import deepcopy


def visualizer(fnc):

    def decorator(_, node, ctx = {}):        
        print(f'\n<--- {node.__class__.__name__.upper()} --->\n\nCONTEXT: {ctx}\n')
        print(f'{ast.dump(node)}')
        fnc(_, node, ctx)
    
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
    def visit_FunctionDef(self, node: ast.FunctionDef, ctx = {}) -> Any:
        return self.generic_visit(node, ctx)
