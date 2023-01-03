import ast
from visitor import Visitor


# T = LengthVar('3+K')
# K = LengthVar('5+T')

# I = LengthVar('K+4')
# J = LengthVar('T+4')

# print(type(T))
# print(type(J))

# L = List[type(T)]
# print(type(L))
# print(T+1 == I)


with open("proof.py", "r") as source:  
    ast_tree = ast.parse(source.read())

Visitor().visit(ast_tree)
