import re
from datetime import datetime


class ValidationError(ValueError):
    """Raised when user input fails validation."""


def require_number(value, field_name="value"):
    """Convert to float, raising a friendly error on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"'{field_name}' must be a valid number.")


def require_positive(value, field_name="value"):
    num = require_number(value, field_name)
    if num <= 0:
        raise ValidationError(f"'{field_name}' must be greater than zero.")
    return num


def require_non_negative(value, field_name="value"):
    num = require_number(value, field_name)
    if num < 0:
        raise ValidationError(f"'{field_name}' cannot be negative.")
    return num


def require_date(value, field_name="date", fmt="%Y-%m-%d"):
    try:
        return datetime.strptime(value, fmt).date()
    except (TypeError, ValueError):
        raise ValidationError(f"'{field_name}' must be a valid date in {fmt} format.")


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require_email(value):
    if not value or not EMAIL_RE.match(value):
        raise ValidationError("A valid email address is required.")
    return value.strip().lower()


def require_password(value, min_length=8):
    if not value or len(value) < min_length:
        raise ValidationError(f"Password must be at least {min_length} characters.")
    return value


def sanitize_expression(expr, allowed_chars="0123456789+-*/().% "):
    """Whitelist-only check for basic calculator expressions to block code injection."""
    if not expr or not all(ch in allowed_chars for ch in expr):
        raise ValidationError("Expression contains invalid characters.")
    return expr
