from flask import Blueprint, render_template, request

from utils.finance import (
    calculate_gst, calculate_emi, calculate_loan,
    calculate_sip, calculate_discount, calculate_profit_loss, calculate_percentage,
)
from utils.validators import ValidationError, require_number
from utils.helpers import success_response, error_response, save_history

finance_bp = Blueprint("finance", __name__)

# --- Page routes ---

@finance_bp.route("/gst")
def gst_page():
    return render_template("gst.html")


@finance_bp.route("/emi")
def emi_page():
    return render_template("emi.html")


@finance_bp.route("/loan")
def loan_page():
    return render_template("loan.html")


@finance_bp.route("/sip")
def sip_page():
    return render_template("sip.html")


@finance_bp.route("/discount")
def discount_page():
    return render_template("discount.html")


@finance_bp.route("/profit-loss")
def profit_loss_page():
    return render_template("profit_loss.html")


@finance_bp.route("/percentage")
def percentage_page():
    return render_template("percentage.html")


# --- API routes ---

@finance_bp.route("/gst", methods=["POST"])
def gst_api():
    data = request.get_json(silent=True) or {}
    try:
        amount = require_number(data.get("amount", 0), "amount")
        rate = require_number(data.get("gst_rate", 0), "gst_rate")
        mode = data.get("mode", "exclusive")
        result = calculate_gst(amount, rate, mode)
    except ValidationError as exc:
        return error_response(str(exc))
    save_history("gst", f"amount={amount}, rate={rate}%", result["total_amount"])
    return success_response(result)


@finance_bp.route("/emi", methods=["POST"])
def emi_api():
    data = request.get_json(silent=True) or {}
    try:
        principal = require_number(data.get("principal", 0), "principal")
        rate = require_number(data.get("annual_rate", 0), "annual_rate")
        tenure = require_number(data.get("tenure_months", 0), "tenure_months")
        result = calculate_emi(principal, rate, tenure)
    except ValidationError as exc:
        return error_response(str(exc))
    save_history("emi", f"P={principal}, R={rate}%, N={tenure}mo", result["emi"])
    return success_response(result)


@finance_bp.route("/loan", methods=["POST"])
def loan_api():
    data = request.get_json(silent=True) or {}
    try:
        principal = require_number(data.get("principal", 0), "principal")
        rate = require_number(data.get("annual_rate", 0), "annual_rate")
        tenure = require_number(data.get("tenure_years", 0), "tenure_years")
        result = calculate_loan(principal, rate, tenure)
    except ValidationError as exc:
        return error_response(str(exc))
    save_history("loan", f"P={principal}, R={rate}%, {tenure}yr", result["total_payable"])
    return success_response(result)


@finance_bp.route("/sip", methods=["POST"])
def sip_api():
    data = request.get_json(silent=True) or {}
    try:
        monthly = require_number(data.get("monthly_investment", 0), "monthly_investment")
        rate = require_number(data.get("annual_rate", 0), "annual_rate")
        tenure = require_number(data.get("tenure_years", 0), "tenure_years")
        result = calculate_sip(monthly, rate, tenure)
    except ValidationError as exc:
        return error_response(str(exc))
    save_history("sip", f"{monthly}/mo, {rate}%, {tenure}yr", result["future_value"])
    return success_response(result)


@finance_bp.route("/discount", methods=["POST"])
def discount_api():
    data = request.get_json(silent=True) or {}
    try:
        price = require_number(data.get("original_price", 0), "original_price")
        pct = require_number(data.get("discount_percent", 0), "discount_percent")
        result = calculate_discount(price, pct)
    except ValidationError as exc:
        return error_response(str(exc))
    save_history("discount", f"{price} @ {pct}% off", result["final_price"])
    return success_response(result)


@finance_bp.route("/profit-loss", methods=["POST"])
def profit_loss_api():
    data = request.get_json(silent=True) or {}
    try:
        cost = require_number(data.get("cost_price", 0), "cost_price")
        selling = require_number(data.get("selling_price", 0), "selling_price")
        result = calculate_profit_loss(cost, selling)
    except ValidationError as exc:
        return error_response(str(exc))
    save_history("profit_loss", f"CP={cost}, SP={selling}", f"{result['type']}: {result['amount']}")
    return success_response(result)


@finance_bp.route("/percentage", methods=["POST"])
def percentage_api():
    data = request.get_json(silent=True) or {}
    try:
        value = require_number(data.get("value", 0), "value")
        pct = require_number(data.get("percent", 0), "percent")
        result = calculate_percentage(value, pct)
    except ValidationError as exc:
        return error_response(str(exc))
    save_history("percentage", f"{pct}% of {value}", result["result"])
    return success_response(result)
