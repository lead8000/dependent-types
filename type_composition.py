from ast import parse
from ranges import Range, RangeSet
from dtypes.visitor import CheckTypeComposition

def composes(dt_a, dt_b):
    """
        Dependent type A composes dependent type B.
    """
    ast_a = parse(dt_a)
    ast_b = parse(dt_b)

    ctx_a = {} 
    ctx_b = {}
    CheckTypeComposition().visit(ast_a, ctx_a)
    CheckTypeComposition().visit(ast_b, ctx_b)
    print(ctx_a)
    print(ctx_b)
    rng_a = ctx_a["x"]["range"]
    rng_b = ctx_b["x"]["range"]

    if rng_a is None:
        return True
    elif rng_b is None:
        return False
    
    if isinstance(rng_a, Range):
        rng_a = RangeSet(rng_a)
    if isinstance(rng_b, Range):
        rng_b = RangeSet(rng_b)

    u = rng_a | rng_b

    return rng_b == u

stament = composes(
    'List[int | (lambda x: (x < 170 and x >= 160) or (x >= 0 and x <= 50) or (x >= 75 and x <= 100))]',
    'List[float | (lambda x: x >= 0 and x < 170)]'
)
print(stament)

from typing import List
class Person: 
    pass

def do_something(
        a: "List[float | (lambda x: x < 10 and x >= -23)]",
        b: "List[Person | (lambda p: p.Age > 0 and p.Grade >= 1 and p.Grade <= 12 and p.Age < 80)]"
    ):
    pass

dtype_a = "List[float | (lambda x: x < 10 and x >= -23)]"
dtype_b = "List[Person | (lambda p: p.Age > 0 and p.Grade >= 1 and p.Grade <= 12 and p.Age < 80)]"

# #print(composes(dtype_a, dtype_b))


