from dependent_types import DependentType, _

class Matrix(metaclass=DependentType):

    def __init__(self, _list):
        self.list = _list
        self.amount_rows = len(_list)
        self.amount_cols = len(_list[0])
        self.len = len(self)

    def __len__(self):
        return sum([len(row) for row in self.list])

Matrix |= 'amount_rows'
Matrix |= 'amount_cols'

class Matrix4x4(Matrix[_, 4]):...
