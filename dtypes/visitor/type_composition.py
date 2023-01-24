from .generic import GenericVisitor, visualizer
from ranges import Range, RangeSet
from copy import deepcopy

class CheckTypeComposition(GenericVisitor):

    @visualizer()
    def visit(self, dtype, ctx={}):
        return super().visit(dtype, ctx)

    # def visit_Lambda(self, dtype: ast.Lambda, ctx={}):
    #     for arg in dtype.args.args:
    #         ctx[arg.arg] = { }
    #     return self.visit(dtype.body, ctx)

    # def visit_Compare(self, dtype: ast.Compare, ctx={}):

    #     if isinstance(dtype.left, ast.Attribute):
    #         ##print(ast.dump(dtype))
    #         if isinstance(dtype.comparators[0], ast.Constant):
                
    #             if dtype.left.attr not in ctx[dtype.left.value.id]:
    #                 ctx[dtype.left.value.id][dtype.left.attr] = Range(-oo,oo)

    #             if isinstance(dtype.ops[0], ast.Lt):
    #                 if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                     and isinstance(dtype.comparators[0].op, ast.USub):
    #                     rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=False)
    #                 elif isinstance(dtype.comparators[0], ast.Constant):
    #                     rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=False)
    #                 ctx[dtype.left.value.id][dtype.left.attr] &= rng

    #             elif isinstance(dtype.ops[0], ast.LtE):
    #                 if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                     and isinstance(dtype.comparators[0].op, ast.USub):
    #                     rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=True)
    #                 elif isinstance(dtype.comparators[0], ast.Constant):
    #                     rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=True)
    #                 ctx[dtype.left.value.id][dtype.left.attr] &= rng

    #             elif isinstance(dtype.ops[0], ast.Gt):
    #                 if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                     and isinstance(dtype.comparators[0].op, ast.USub):
    #                     rng = Range(-dtype.comparators[0].operand.value, oo, include_start=False, include_end=False)
    #                 elif isinstance(dtype.comparators[0], ast.Constant):
    #                     rng = Range(dtype.comparators[0].value, oo, include_start=False, include_end=False)
    #                 ctx[dtype.left.value.id][dtype.left.attr] &= rng

    #             elif isinstance(dtype.ops[0], ast.GtE):
    #                 if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                     and isinstance(dtype.comparators[0].op, ast.USub):
    #                     rng = Range(-dtype.comparators[0].operand.value, oo, include_start=True, include_end=False)
    #                 elif isinstance(dtype.comparators[0], ast.Constant):
    #                     rng = Range(dtype.comparators[0].value, oo, include_start=True, include_end=False)
    #                 ctx[dtype.left.value.id][dtype.left.attr] &= rng

    #     elif isinstance(dtype.left, ast.Name):

    #         if "range" not in ctx[dtype.left.id]:
    #             ctx[dtype.left.id]["range"] = Range(-oo,oo)

    #         if isinstance(dtype.ops[0], ast.Lt):
    #             if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                 and isinstance(dtype.comparators[0].op, ast.USub):
    #                 rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=False)
    #             elif isinstance(dtype.comparators[0], ast.Constant):
    #                 rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=False)
    #             ctx[dtype.left.id]["range"] &= rng

    #         elif isinstance(dtype.ops[0], ast.LtE):
    #             if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                 and isinstance(dtype.comparators[0].op, ast.USub):
    #                 rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=True)
    #             elif isinstance(dtype.comparators[0], ast.Constant):
    #                 rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=True)
    #             ctx[dtype.left.id]["range"] &= rng

    #         elif isinstance(dtype.ops[0], ast.Gt):
    #             if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                 and isinstance(dtype.comparators[0].op, ast.USub):
    #                 rng = Range(-dtype.comparators[0].operand.value, oo, include_start=False, include_end=False)
    #             elif isinstance(dtype.comparators[0], ast.Constant):
    #                 rng = Range(dtype.comparators[0].value, oo, include_start=False, include_end=False)
    #             ctx[dtype.left.id]["range"] &= rng

    #         elif isinstance(dtype.ops[0], ast.GtE):
    #             if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                 and isinstance(dtype.comparators[0].op, ast.USub):
    #                 rng = Range(-dtype.comparators[0].operand.value, oo, include_start=True, include_end=False)
    #             elif isinstance(dtype.comparators[0], ast.Constant):
    #                 rng = Range(dtype.comparators[0].value, oo, include_start=True, include_end=False)
    #             ctx[dtype.left.id]["range"] &= rng

    #     elif isinstance(dtype.left, ast.Constant):

    #         if isinstance(dtype.comparators[0], ast.Attribute):
    #             ... #TODO
            
    #         elif isinstance(dtype.comparators[0], ast.Name):

    #             if "range" not in ctx[dtype.comparators[0].id]:
    #                 ctx[dtype.comparators[0].id]["range"] = Range(-oo,oo)

    #             if isinstance(dtype.ops[0], ast.Gt):
    #                 if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                     and isinstance(dtype.comparators[0].op, ast.USub):
    #                     rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=False)
    #                 elif isinstance(dtype.comparators[0], ast.Constant):
    #                     rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=False)
    #                 ctx[dtype.comparators[0].id]["range"] &= rng

    #             elif isinstance(dtype.ops[0], ast.GtE):
    #                 if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                     and isinstance(dtype.comparators[0].op, ast.USub):
    #                     rng = Range(-oo, -dtype.comparators[0].operand.value, include_start=False, include_end=True)
    #                 elif isinstance(dtype.comparators[0], ast.Constant):
    #                     rng = Range(-oo, dtype.comparators[0].value, include_start=False, include_end=True)
    #                 ctx[dtype.comparators[0].id]["range"] &= rng

    #             elif isinstance(dtype.ops[0], ast.Lt):
    #                 if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                     and isinstance(dtype.comparators[0].op, ast.USub):
    #                     rng = Range(-dtype.comparators[0].operand.value, oo, include_start=False, include_end=False)
    #                 elif isinstance(dtype.comparators[0], ast.Constant):
    #                     rng = Range(dtype.comparators[0].value, oo, include_start=False, include_end=False)
    #                 ctx[dtype.comparators[0].id]["range"] &= rng

    #             elif isinstance(dtype.ops[0], ast.LtE):
    #                 if isinstance(dtype.comparators[0], ast.UnaryOp) \
    #                     and isinstance(dtype.comparators[0].op, ast.USub):
    #                     rng = Range(-dtype.comparators[0].operand.value, oo, include_start=True, include_end=False)
    #                 elif isinstance(dtype.comparators[0], ast.Constant):
    #                     rng = Range(dtype.comparators[0].value, oo, include_start=True, include_end=False)
    #                 ctx[dtype.comparators[0].id]["range"] &= rng

    # def visit_BoolOp(self, dtype: ast.BoolOp, ctx={}):
    #     if isinstance(dtype.op, ast.And):
    #         for value in dtype.values:
    #             self.visit(value, ctx)
    #     elif isinstance(dtype.op, ast.Or):
    #         rngs = RangeSet()
    #         first = True
    #         for value in dtype.values:
    #             tmp_ctx = deepcopy(ctx)
    #             self.visit(value, tmp_ctx)
    #             if first:
    #                 rngs = RangeSet(tmp_ctx["x"]["range"])
    #                 first = False
    #             else:
    #                 rngs.add(tmp_ctx["x"]["range"])
    #         ctx["x"]["range"] = rngs._ranges.first.value
