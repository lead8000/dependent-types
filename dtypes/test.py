"""
something
"""

import ast
from dtypes.metaclasses import LengthVar
from visitor import Visitor
from typing import List

K = LengthVar('5+T')
J = LengthVar('T+4')

T = LengthVar('3+K')
I = LengthVar('K+4')
#print(T+1 == I)

# with open("proof.py", "r") as source:  
#     ast_tree = ast.parse(source.read())

# Visitor().visit(ast_tree)

# class A:
#     a: 'List[int | (lambda x: x % 2 == 0)]' = []

# from itertools import zip_longest

# for i in zip_longest(range(10), range(40,60)):
#     #print(i)