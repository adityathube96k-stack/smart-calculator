from flask import Blueprint, render_template, request

from utils.calculator import evaluate_expression
from utils.validators import ValidationError
from utils.helpers import success_response, error_response, save_history

calculator_bp = Blueprint("calculator", __name__)


@calculator_bp.route("/calculator")
def calculator_page():
    return render_template("calculator.html")


@calculator_bp.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}
    expression = data.get("expression", "")

    try:
        result = evaluate_expression(expression)
    except ValidationError as exc:
        return error_response(str(exc))

    save_history("basic", expression, result)
    return success_response({"expression": expression, "result": result})
