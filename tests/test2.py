from matrix import Matrix, Matrix4x4
from dependent_types import Attr, _

N = Attr()
M = Attr('amount_cols')

m = Matrix4x4(
    [[43,23,54,22],
     [13,65,54,34],
     [84,23,54,23],
     [29,49,23,53]]
)

# a = Matrix[N, 5 | (N > 10) ]
# (
#    [[5,6,8,3,6],
#     [2,5,6,7,4],
#     [5,6,8,3,6],
#     [2,5,6,7,4],
#     [5,6,8,3,6],
#     [2,5,6,7,4],
#     [5,6,8,3,6],
#     [2,5,6,7,4],
#     [5,6,8,3,6],
#     [2,5,6,7,4],
#     [5,6,8,3,6],
#     [2,5,6,7,4],
#     [5,6,8,3,6],
#     [2,5,6,7,4]]
# )


# assert isinstance(m, Matrix[N, M | ~(N > 1) & (M < 9)])
# A = Matrix[ N, M | (((N > 4) | ((N < 1) | (N > 2))) | ((N == 4) & (M == 3)))]

# print(isinstance(m, A))
