from dependent_types.metaclass import DependentType, SetAttr
from dependent_types.ast.literals import AttrVar

class Matrix(metaclass=DependentType):

    def __init__(self, l):
        self.list = l
        self.amount_rows = len(l)
        self.amount_cols = len(l[0])
    
    def __len__(self):
        return sum([len(row) for row in self.list])

# N = AttrVar('N')
# M = AttrVar('M')

Matrix |= 'amount_rows'
Matrix |= 'amount_cols'

print(Matrix.__dict__)
# Matrix <<= (N > 2 * M) & (N <= M + 1) | (N == 1)

m = Matrix([[23,43],[95,2],[93,12],[3,53]])

N = SetAttr(Matrix, 'amount_rows')
M = SetAttr(Matrix, 'amount_cols')

if isinstance(m, Matrix[ N, M | ( (N > 2 * M) & (N <= M + 1) | (N != 1) ) ]):
    print('YEESSSS')
else:
    print('NOOOOOO')

# Matrix[N, M | (N == 2 * M) & (N == M + 1)]
