from .matrix import Matrix
from dependent_types import Attr, _

N = Attr('amount_rows')
M = Attr('amount_cols')

def test_1():
    assert issubclass(
        Matrix[ N, M | (((N < 100) & ( N > 50)) & (M > 100)) ], 
        Matrix[ _, M | ( M > 50 ) ]
    )
