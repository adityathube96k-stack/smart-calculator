from datetime import datetime, time as dtime
from flask import Blueprint, render_template, request

from utils.age import calculate_age, date_difference
from utils.validators import ValidationError, require_date
from utils.helpers import success_response, error_response, save_history

age_bp = Blueprint("age", __name__)


@age_bp.route("/age")
def age_page():
    return render_template("age.html")


@age_bp.route("/age", methods=["POST"])
def age():
    data = request.get_json(silent=True) or {}

    try:
        birth_date = require_date(data.get("date_of_birth", ""), "date_of_birth")
        birth_time_str = data.get("birth_time")
        birth_time = None
        if birth_time_str:
            try:
                birth_time = datetime.strptime(birth_time_str, "%H:%M").time()
            except ValueError:
                raise ValidationError("birth_time must be in HH:MM format.")

        result = calculate_age(birth_date, birth_time or dtime(0, 0))
    except ValidationError as exc:
        return error_response(str(exc))

    save_history("age", birth_date.isoformat(), f"{result['years']}y {result['months']}m {result['days']}d")
    return success_response(result)


@age_bp.route("/date-difference")
def date_difference_page():
    return render_template("date_difference.html")


@age_bp.route("/date", methods=["POST"])
def date_diff():
    data = request.get_json(silent=True) or {}

    try:
        start = require_date(data.get("start_date", ""), "start_date")
        end = require_date(data.get("end_date", ""), "end_date")
        result = date_difference(start, end)
    except ValidationError as exc:
        return error_response(str(exc))

    expression = f"{start.isoformat()} to {end.isoformat()}"
    save_history("date_difference", expression, f"{result['total_days']} days")
    return success_response(result)


@age_bp.route("/time-calculator")
def time_page():
    return render_template("time.html")


@age_bp.route("/time", methods=["POST"])
def time_calc():
    """Add or subtract durations from a given time (HH:MM:SS)."""
    data = request.get_json(silent=True) or {}
    try:
        base = datetime.strptime(data.get("base_time", ""), "%H:%M:%S")
        hours = int(data.get("hours", 0))
        minutes = int(data.get("minutes", 0))
        seconds = int(data.get("seconds", 0))
        operation = data.get("operation", "add")
    except (TypeError, ValueError):
        return error_response("Invalid time input. Use HH:MM:SS and integer offsets.")

    from datetime import timedelta
    delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    result_time = base + delta if operation == "add" else base - delta

    formatted = result_time.strftime("%H:%M:%S")
    save_history("time", data.get("base_time", ""), formatted)
    return success_response({"result_time": formatted})
