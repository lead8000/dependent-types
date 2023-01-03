
from typing import List
from metaclass import LengthVar, axiom

N = LengthVar('N')
M = LengthVar('M')

@axiom
def add_something(n: List[N], item) -> List[N + 1]:
    n.append(item)
    return n

def concatenate_list(n: List[N], m: List[M]) -> List[N + M]:    
    for item in m:
        n = add_something(n, item)
    return n


# print('jfskjf')
print(N.__name__)

# assert add_something(['no', 'no'], 'yes') == ['no', 'no', 'yes']
# print(add_something.__annotations__)
