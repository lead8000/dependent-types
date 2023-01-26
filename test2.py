from matrix import Matrix, Matrix4x4
from dtypes import Attr, _

N = Attr()
M = Attr('amount_cols')

m = Matrix4x4(
    [[43,23,54,22],
     [13,65,54,34],
     [84,23,54,23],
     [29,49,23,53]]
)

a = Matrix[N, 5 | (N > 10) ]
(
   [[5,6,8,3,6],
    [2,5,6,7,4],
    [5,6,8,3,6],
    [2,5,6,7,4],
    [5,6,8,3,6],
    [2,5,6,7,4],
    [5,6,8,3,6],
    [2,5,6,7,4],
    [5,6,8,3,6],
    [2,5,6,7,4],
    [5,6,8,3,6],
    [2,5,6,7,4],
    [5,6,8,3,6],
    [2,5,6,7,4]]
)


# assert isinstance(m, Matrix[N, M | ~(N > 1) & (M < 9)])
assert not isinstance(a, Matrix[N, 4 | (M < 9)])

try:
    A = Matrix[N, 4 | (M > 9)]
except:...

print(A.__dict__)