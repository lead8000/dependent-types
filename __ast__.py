import ast
from functools import reduce
from typing import Any

with open("test.py", "r") as source:  
    ast_tree = ast.parse(source.read())

axioms = {}

class Visitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if reduce(
            lambda Bool, dec: Bool or dec.id == 'axiom', 
            node.decorator_list, 
            False):
            axioms[node.name]=True
        else:
            for _node in node.body:
                print(ast.dump(_node))
        return ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node: ast.Call) -> Any:

        name: ast.Name = node.func
        
        if 'id' in name._fields:
            print(name.__dict__['id'])

        return ast.NodeVisitor.generic_visit(self, node)

Visitor().visit(ast_tree)

print(axioms)