from metaclass import DependentType, Attribute, Predicate

class Matrix(metaclass=DependentType):

    def __init__(self, l):
        self.list = l
        self.amount_rows = len(l)
        self.amount_cols = len(l[0])
    
    def __len__(self):
        return sum([len(row) for row in self.list])

N = Attribute(Matrix, 'amount_rows')
M = Attribute(Matrix, 'amount_cols')

m = Matrix([[9,4],[4,3],[5,5],[43,5]])
print(f'm={m.list}')
print(f'isinstance(m, Matrix[N, M | Predicate(lambda: N == M)]): {isinstance(m, Matrix[N, M | Predicate(lambda: (N - 1) // 2  < M ** 2)])}')
