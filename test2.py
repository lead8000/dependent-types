from dtypes import DependentType
from matrix import Matrix
from dtypes import GetAttr, _

m = Matrix([[23,3,5,43],[95,5],[93,12],[55,53]])

N = GetAttr(Matrix, 'amount_rows')
M = GetAttr(Matrix, 'amount_cols')

if issubclass(Matrix[ N, _ | (N < 100) & ( N > 50) ], Matrix[ _, M | ( M > 50 ) ]):
    print('YEESSSS')
else:
    print('NOOOOOO')
