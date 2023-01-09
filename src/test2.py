import ast
from visitor import CheckPredicates

with open("predicates.py", "r") as source:
    ast_tree = ast.parse(source.read())

CheckPredicates().visit(ast_tree)
