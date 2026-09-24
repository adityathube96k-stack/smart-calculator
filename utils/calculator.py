import ast
import math
import operator

from utils.validators import ValidationError, sanitize_expression

# --- Basic calculator: safe expression evaluation (no eval()) ---

_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValidationError("Invalid constant in expression.")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BIN_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        try:
            return _ALLOWED_BIN_OPS[type(node.op)](left, right)
        except ZeroDivisionError:
            raise ValidationError("Division by zero is not allowed.")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY_OPS:
        return _ALLOWED_UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise ValidationError("Expression contains an unsupported operation.")


def evaluate_expression(expr: str) -> float:
    """Safely evaluate a basic arithmetic expression like '12 * (3 + 4) / 2'."""
    expr = sanitize_expression(expr.replace("%", "/100"))
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        raise ValidationError("Invalid expression syntax.")
    result = _eval_node(tree.body)
    return round(result, 10)


# --- Scientific calculator ---

def scientific_calculate(operation: str, value, value2=None):
    ops = {
        "sqrt": lambda v: math.sqrt(v),
        "power": lambda v: v ** value2 if value2 is not None else None,
        "log": lambda v: math.log10(v),
        "ln": lambda v: math.log(v),
        "sin": lambda v: math.sin(math.radians(v)),
        "cos": lambda v: math.cos(math.radians(v)),
        "tan": lambda v: math.tan(math.radians(v)),
        "factorial": lambda v: math.factorial(int(v)),
        "pi": lambda v: math.pi,
        "e": lambda v: math.e,
    }

    if operation not in ops:
        raise ValidationError(f"Unsupported scientific operation: {operation}")

    try:
        result = ops[operation](value)
    except ValueError as exc:
        raise ValidationError(str(exc))

    if result is None:
        raise ValidationError("This operation requires a second value.")

    return round(result, 10)
