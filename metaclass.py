
from typing import Generic, TypeVar

T = TypeVar('T'); K = TypeVar('K')
class Add(Generic[T, K]): pass

class Annotated(type):
	def __add__(cls, otherCls):			
		return Add[cls, otherCls]

def axiom(func):
	return func
