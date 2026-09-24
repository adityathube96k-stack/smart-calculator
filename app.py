import os
import logging

from flask import Flask, render_template
from flask_login import LoginManager
from dotenv import load_dotenv

from config import config_by_name
from database.database import db, init_db
from database.models import User

load_dotenv()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app(env_name=None):
    app = Flask(__name__)

    env_name = env_name or os.environ.get("FLASK_ENV", "production")
    app.config.from_object(config_by_name[env_name])

    if env_name == "production":
        config_by_name["production"].validate()

    # --- Extensions ---
    init_db(app)
    login_manager.init_app(app)

    # --- Blueprints ---
    from routes.calculator import calculator_bp
    from routes.scientific import scientific_bp
    from routes.age import age_bp
    from routes.converter import converter_bp
    from routes.finance import finance_bp
    from routes.auth import auth_bp
    from routes.history import history_bp

    app.register_blueprint(calculator_bp)
    app.register_blueprint(scientific_bp)
    app.register_blueprint(age_bp)
    app.register_blueprint(converter_bp)
    app.register_blueprint(finance_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(history_bp)

    # --- Logging ---
    # File logging fails on Vercel's read-only filesystem; use stream logging instead
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
        )
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)

    # --- Error handlers ---
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.exception("Internal server error")
        return render_template("500.html"), 500

    # --- Home ---
    @app.route("/")
    def index():
        return render_template("index.html")

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Top-level 'app' instance required by Vercel:
app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))