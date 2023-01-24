from dtypes.ast import AST

VISUALIZER = True
VISUALIZER = False

def visualizer(func):

    def decorator(_, node, ctx = {}):        
        if VISUALIZER:
            print(f'\n<--- {node.__class__.__name__.upper()} --->\n\nCONTEXT: {ctx}\n')
            print(f'{node._fields}')
        func(_, node, ctx)
    
    return decorator

def iter_fields(node):
    """
    Yield a tuple of ``(fieldname, value)`` for each field in ``node._fields``
    that is present on *node*.
    """
    for field in node._fields:
        try:
            yield field, getattr(node, field)
        except AttributeError:
            pass

class GenericVisitor:
    @visualizer
    def visit(self, node, ctx = {}):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, ctx)

    def generic_visit(self, node, ctx = {}):
        """Called if no explicit visitor function exists for a node."""
        for _, value in iter_fields(node):
            if isinstance(value, AST):
                self.visit(value, ctx)
