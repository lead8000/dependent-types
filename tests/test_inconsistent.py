from .matrix import Matrix
from dependent_types import Attr

N = Attr()
M = Attr()

def test_1():
    try:
        Matrix[N, 4| (M > 9)]
    except Exception:
        return True
    # raise Exception() 
    