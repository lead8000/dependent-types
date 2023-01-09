from typing import List

def intersection(
        a: 'List[int | (lambda x: x > 50)]', 
        b: 'List[int | (lambda x: x < 100)]'
    )  ->  'List[int | (lambda x: x > 50 and x < 100)]':
    return [x for x in a if x in b]

a: int = 6
print(intersection.__annotations__)

dsl = """
axioms = {
    Student | (lambda x: x.Grade > 13 ==> x.IsUniversitary)
}

List[int | (lambda x: x > 0)]

List[float | (lambda x: x < 100)]

List[object | (lambda x: x.PropertyTrue)]

List[Person | (lambda x: x.PropertyTrue and x.Age < 50)]

List[Student | (lambda x: x.Grade <= 12 or x.IsUniversitary)]
"""

import ast

print(ast.dump(ast.parse(dsl)))