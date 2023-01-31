from .matrix import Matrix
from dependent_types import Attr, _

N = Attr('amount_rows')
M = Attr('amount_cols')

m = Matrix(
    [[43,23,54,22],
     [13,65,54,34],
     [84,23,54,23],
     [29,49,23,53]]
)

def test_1():
    assert not isinstance(m, Matrix[ _, M | ( M > 50 ) ])
