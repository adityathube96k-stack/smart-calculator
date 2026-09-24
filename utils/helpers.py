from flask import jsonify
from flask_login import current_user

from database.database import db
from database.models import History


def success_response(data, status=200):
    return jsonify({"success": True, "data": data}), status


def error_response(message, status=400):
    return jsonify({"success": False, "error": message}), status


def save_history(calculator: str, expression: str, result: str):
    """Save a calculation to history if the user is logged in. No-op for guests."""
    if not current_user.is_authenticated:
        return
    entry = History(
        user_id=current_user.id,
        calculator=calculator,
        expression=expression,
        result=str(result),
    )
    db.session.add(entry)
    db.session.commit()
