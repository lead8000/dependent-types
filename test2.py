from dtypes import DependentType
from matrix import Matrix
from dtypes import GetAttr, _
from dtypes.visitor import CheckTypeComposition

m = Matrix([[23,3,5,43],[95,5],[93,12],[55,53]])

N = GetAttr(Matrix, 'amount_rows')
M = GetAttr(Matrix, 'amount_cols')

if isinstance(m, Matrix[ M, _ | ( (N > 2 * M) & (N <= M + 1) | (M != 4) ) ]):
    print('YEESSSS')
else:
    print('NOOOOOO')

# expr = (2*N > M) | ( (M != 1) & (N % 2 == 1) ) | (M > 50)

class A:...
class B(A):...
assert issubclass(B, A)

# if issubclass(Matrix[ N | ( (N < 100) & ( N > 50) ) ], Matrix[ N | ( N > 50 ) ]):

# expr = N > 50
# ctx = { 'vars': {}, 'ranges': {} }
# ctx_result = CheckTypeComposition().visit(expr, ctx)
# print(f'\nFINAL CONTEXT: {ctx_result}')

# expr2 = N > 100
# ctx2 = { 'vars': {}, 'ranges': {} }
# ctx_result2 = CheckTypeComposition().visit(expr2, ctx2)
# print(f'\nFINAL CONTEXT: {ctx_result2}')