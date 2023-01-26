from .Range import Range
from .RangeSet import RangeSet
from copy import deepcopy


class RangeDict:
    """
        RangeDict handles relationships between dictionaries with stored Ranges.
    """
    def __init__(self, __dict):
        if isinstance(__dict, RangeDict):
            self.dict = deepcopy(__dict.dict)
        else:
            #print(type(__dict))
            self.dict = {
                var: RangeSet(rng) if isinstance(rng, Range) else rng   
                for var, rng in __dict.items()
            }

    def __getitem__(self, var):
        return self.dict[var]

    def __contains__(self, attr, value):
        return self.dict[attr].__contains__(value)

    def __setitem__(self, var, rng):
        
        if isinstance(rng, Range):
            self.dict[var] = RangeSet(rng)

        elif isinstance(rng, RangeSet):
            self.dict[var] = rng

    def __or__(self, other):
        rng_dict = RangeDict({})

        for var, rng in self.dict.items():
            rng_dict[var] = rng

        for var, rng in other.dict.items():
            if var in rng_dict.dict:
                rng_dict[var] |= rng
            else:
                rng_dict[var] = rng
        
        return rng_dict

    def __and__(self, other):
        rng_dict = RangeDict({})

        for var, rng in self.dict.items():
            rng_dict[var] = rng

        for var, rng in other.dict.items():
            if var in rng_dict.dict:
                rng_dict[var] &= rng
            else:
                rng_dict[var] = rng
        
        return rng_dict

    def __eq__(self, other) -> bool:
        
        try:
            for var, rng in self.dict.items():    
                if other[var] != rng:
                    return False
            return True
        
        except KeyError:
            return False

    def __repr__(self) -> str:
        __str = ""
        first = True
        for var, rng in self.dict.items():
            if first:
                __str += f'{var}: {rng}'
                first = False
            else:
                __str += f', {var}: {rng}'
        return "RangeDict{ " + __str + " }"

    def __len__(self) -> int:
        return len(self.dict)