from nodes import Number, Var, Unary, Binary, Assign, Print, Block

class Interpreter:
    def __init__(self):
        # variable environment: maps variable names -> integer values
        self.env = {}

    def eval(self, node):
        # BLOCK of statements
        if isinstance(node, Block):
            outputs = []
            for stmt in node.stmts:
                result = self.eval(stmt)
                if result is not None:
                    outputs.append(result)
            return outputs

        # ASSIGNMENT (x = expr;)
        if isinstance(node, Assign):
            value = self._eval_expr(node.expr)
            self.env[node.name] = value
            return None

        # PRINT (print(expr);)
        if isinstance(node, Print):
            value = self._eval_expr(node.expr)
            return str(value)

        raise RuntimeError(f"Unknown statement node: {node}")

    # ---------------- EXPRESSIONS ----------------

    def _eval_expr(self, expr):
        # number literal
        if isinstance(expr, Number):
            return expr.value

        # variable reference
        if isinstance(expr, Var):
            if expr.name not in self.env:
                raise RuntimeError(f"Undefined variable '{expr.name}'")
            return self.env[expr.name]

        # unary operator (+ or -)
        if isinstance(expr, Unary):
            value = self._eval_expr(expr.right)
            if expr.op == '-':
                return -value
            if expr.op == '+':
                return value

        # binary operator (+ - * /)
        if isinstance(expr, Binary):
            left = self._eval_expr(expr.left)
            right = self._eval_expr(expr.right)

            if expr.op == '+':
                return left + right
            if expr.op == '-':
                return left - right
            if expr.op == '*':
                return left * right
            if expr.op == '/':
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left // right  # integer division

        raise RuntimeError(f"Unknown expression node: {expr}")
