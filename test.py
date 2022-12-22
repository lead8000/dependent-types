
from typing import List
from metaclass import Annotated, annotated, axiom

class N(metaclass=Annotated): pass
class M(metaclass=Annotated): pass

@axiom
def add_something(n: List[N], item) -> List[N + 1]:
    n.append(item)
    return n

def wrapper(n: List[N], item) -> List[N+1]:
    add_something(n, item)
    return n

assert wrapper(['no', 'no'], 'yes') == ['no', 'no', 'yes']

