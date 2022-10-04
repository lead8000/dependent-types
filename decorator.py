from typing import List

"""
    `before`: is a lambda expression that receives all the parameters of the function and returns a dictionary with some useful values
    `after`: is a predicate that receives the result of the function and the dictionary of the predicate `before`
"""
def predicate(before, after):

	def inner(func):

		def wrapper(*args, **kwargs):

			predicateResults = before(*args, **kwargs)

			result = func(*args, **kwargs)

			if not after(result, **predicateResults):
				raise Exception("the predicate is not fulfilled")

			if func.__annotations__.__contains__("return"): 
				return result
			
		return wrapper

	return inner


@predicate(
	before = lambda input : { "len_input" : len(input) },
	after = lambda result, len_input : len_input == len(result) - 1
)
def add_yes(input: List[str]) -> List[str]:
	input.append("yes")
	return input


@predicate(
	before = lambda x, y: { "x__y": x + y },
	after = lambda result, x__y: len(result) == x__y
)
def create_list(x: int, y: int) -> List[int]:
	return x * [0] + y * [1]


assert add_yes(['no', 'no']) == ["no", "no", "yes"]
assert create_list(4,5) == [0, 0, 0, 0, 1, 1, 1, 1, 1]