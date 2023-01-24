from .Range import Range
from .RangeSet import RangeSet


class RangeDict:

    def __init__(self, __dict):
        self.dict = {
            var: RangeSet(rng) if isinstance(rng, Range) else rng   
            for var, rng in __dict.items()
        }

    def __getitem__(self, var):
        return self.dict[var]

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
