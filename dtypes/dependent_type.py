from dtypes.ast import AST, Attr, BitOr, Constant
from dtypes.visitor import TypeInference
from dtypes.ranges import Range, RangeDict, RangeList, RangeSet
from sys import maxsize as oo
from copy import deepcopy
import dtypes

class Checkable(type):

    def __instancecheck__(self, instance) -> bool:
        # print(eval(f'__instance.{attr}'))
        for attr in self._attrs:
            if not self._attrs[attr].__contains__(eval(f'instance.{attr}')):
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

        _dict = { name: deepcopy(func) for name, func in cls.__dict__.items() 
            if name not in ('__module__', '__weakref__', '__dict__') }
        _dict['base_type'] = cls
        _dict['contraint'] = contraint

        for attr1, attr2 in zip(dtypes, cls._attrs.keys()):
            if isinstance(attr1, Constant):
                _dict['_attrs'][attr2] = RangeSet(Range(f"[{attr1.value},{attr1.value}]"))
            else:
                attr1.attr = attr2
        _dict['_ranges'] = RangeList(RangeDict(_dict['_attrs']))

        dtype = DependentType.__new__(self, self.__name__, (), _dict)

        vars   = { attr: f'var_{i}' for i, attr in enumerate(dtype._attrs) } 
        ranges = deepcopy(dtype._ranges)
        ctx    = { 'vars': vars, 'ranges': ranges }

        if contraint:
            print(f'\n{ctx}')
            ctx_result = TypeInference().get(dtype, ctx)

            print(f'{ctx_result}\n')
            for attr,var in ctx_result['vars'].items():
                if ctx_result['ranges'][var]:
                    dtype._attrs[attr] = ctx_result['ranges'][var]
                else:
                    raise Exception("The dependent type expresses an inconsistent state.")
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
