from flask import Blueprint, render_template, request

from utils.calculator import scientific_calculate
from utils.validators import ValidationError, require_number
from utils.helpers import success_response, error_response, save_history

scientific_bp = Blueprint("scientific", __name__)


@scientific_bp.route("/scientific")
def scientific_page():
    return render_template("scientific.html")


@scientific_bp.route("/scientific", methods=["POST"])
def scientific():
    data = request.get_json(silent=True) or {}
    operation = data.get("operation", "")

    try:
        value = require_number(data.get("value", 0), "value")
        value2 = data.get("value2")
        value2 = require_number(value2, "value2") if value2 is not None else None
        result = scientific_calculate(operation, value, value2)
    except ValidationError as exc:
        return error_response(str(exc))

    expression = f"{operation}({value}{', ' + str(value2) if value2 is not None else ''})"
    save_history("scientific", expression, result)
    return success_response({"expression": expression, "result": result})
