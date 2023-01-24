from matrix import Matrix
from dtypes import GetAttr

#print(Matrix.__dict__)
# Matrix <<= (N > 2 * M) & (N <= M + 1) | (N == 1)

m = Matrix([[23,3,5,43],[95,5],[93,12],[55,53]])

N = GetAttr(Matrix, 'amount_rows')
M = GetAttr(Matrix, 'amount_cols')

# if isinstance(m, Matrix[ N, 4 | ( (N > 2 * M) & (N <= M + 1) | (M != 4) ) ]):

if issubclass(Matrix[ N, M | ( 2*N > M ) ], Matrix[ N, M | ( N > M ) ]):
    print('YEESSSS')
else:
    print('NOOOOOO')
