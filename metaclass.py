
from typing import Generic, List, TypeVar


T = TypeVar('T'); K = TypeVar('K')
class Add(Generic[T, K]): pass

class Annotated(type):
	def __add__(cls, otherCls):			
		return Add[cls, otherCls]


class N(metaclass=Annotated): pass
class M(metaclass=Annotated): pass

def add_something(n: List[N]) -> List[N + 1]:
    n.append("yes")
    return n

def create_list(n: N, m: M) -> List[N + M]:
	return n * [0] + m * [1]

assert add_something(['no', 'no']) == ['no', 'no', 'yes']
print(add_something.__annotations__)

assert create_list(4,5) == [0, 0, 0, 0, 1, 1, 1, 1, 1]
print(create_list.__annotations__)
