from abc import abstractmethod

VISUALIZE = True
# VISUALIZE = False

def visualizer(fn):
    def inner(*args):
        if VISUALIZE:
            print('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(f'\nFUNCTION {fn.__name__.upper()}\n\n')
            print(f'ARGS:\n')
            for arg in args:
                ...
                print(f'TYPEOF({arg})={type(arg)}') 
                print(f'dict({arg})={arg.__dict__}\n')
        result = fn(*args)
        if VISUALIZE:
            ...
            print(f'\n\nRESULT ==> {result}\n\n')
            print(f'\nENDED {fn.__name__.upper()}\n\n')
        return result
    return inner

class AST(type):

    def __new__(cls, name, *subclasses, **dict):
        dict = { '_fields': { } }
        return super().__new__(cls, name, subclasses, dict)

    def __getattr__(self, __field):
        return self.__dict__['_fields'][__field]

    def __setattr__(self, __name: str, __value):
        self.__dict__['_fields'][__name] = __value

    @abstractmethod
    def eval(self):...
