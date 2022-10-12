
from typing import Generic, List, TypeVar


T = TypeVar('T')
K = TypeVar('K')
class Add(Generic[T, K]):
	pass

class Annotated(type):
	def __add__(cls, otherCls):			
		return Add[cls, otherCls]

class N(metaclass=Annotated):
	pass

class M(metaclass=Annotated):
	pass

def add_something(l: List[N]) -> List[N + 1]:
    l.append("yes")
    return l

assert add_something(['no', 'no']) == ['no', 'no', 'yes']

print(add_something.__annotations__)
