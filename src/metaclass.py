import re


def axiom(func):
	func.__is_axiom__ = True
	return func


class LengthVar(type):

	def __new__(cls, name):
		return super().__new__(cls, name, (), { 
			# '__repr__': lambda self: self, 
			# 'a': 100 
		})

	def __add__(self, other):

		if isinstance(other, int):
			other = LengthVar(str(other))

		x = self.__name__.split('+') + other.__name__.split('+')		

		sum = 0
		vars = []

		for i in x:
			if re.match(r'[0-9]+', i):
				sum += int(i)
			else:
				vars.append(i)

		if len(vars) == 0:
			return LengthVar(str(sum))

		vars = sorted(vars)
		vars = '+'.join(vars)

		if sum != 0:
			vars += '+' + str(sum)

		return LengthVar(vars)

	def __eq__(self, other):
		return self.__name__ == other.__name__

class ForAll(type):

	def __new__(cls, name):
		return super().__new__(cls, name, (), { 
			# '__repr__': lambda self: self, 
			# 'a': 100 
		})

class ThereExists(type):

	def __new__(cls, name):
		return super().__new__(cls, name, (), { 
			# '__repr__': lambda self: self, 
			# 'a': 100 
		})
