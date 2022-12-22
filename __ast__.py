import ast
from functools import reduce
from typing import Any, List

with open("test.py", "r") as source:  
    ast_tree = ast.parse(source.read())

axioms = {}
proofs: List[ast.NodeVisitor] = []
variables = {}
annotations = {}

class Visitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if reduce(
            lambda Bool, dec: Bool or dec.id == 'axiom', 
            node.decorator_list, 
            False):
            axioms[node.name]=True
        else:
            proofs.append(node)

class Proofs(ast.NodeVisitor):

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        # print(ast.dump(node))
        # print(f'\n{ast.dump(node.args.args[0])}\n')
        
        # visitor for get
        GetInPar().generic_visit(node)
        
        # return self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr) -> Any:
        print(ast.dump(node))
    
    def visit_Name(self, node: ast.Name) -> Any:
        print(ast.dump(node))

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        print(ast.dump(node))

    def visit_Return(self, node: ast.Return) -> Any:
        print(ast.dump(node))

class GetInPar(ast.NodeVisitor):

    def visit_arg(self, node: ast.arg) -> Any:
        if node.annotation != None:
            annotations[node.arg] = node.annotation
            self.generic_visit(node)

Visitor().visit(ast_tree)
Proofs().visit(proofs[0])

print(axioms)
print(variables)
print(annotations['n'])

# print(ast.dump(proofs[0]))
# visitor para coger las variables de entrada y sus tipos