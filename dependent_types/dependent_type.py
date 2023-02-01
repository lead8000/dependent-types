from dependent_types.ast import AST, BitOr, Constant
from dependent_types.visitor import TypeInference
from copy import deepcopy


class Checkable(type):

    def __instancecheck__(self, instance) -> bool:

        for dict in self.__contraints__:
            for attr in self.__dependent_attrs__:
                if not dict.__contains__(attr, instance.__getattribute__(attr)):
                    break
            else:
                return True

        return False

    def __subclasscheck__(self, __subclass) -> bool:

        if self.__name__ != "DependentType" and \
        __subclass.__name__ != "DependentType":
            for cls in self.mro():
                if cls == __subclass:
                    return True
            return False

        if not issubclass(self.__base_type__, __subclass.__base_type__):
            return False

        contraints_a = __subclass.__contraints__
        contraints_b = self.__contraints__

        for dict_a in contraints_a:
            for dict_b in contraints_b:
                u = dict_a | dict_b
                if dict_b == u:
                    break
            else:
                return False                    

        return True

class Subcriptable(type):

    def __class_getitem__(self, cls, item) -> 'DependentType':
        dependent_attrs = []
        contraint = None
        
        if isinstance(item, BitOr):
            dependent_attrs.append(item.left)
            contraint = item.right
        else:
            for token in item:
                if isinstance(token, BitOr):
                    dependent_attrs.append(token.left)
                    contraint = token.right
                elif isinstance(token, (int,float)):
                    dependent_attrs.append(Constant(token))
                elif isinstance(token, AST): 
                    dependent_attrs.append(token)
        
        if len(dependent_attrs) != len(cls.__dependent_attrs__):
            raise Exception("Missing or excess of dependent attributes.")

        _dict = { name: deepcopy(func) for name, func in cls.__dict__.items() 
            if name not in ('__module__', '__weakref__', '__dict__') }
        _dict['__base_type__'] = cls
        _dict['__contraints__'] = contraint

        dtype = DependentType.__new__(self, self.__name__, (), _dict)

        ctx = { 'dependent_attrs': deepcopy(cls.__dependent_attrs__), 'contraints': [] }

        if contraint:

            ctx_result = TypeInference().visit(dtype.__contraints__, ctx)

            print(f'\n\n\n{ctx_result["contraints"]}\n')

            if ctx_result['contraints']:
                dtype.__contraints__ = ctx_result['contraints']
            else:
                raise Exception("The dependent type expresses an inconsistent state.")
        
        return dtype

    def __getitem__(cls, item):
        return cls.__class_getitem__(cls, item)

class DependentType(Checkable,Subcriptable):

    def __new__(self, name, *subclasses):
        return super().__new__(self, name, *subclasses)
    
    def __init__(self, name, *subclasses, **dict) -> None:
        self.__dependent_attrs__ = set()

    def __ior__(self, attr):
        self.__dependent_attrs__.add(attr)
        return self
