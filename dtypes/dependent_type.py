from dtypes.ast import AST, Attr, BitOr, Constant
from dtypes.visitor import TypeInference
from dtypes.ranges import Range, RangeDict
from sys import maxsize as oo
from copy import deepcopy

class Checkable(type):

    def __instancecheck__(self, __instance) -> bool:
        
        for attr in self._attrs:
            if not self._attrs[attr].__contains__(__instance.__getattribute__(attr)):
                return False

        return True

    def __subclasscheck__(self, __subclass) -> bool:

        if self.__name__ != "DependentType" and \
        __subclass.__name__ != "DependentType":
            for cls in self.mro():
                if cls == __subclass:
                    return True
            return False

        if not issubclass(self.base_type, __subclass.base_type):
            return False

        rng_a = self._attrs
        rng_b = __subclass._attrs

        if len(rng_a) == 0:
            return True
        elif len(rng_b) == 0:
            return False

        if not isinstance(rng_a, RangeDict):
            rng_a = RangeDict(rng_a)
        if not isinstance(rng_b, RangeDict):
            rng_b = RangeDict(rng_b)

        u = rng_a | rng_b

        return rng_b == u

class Subcriptable(type):

    def __class_getitem__(self, cls, item) -> 'DependentType':
        dtypes = []
        contraint = None
        
        if isinstance(item, BitOr):
            dtypes.append(item.left)
            contraint = item.right
        else:
            for token in item:
                if isinstance(token, BitOr):
                    dtypes.append(token.left)
                    contraint = token.right
                elif isinstance(token, (int,float)):
                    dtypes.append(Constant(token))
                elif isinstance(token, AST): 
                    dtypes.append(token)

        if len(dtypes) != len(cls._attrs):
            raise Exception("Missing or excess of dependent attributes.")

        for attr1, attr2 in zip(dtypes, cls._attrs.keys()):
            attr1.attr = attr2

        _dict = { '_attrs': deepcopy(cls._attrs) }
        _dict['base_type'] = cls
        _dict['contraint'] = contraint

        dtype = DependentType.__new__(self, self.__name__, (), _dict)

        vars   = { attr: f'var_{i}' for i, attr in enumerate(dtype._attrs) } 
        ranges = { vars[attr]: rng  for attr, rng in dtype._attrs.items() }
        ctx    = { 'vars': vars, 'ranges': ranges }

        ctx_result = TypeInference().get(dtype, ctx)
        
        for attr,var in ctx_result['vars'].items():
            dtype._attrs[attr] = ctx_result['ranges'][var]

        return dtype

    def __getitem__(cls, item):
        return cls.__class_getitem__(cls, item)

class DependentType(Checkable,Subcriptable):

    def __new__(self, name, *subclasses):
        return super().__new__(self, name, *subclasses)
    
    def __init__(self, name, *subclasses, **dict) -> None:
        self._attrs = {}

    def __ior__(self, attr):
        self._attrs[attr] = Range(-oo, oo, include_start=False)
        return self

    def __ilshift__(self, contraint):
        self.contraint = contraint
        return self
