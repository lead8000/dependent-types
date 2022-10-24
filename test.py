
from typing import List
from metaclass import Annotated, axiom

class N(metaclass=Annotated): pass
class M(metaclass=Annotated): pass

@axiom
def add_something(n: List[N], item) -> List[N + 1]:
    n.append(item)
    return n

def concatenate_list(n: List[N], m: List[M]) -> List[N + M]:    
    for item in m:
        add_something(n, item)
    return n

assert add_something(['no', 'no'], 'yes') == ['no', 'no', 'yes']
print(add_something.__annotations__)
