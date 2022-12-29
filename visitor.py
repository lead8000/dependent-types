import ast
from functools import reduce
from typing import Any
from metaclass import LengthVar

with open("test.py", "r") as source:  
    ast_tree = ast.parse(source.read())

axioms: set = set()


class Visitor(ast.NodeVisitor):

    def visit(self, node, ctx = {}):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, ctx)

    def generic_visit(self, node, ctx = {}):
        """Called if no explicit visitor function exists for a node."""
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, ctx)
            elif isinstance(value, ast.AST):
                self.visit(value, ctx)

    def visit_Constant(self, node, ctx = {}):
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

    def visit_FunctionDef(self, node: ast.FunctionDef, ctx = {}) -> Any:
        print('FUNCTION')
        print(ctx)
        if reduce( # check if function is an axiom
            lambda Bool, dec: Bool or dec.id == 'axiom', 
            node.decorator_list, 
            False):
            axioms.add(node.name)
        else:
            for arg in node.args.args:
                print(arg.annotation.value.id, arg.annotation.slice.id)
            print(ast.dump(node))
        print()
        return self.generic_visit(node, ctx)

    def visit_For(self, node: ast.For, ctx = {}) -> Any:
        print('FOR')
        for _node in node.body:
            print('X veces --- ', ast.dump(_node))
        print()
        return self.generic_visit(node, ctx)

    def visit_Assign(self, node: ast.Assign, ctx = {}) -> Any:
        print('ASSIGN')
        print(ast.dump(node))
        if node.value.func.id == 'LengthVar':
            lenVar = eval(f'LengthVar(\'{node.value.args[0].value}\')')
            varName=f'{node.targets[0].id}'
            ctx[varName] = lenVar
        return self.generic_visit(node, ctx)


Visitor().visit(ast_tree)

# print(axioms)