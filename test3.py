from dependent_types.metaclass import DependentType, Attribute

class Matrix(metaclass=DependentType):

    def __init__(self, l):
        self.list = l
        self.amount_rows = len(l)
        self.amount_cols = len(l[0])
    
    def __len__(self):
        return sum([len(row) for row in self.list])

N = Attribute(Matrix, 'amount_rows')
M = Attribute(Matrix, 'amount_cols')

m = Matrix([[23,43],[95,2],[93,12],[3,53]])
if isinstance(m, Matrix[ N, M | N < 2 * M ]):
    print('YEESSSS')
else:
    print('NOOOOOO')
