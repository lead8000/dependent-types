from .Range import Range
from .RangeSet import RangeSet
from .RangeDict import RangeDict
from copy import deepcopy


class RangeList:
    """
        RangeDict handles relationships between dictionaries with stored Ranges.
    """
    def __init__(self, __rng):
        if isinstance(__rng, RangeList):
            self.list = deepcopy(__rng.list)
        elif isinstance(__rng, RangeDict):
            self.list = [deepcopy(__rng)]

    # def __getitem__(self, var):
    #     return self.dict[var]

    # def __setitem__(self, var, rng):
        
    #     if isinstance(rng, Range):
    #         self.dict[var] = RangeSet(rng)

    #     elif isinstance(rng, RangeSet):
    #         self.dict[var] = rng

    def __or__(self, other):
        if isinstance(other, RangeList):
            return RangeList(deepcopy(self.list) + deepcopy(other.list))

    def __and__(self, other):
        if isinstance(other, RangeList):
            list_ = []
            for dict1 in self.list:
                for dict2 in other.list:
                    list_.append(deepcopy(dict1) & deepcopy(dict2))
            return RangeList(list_)

    # def __eq__(self, other) -> bool:
        
    #     try:
    #         for var, rng in self.dict.items():    
    #             if other[var] != rng:
    #                 return False
    #         return True
        
    #     except KeyError:
    #         return False

    # def __repr__(self) -> str:
    #     __str = ""
    #     first = True
    #     for var, rng in self.dict.items():
    #         if first:
    #             __str += f'{var}: {rng}'
    #             first = False
    #         else:
    #             __str += f', {var}: {rng}'
    #     return "RangeDict{ " + __str + " }"

    # def __len__(self) -> int:
    #     return len(self.dict)