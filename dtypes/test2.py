import ast
from ranges import Range, RangeSet
from visitor import CheckTypeComposition

# with open("predicates.py", "r") as source:
#     ast_tree = ast.parse(source.read())
# CheckPredicates().visit(ast_tree)

# ast_tree = ast.parse("List[int | (lambda x: x < 50 and x > 0)]")

# ctx_a = {}
# CheckTypeComposition().visit(ast_tree, ctx_a)
# ##print(ctx_a)

# ast_tree = ast.parse("List[int | (lambda x: x < 100)]")

# ctx_b = {}
# CheckTypeComposition().visit(ast_tree, ctx_b)
# ##print(ctx_b)

# from copy import deepcopy

# def union(dtype_a, dtype_b):
#     union = deepcopy(dtype_a)
#     union["x"]["minValue"] = min(union["x"]["minValue"], dtype_b["x"]["minValue"])
#     union["x"]["maxValue"] = max(union["x"]["maxValue"], dtype_b["x"]["maxValue"])
#     return union

# def intersection(dtype_a, dtype_b):
#     intersection = deepcopy(dtype_a)
#     intersection["x"]["minValue"] = max(intersection["x"]["minValue"], dtype_b["x"]["minValue"])
#     intersection["x"]["maxValue"] = min(intersection["x"]["maxValue"], dtype_b["x"]["maxValue"])
#     return intersection

# def difference(dtype_a, dtype_b):
#     difference = deepcopy(dtype_a)
#     if difference["x"]["minValue"] < dtype_b["x"]["minValue"]:...
#     difference["x"]["maxValue"] = min(difference["x"]["maxValue"], dtype_b["x"]["maxValue"])
#     return difference

# rng_a = ctx_a["x"]["range"]
# rng_b = ctx_b["x"]["range"]

# u = rng_a | rng_b
# i = rng_a & rng_b
# d = rng_a - rng_b

# ##print(f"union {u}")
# ##print(f"intersection {i}")
# ##print(f"difference {d}")

# ##print(rng_b == u)

# rg1 = Range(1, 10)
# rg2 = Range(3, 6)
# rg3 = rg1 - rg2
# rg88 = rg3 | Range(100, 1000)
# rg4 = Range(-5, 5) 
# rg5 = Range(8, 15)
# rg6 = rg4 | rg5
# rg7 = rg3 & rg6
# ##print(rg7)

# ##print('test')
# a = Range(1,3) #| Range(4, 9))
from ranges import Inf as oo

a = RangeSet(Range(1,3))
##print(a)
a.add(Range(6,7))
a.add(Range(8,9))
##print(a)
a.add(Range(7,8))
##print(a)
a.add(Range(3,6))
##print(a)
