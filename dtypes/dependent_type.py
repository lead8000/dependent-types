from dtypes.ast import AST, Attr, BitOr, Constant
from dtypes.visitor import CheckTypeComposition
from dtypes.ranges import RangeDict

def GetAttr(cls, attr):
    attribute = None
    for _attr in cls.attrs:
        if _attr.attr == attr:
            attribute = _attr
            break
    if attribute is None:
        attribute = Attr(attr)
    return attribute

class Checkable(type):

    def __instancecheck__(self, __instance) -> bool:
        
        for attr in self.attrs:
            attr.value = __instance.__getattribute__(attr.attr)

        for dtype in self.dtypes:
            if isinstance(dtype, Attr):
                dtype.value = __instance.__getattribute__(dtype.attr)

        if len(self.attrs) != len(self.dtypes):
            return False

        for attr, dtype in zip(self.attrs, self.dtypes):
            if attr.value != dtype.value:
                return False
        
        if self.predicate:
            predicate = self.predicate.eval()

        for attr in self.attrs:
            attr.value = None

        for dtype in self.dtypes:
            dtype.value = None
        
        return predicate if self.predicate else True

    def __subclasscheck__(self, __subclass) -> bool:

        if self.__name__ != "DependentType" and \
        __subclass.__name__ != "DependentType":
            for cls in self.mro():
                if cls == __subclass:
                    return True
            return False

        if not issubclass(self.base_type, __subclass.base_type):
            return False

        dt_a = __subclass.predicate
        ctx_a = { 'vars': {}, 'ranges': {} }
        ctx_result_a = CheckTypeComposition().visit(dt_a, ctx_a)

        dt_b = self.predicate
        ctx_b = { 'vars': { k:v for k,v in ctx_result_a['vars'].items() }, 'ranges': {} }
        ctx_result_b = CheckTypeComposition().visit(dt_b, ctx_b)

        rng_a = ctx_result_a['ranges']
        rng_b = ctx_result_b['ranges']

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
        i = 0
        dtypes = []
        predicate = None

        if isinstance(item, BitOr):
            dtypes.append(item.left)
            predicate = item.right
        else:
            while i < len(item):
                if isinstance(item[i], BitOr):
                    dtypes.append(item[i].left)
                    predicate = item[i].right
                elif isinstance(item[i], (int,float)):
                    dtypes.append(Constant(item[i]))
                elif isinstance(item[i], AST): 
                    dtypes.append(item[i])
                i += 1
            
        _dict = { k: v for k, v in cls.__dict__.items() }
        _dict['dtypes'] = dtypes
        _dict['base_type'] = cls
        _dict['predicate'] = predicate

        newcls = DependentType.__new__(self, self.__name__, (), _dict)
        
        return newcls

    def __getitem__(cls, item):
        return cls.__class_getitem__(cls, item)

class DependentType(Checkable,Subcriptable):

    def __new__(self, name, *subclasses):
        return super().__new__(self, name, *subclasses)
    
    def __init__(self, name, *subclasses, **dict) -> None:
        self.attrs = []

    def __ior__(self, attr):
        self.attrs.append(Attr(attr))
        return self

    def __ilshift__(self, predicate):
        self.predicate = predicate
        return self
