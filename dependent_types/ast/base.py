from abc import abstractmethod

# VISUALIZE = True
VISUALIZE = False

def visualizer(fn):
    def inner(*args):
        if VISUALIZE:
            print('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(f'\nFUNCTION {fn.__name__.upper()}\n\n')
            print(f'ARGS:\n')
            for arg in args:
                print(f'TYPEOF({arg})={type(arg)}') 
                print(f'dict({arg})={arg.__dict__}\n')
        result = fn(*args)
        if VISUALIZE:
            print(f'\n\nRESULT ==> {result}\n\n')
            print(f'\nENDED {fn.__name__.upper()}\n\n')
        return result
    return inner

class AST(type):
    @abstractmethod
    def eval(self):...