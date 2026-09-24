from flask import Blueprint, render_template, request, current_app

from utils.converters import convert_unit, convert_currency, calculate_bmi
from utils.validators import ValidationError, require_number
from utils.helpers import success_response, error_response, save_history

converter_bp = Blueprint("converter", __name__)


@converter_bp.route("/unit-converter")
def unit_converter_page():
    return render_template("unit_converter.html")


@converter_bp.route("/currency")
def currency_page():
    return render_template("currency.html")


@converter_bp.route("/bmi")
def bmi_page():
    return render_template("bmi.html")


@converter_bp.route("/convert", methods=["POST"])
def convert():
    data = request.get_json(silent=True) or {}
    try:
        category = data.get("category", "")
        value = require_number(data.get("value", 0), "value")
        from_unit = data.get("from_unit", "")
        to_unit = data.get("to_unit", "")
        result = convert_unit(category, value, from_unit, to_unit)
    except ValidationError as exc:
        return error_response(str(exc))

    expression = f"{value} {from_unit} -> {to_unit}"
    save_history("unit_converter", expression, result)
    return success_response({"result": result})


@converter_bp.route("/currency", methods=["POST"])
def currency_convert():
    data = request.get_json(silent=True) or {}
    try:
        amount = require_number(data.get("amount", 0), "amount")
        from_currency = data.get("from_currency", "")
        to_currency = data.get("to_currency", "")
        api_key = current_app.config.get("EXCHANGE_RATE_API_KEY", "")
        result = convert_currency(amount, from_currency, to_currency, api_key)
    except ValidationError as exc:
        return error_response(str(exc))

    expression = f"{amount} {from_currency} -> {to_currency}"
    save_history("currency", expression, result["converted"])
    return success_response(result)


@converter_bp.route("/bmi", methods=["POST"])
def bmi_calculate():
    data = request.get_json(silent=True) or {}
    try:
        weight = require_number(data.get("weight_kg", 0), "weight_kg")
        height = require_number(data.get("height_cm", 0), "height_cm")
        result = calculate_bmi(weight, height)
    except ValidationError as exc:
        return error_response(str(exc))

    expression = f"weight={weight}kg, height={height}cm"
    save_history("bmi", expression, f"{result['bmi']} ({result['category']})")
    return success_response(result)
