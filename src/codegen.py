from nodes import Number, Var, Unary, Binary, Assign, Print, Block

class CodeGen:
    """
    Simple 3-address style code generator.
    Generates pseudo-assembly like:

        t1 = 5
        t2 = 3
        t3 = t1 + t2
        x = t3
        print x
    """

    def __init__(self):
        self.temp_counter = 1

    def _new_temp(self) -> str:
        name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return name

    def generate(self, node: Block):
        # entry point – expect a Block
        lines = ["; BEGIN PROGRAM"]
        lines.extend(self._gen_block(node))
        lines.append("; END PROGRAM")
        return lines

    # ---------- statement helpers ----------

    def _gen_block(self, block: Block):
        lines = []
        for stmt in block.stmts:
            lines.extend(self._gen_stmt(stmt))
        return lines

    def _gen_stmt(self, stmt):
        # assignment: x = expr;
        if isinstance(stmt, Assign):
            expr_code, result_temp = self._gen_expr(stmt.expr)
            lines = list(expr_code)
            lines.append(f"{stmt.name} = {result_temp}")
            return lines

        # print(expr);
        if isinstance(stmt, Print):
            expr_code, result_temp = self._gen_expr(stmt.expr)
            lines = list(expr_code)
            lines.append(f"print {result_temp}")
            return lines

        raise RuntimeError(f"Unknown statement node in codegen: {stmt}")

    # ---------- expression helpers ----------

    def _gen_expr(self, expr):
        # returns (code_lines, result_temp_name)

        if isinstance(expr, Number):
            temp = self._new_temp()
            return [f"{temp} = {expr.value}"], temp

        if isinstance(expr, Var):
            # variables are just used directly as operands
            return [], expr.name

        if isinstance(expr, Unary):
            code, t = self._gen_expr(expr.right)
            temp = self._new_temp()
            if expr.op == '-':
                return code + [f"{temp} = -{t}"], temp
            elif expr.op == '+':
                return code + [f"{temp} = +{t}"], temp
            else:
                raise RuntimeError(f"Unknown unary op {expr.op!r}")

        if isinstance(expr, Binary):
            left_code, lt = self._gen_expr(expr.left)
            right_code, rt = self._gen_expr(expr.right)
            temp = self._new_temp()
            line = f"{temp} = {lt} {expr.op} {rt}"
            return left_code + right_code + [line], temp

        raise RuntimeError(f"Unknown expression node in codegen: {expr}")
