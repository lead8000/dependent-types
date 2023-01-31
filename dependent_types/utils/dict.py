from copy import deepcopy
from sys import maxsize as oo
from dependent_types.ranges.RangeSet import RangeSet


class AttributeDict:
    """
        Dictionary of `dependent attributes` to store coupled possible 
        attribute values.
    """ 
    def __init__(self, __attrs = None):
        if isinstance(__attrs, dict):
            self.__attribute_dict__ = deepcopy(__attrs)
        elif not __attrs:
            self.__attribute_dict__ = {}

    def __getitem__(self, attr):
        return self.__attribute_dict__[attr]

    def __contains__(self, attr, value):
        if attr not in self.__attribute_dict__:
            return True
        return self.__attribute_dict__[attr].__contains__(value)

    def __setitem__(self, attr, value):
        self.__attribute_dict__[attr] = value        

    def __or__(self, other: 'AttributeDict'):
        attr_dict = AttributeDict()

        for attr, value in self.__attribute_dict__.items():
            attr_dict[attr] = deepcopy(value)

        for attr, value in other.__attribute_dict__.items():
            if attr in attr_dict.__attribute_dict__:
                attr_dict[attr] |= deepcopy(value)
        
        return attr_dict

    def __and__(self, other: 'AttributeDict'):
        attr_dict = AttributeDict()

        for attr, value in self.__attribute_dict__.items():
            attr_dict[attr] = deepcopy(value)

        for attr, value in other.__attribute_dict__.items():
            if attr in attr_dict.__attribute_dict__:
                attr_dict[attr] &= deepcopy(value)
            else:
                attr_dict[attr] = deepcopy(value)
        
        return attr_dict

    def __eq__(self, other) -> bool:
        
        try:
            for attr, value in self.__attribute_dict__.items():    
                if value == RangeSet(f'({-oo}, {oo})'): continue
                if other[attr] != value:
                    return False
            return True
        
        except KeyError:
            return False

    def __repr__(self) -> str:
        __str = ""
        first = True
        for var, rng in self.__attribute_dict__.items():
            if first:
                __str += f'{var}: {rng}'
                first = False
            else:
                __str += f', {var}: {rng}'
        return "RangeDict{ " + __str + " }"

    def __len__(self) -> int:
        return len(self.__attribute_dict__)

