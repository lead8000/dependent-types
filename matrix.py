from dtypes import DependentType, _

class Matrix(metaclass=DependentType):

    def __init__(self, l):
        self.list = l
        self.amount_rows = len(l)
        self.amount_cols = len(l[0])
        self.len = len(self)
    
    def __len__(self):
        return sum([len(row) for row in self.list])

Matrix |= 'amount_rows'
Matrix |= 'amount_cols'

class Matrix4x4(Matrix[_, 4]):...
