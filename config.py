import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

# On Vercel, the filesystem is read-only except for /tmp
if os.environ.get("VERCEL"):
    default_db_uri = "sqlite:////tmp/smartcalculator.db"
    default_log_file = "/tmp/app.log"
else:
    default_db_uri = f"sqlite:///{os.path.join(basedir, 'instance', 'smartcalculator.db')}"
    default_log_file = os.path.join(basedir, "logs", "app.log")


class Config:
    """Base configuration shared by all environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default_db_uri)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    WTF_CSRF_ENABLED = True

    # Currency API (used by currency converter). Free tier key can be added via .env
    EXCHANGE_RATE_API_KEY = os.environ.get("EXCHANGE_RATE_API_KEY", "")

    LOG_FILE = default_log_file


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    @classmethod
    def validate(cls):
        if cls.SECRET_KEY == "dev-secret-key-change-me":
            raise RuntimeError(
                "SECRET_KEY must be set via environment variable in production."
            )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}