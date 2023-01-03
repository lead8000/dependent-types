from typing import List
from metaclass import Predicate

def intersection(
        a: List[int | Predicate(lambda x: x > 50)], 
        b: List[int | Predicate(lambda x: x < 100)]
    )  ->  List[int | Predicate(lambda x: x > 50 and x < 100)]:
    return [x for x in a if x in b]
