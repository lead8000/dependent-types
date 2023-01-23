import ast
from copy import deepcopy
from ranges import Inf as oo
from functools import reduce
from metaclass import LengthVar
from ranges import Range, RangeSet

def visualizer(func):

    def decorator(_, node, ctx = {}):        
        #print(f'\n<--- {node.__class__.__name__.upper()} --->\n\nCONTEXT: {ctx}\n')
        #print(f'{ast.dump(node)}')
        func(_, node, ctx)
    
    return decorator

class GenericVisitor(ast.NodeVisitor):

    def visit(self, node, ctx = {}):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, ctx)

    def generic_visit(self, node, ctx = {}):
        """Called if no explicit visitor function exists for a node."""
        for _, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, ctx)
            elif isinstance(value, ast.AST):
                self.visit(value, ctx)
    
    def visit_Constant(self, node: ast.Constant, ctx = {}):
        value = node.value
        type_name = ast._const_node_type_names.get(type(value))
        if type_name is None:
            for cls, name in ast._const_node_type_names.items():
                if isinstance(value, cls):
                    type_name = name
                    break
        if type_name is not None:
            method = 'visit_' + type_name
            try:
                visitor = getattr(self, method)
            except AttributeError:
                pass
            else:
                import warnings
                warnings.warn(f"{method} is deprecated; add visit_Constant",
                              DeprecationWarning, 2)
                return visitor(node, ctx)
        return self.generic_visit(node, ctx) 

class Visitor(GenericVisitor):

    @visualizer
    def visit_FunctionDef(self, node: ast.FunctionDef, ctx = {}):
        childCtx = deepcopy(ctx)
        if reduce( # check if function is an axiom
            lambda Bool, dec: Bool or dec.id == 'axiom', 
            node.decorator_list, 
            False):
            if 'axioms' not in ctx:
                ctx['axioms'] = set()
            ctx['axioms'].add(node.name)
        else:
            if 'unchecked' not in ctx:
                ctx['unchecked'] = set()
            ctx['unchecked'].add(node.name)
            for arg in node.args.args:
                dtype = childCtx[f'{arg.annotation.slice.id}']
                childCtx[arg.arg] = deepcopy(dtype) 
            #print(ast.dump(node))
            #print(ctx)    

        #print()

        return self.generic_visit(node, childCtx)

    @visualizer
    def visit_For(self, node: ast.For, ctx = {}):
        for _node in node.body:
            if isinstance(_node, ast.Assign):
                ctx['numberOfTimes'] = ctx[node.iter.id]
            #print(f'{ctx[node.iter.id]} veces --- ', ast.dump(_node))
            #print(_node.targets)
        #print()
        return self.generic_visit(node, ctx)

    @visualizer
    def visit_Assign(self, node: ast.Assign, ctx = {}):
        if node.value.func.id == 'LengthVar':
            lenVar = eval(f'LengthVar(\'{node.value.args[0].value}\')')
            varName=f'{node.targets[0].id}'
            ctx[varName] = lenVar
        else: 
            # check if there is cyclic dependency
            varAssign = node.targets[0].id
            if varAssign in [arg.id for arg in node.value.args]:
                numberOfTimes = LengthVar('1')
                # check if it executes various times
                if 'numberOfTimes' in ctx:
                    numberOfTimes = ctx['numberOfTimes']
                    if isinstance(ctx['numberOfTimes'], str):
                        numberOfTimes = ctx[numberOfTimes] 
                    # ctx.__delattr__('numberOfTimes')
                ctx[varAssign] = ctx[varAssign] + numberOfTimes
                #print(ctx)

        #print()
        return self.generic_visit(node, ctx)

    @visualizer
    def visit_Return(self, node: ast.Return, ctx = {}):
        return self.generic_visit(node, ctx)

class CheckTypeComposition(GenericVisitor):

    # @visualizer
    def visit(self, dtype, ctx={}):
        return super().visit(dtype, ctx)

    def visit_Lambda(self, dtype: ast.Lambda, ctx={}):
        for arg in dtype.args.args:
            ctx[arg.arg] = { }
        return self.visit(dtype.body, ctx)

    def visit_Compare(self, dtype: ast.Compare, ctx={}):

        if isinstance(dtype.left, ast.Attribute):
            #print(ast.dump(dtype))
            if isinstance(dtype.comparators[0], ast.Constant):
                
                if dtype.left.attr not in ctx[dtype.left.value.id]:
                    ctx[dtype.left.value.id][dtype.left.attr] = Range(-oo,oo)

                if isinstance(dtype.ops[0], ast.Lt):
                    if isinstance(dtype.comparators[0], ast.UnaryOp) \
                        and isinstance(dtype.comparators[0].op, ast.USub):
                        rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=False)
                    elif isinstance(dtype.comparators[0], ast.Constant):
                        rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=False)
                    ctx[dtype.left.value.id][dtype.left.attr] &= rng

                elif isinstance(dtype.ops[0], ast.LtE):
                    if isinstance(dtype.comparators[0], ast.UnaryOp) \
                        and isinstance(dtype.comparators[0].op, ast.USub):
                        rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=True)
                    elif isinstance(dtype.comparators[0], ast.Constant):
                        rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=True)
                    ctx[dtype.left.value.id][dtype.left.attr] &= rng

                elif isinstance(dtype.ops[0], ast.Gt):
                    if isinstance(dtype.comparators[0], ast.UnaryOp) \
                        and isinstance(dtype.comparators[0].op, ast.USub):
                        rng = Range(-dtype.comparators[0].operand.value, oo, include_start=False, include_end=False)
                    elif isinstance(dtype.comparators[0], ast.Constant):
                        rng = Range(dtype.comparators[0].value, oo, include_start=False, include_end=False)
                    ctx[dtype.left.value.id][dtype.left.attr] &= rng

                elif isinstance(dtype.ops[0], ast.GtE):
                    if isinstance(dtype.comparators[0], ast.UnaryOp) \
                        and isinstance(dtype.comparators[0].op, ast.USub):
                        rng = Range(-dtype.comparators[0].operand.value, oo, include_start=True, include_end=False)
                    elif isinstance(dtype.comparators[0], ast.Constant):
                        rng = Range(dtype.comparators[0].value, oo, include_start=True, include_end=False)
                    ctx[dtype.left.value.id][dtype.left.attr] &= rng

        elif isinstance(dtype.left, ast.Name):

            if "range" not in ctx[dtype.left.id]:
                ctx[dtype.left.id]["range"] = Range(-oo,oo)

            if isinstance(dtype.ops[0], ast.Lt):
                if isinstance(dtype.comparators[0], ast.UnaryOp) \
                    and isinstance(dtype.comparators[0].op, ast.USub):
                    rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=False)
                elif isinstance(dtype.comparators[0], ast.Constant):
                    rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=False)
                ctx[dtype.left.id]["range"] &= rng

            elif isinstance(dtype.ops[0], ast.LtE):
                if isinstance(dtype.comparators[0], ast.UnaryOp) \
                    and isinstance(dtype.comparators[0].op, ast.USub):
                    rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=True)
                elif isinstance(dtype.comparators[0], ast.Constant):
                    rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=True)
                ctx[dtype.left.id]["range"] &= rng

            elif isinstance(dtype.ops[0], ast.Gt):
                if isinstance(dtype.comparators[0], ast.UnaryOp) \
                    and isinstance(dtype.comparators[0].op, ast.USub):
                    rng = Range(-dtype.comparators[0].operand.value, oo, include_start=False, include_end=False)
                elif isinstance(dtype.comparators[0], ast.Constant):
                    rng = Range(dtype.comparators[0].value, oo, include_start=False, include_end=False)
                ctx[dtype.left.id]["range"] &= rng

            elif isinstance(dtype.ops[0], ast.GtE):
                if isinstance(dtype.comparators[0], ast.UnaryOp) \
                    and isinstance(dtype.comparators[0].op, ast.USub):
                    rng = Range(-dtype.comparators[0].operand.value, oo, include_start=True, include_end=False)
                elif isinstance(dtype.comparators[0], ast.Constant):
                    rng = Range(dtype.comparators[0].value, oo, include_start=True, include_end=False)
                ctx[dtype.left.id]["range"] &= rng

        elif isinstance(dtype.left, ast.Constant):

            if isinstance(dtype.comparators[0], ast.Attribute):
                ... #TODO
            
            elif isinstance(dtype.comparators[0], ast.Name):

                if "range" not in ctx[dtype.comparators[0].id]:
                    ctx[dtype.comparators[0].id]["range"] = Range(-oo,oo)

                if isinstance(dtype.ops[0], ast.Gt):
                    if isinstance(dtype.comparators[0], ast.UnaryOp) \
                        and isinstance(dtype.comparators[0].op, ast.USub):
                        rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=False)
                    elif isinstance(dtype.comparators[0], ast.Constant):
                        rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=False)
                    ctx[dtype.comparators[0].id]["range"] &= rng

                elif isinstance(dtype.ops[0], ast.GtE):
                    if isinstance(dtype.comparators[0], ast.UnaryOp) \
                        and isinstance(dtype.comparators[0].op, ast.USub):
                        rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=True)
                    elif isinstance(dtype.comparators[0], ast.Constant):
                        rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=True)
                    ctx[dtype.comparators[0].id]["range"] &= rng

                elif isinstance(dtype.ops[0], ast.Lt):
                    if isinstance(dtype.comparators[0], ast.UnaryOp) \
                        and isinstance(dtype.comparators[0].op, ast.USub):
                        rng = Range(-dtype.comparators[0].operand.value, oo, include_start=False, include_end=False)
                    elif isinstance(dtype.comparators[0], ast.Constant):
                        rng = Range(dtype.comparators[0].value, oo, include_start=False, include_end=False)
                    ctx[dtype.comparators[0].id]["range"] &= rng

                elif isinstance(dtype.ops[0], ast.LtE):
                    if isinstance(dtype.comparators[0], ast.UnaryOp) \
                        and isinstance(dtype.comparators[0].op, ast.USub):
                        rng = Range(-dtype.comparators[0].operand.value, oo, include_start=True, include_end=False)
                    elif isinstance(dtype.comparators[0], ast.Constant):
                        rng = Range(dtype.comparators[0].value, oo, include_start=True, include_end=False)
                    ctx[dtype.comparators[0].id]["range"] &= rng

    def visit_BoolOp(self, dtype: ast.BoolOp, ctx={}):
        if isinstance(dtype.op, ast.And):
            for value in dtype.values:
                self.visit(value, ctx)
        elif isinstance(dtype.op, ast.Or):
            rngs = RangeSet()
            first = True
            for value in dtype.values:
                tmp_ctx = deepcopy(ctx)
                self.visit(value, tmp_ctx)
                if first:
                    rngs = RangeSet(tmp_ctx["x"]["range"])
                    first = False
                else:
                    rngs.add(tmp_ctx["x"]["range"])
            #print("!!!!!!!!!!!!!")
            #print(f'{rngs}')
            ctx["x"]["range"] = rngs._ranges.first.value
