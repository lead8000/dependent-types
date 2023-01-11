from ast import parse, dump, BitOr, Name, BoolOp, BinOp
from visitor import CheckTypeComposition

def subtype(type_a, type_b):
    return True 

def subrestriction(lambda_a, lambda_b):
    print(f"\n{dump(lambda_a)}\n\n{dump(lambda_b)}")

    return True

def subdependenttype(dt_a, dt_b):
    """
        Dependent type A composes dependent type B.
    """
    if isinstance(dt_a, BinOp) and isinstance(dt_b, BinOp) \
        and isinstance(dt_a.op, BitOr) and isinstance(dt_b.op, BitOr):
        if subtype(dt_a.left, dt_b.left) and subrestriction(dt_a.right, dt_b.right):
            return True
    elif isinstance(dt_a, BinOp) and isinstance(dt_b, Name) \
        and isinstance(dt_a.op, BitOr):...
    elif isinstance(dt_a, Name) and isinstance(dt_b, BinOp) \
        and isinstance(dt_b.op, BitOr):...
    elif isinstance(dt_a, BinOp) and isinstance(dt_b, BoolOp) \
        and isinstance(dt_a.op, BitOr):...
    elif isinstance(dt_a, BoolOp) and isinstance(dt_b, BinOp) \
        and isinstance(dt_b.op, BitOr):...

    raise Exception("Invalid dependent types.")

def composes(dt_a, dt_b):
    """
        Dependent type A composes dependent type B.
    """
    ast_a = parse(dt_a)
    ast_b = parse(dt_b)

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

    print(dump(dt_a))
    print()
    print(dump(dt_b))

    # types_a = slice_a.left
    # types_b = slice_b.left
    # assert type(slice_a.op) == type(slice_b.op) == BitOr    
    # print(dump(slice_a))

    return subdependenttype(dt_a, dt_b)

stament = composes(
    'int | (lambda x: x < 4 * 50 + 10 * 8 and x > 0)',
    'float | (lambda x: x < 100)'
)

print(f"\n{stament}")
