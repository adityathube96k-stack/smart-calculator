from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from database.database import db
from database.models import History, Favorite
from utils.helpers import success_response, error_response

history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
@login_required
def history_page():
    entries = (
        History.query.filter_by(user_id=current_user.id)
        .order_by(History.created_at.desc())
        .limit(100)
        .all()
    )
    return render_template("history.html", entries=entries)


@history_bp.route("/history", methods=["GET"])
@login_required
def history_api():
    entries = (
        History.query.filter_by(user_id=current_user.id)
        .order_by(History.created_at.desc())
        .limit(100)
        .all()
    )
    return success_response([e.to_dict() for e in entries])


@history_bp.route("/history/clear", methods=["POST"])
@login_required
def clear_history():
    History.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return success_response({"cleared": True})


@history_bp.route("/favorites", methods=["POST"])
@login_required
def toggle_favorite():
    data = request.get_json(silent=True) or {}
    name = data.get("calculator_name", "")
    if not name:
        return error_response("calculator_name is required.")

    existing = Favorite.query.filter_by(user_id=current_user.id, calculator_name=name).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return success_response({"favorited": False})

    db.session.add(Favorite(user_id=current_user.id, calculator_name=name))
    db.session.commit()
    return success_response({"favorited": True})


@history_bp.route("/settings")
@login_required
def settings_page():
    return render_template("settings.html")
