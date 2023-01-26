from matrix import Matrix
from dtypes import Attr, _

N = Attr('amount_rows')
M = Attr('amount_cols')

def test_1():
    assert not issubclass(Matrix[ N, _ | (N < 100) & ( N > 50) ], Matrix[ _, M | ( M > 50 ) ])
