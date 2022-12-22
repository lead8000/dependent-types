
from typing import Generic, TypeVar

T = TypeVar('T'); K = TypeVar('K')
class Add(Generic[T, K]): pass

class Annotated(type):
	def __add__(cls, otherCls):			
		return Add[cls, otherCls]

class Function:
	def __init__(self, func):
		self.func = func

	def __call__(self, *args, **kwargs):
		return self.func(*args, **kwargs)

def axiom(func):
	return func

def annotated(func):
	newFunc = Function(func)
	newFunc.__dict__['signature'] = func.__annotations__
	return newFunc