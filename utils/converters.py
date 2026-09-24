import requests
from utils.validators import ValidationError, require_positive

# --- Unit conversion ---
# Each category stores conversion factors relative to a base unit.

LENGTH_TO_METERS = {
    "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
    "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.34,
}

WEIGHT_TO_GRAMS = {
    "mg": 0.001, "g": 1, "kg": 1000, "ton": 1_000_000,
    "oz": 28.3495, "lb": 453.592,
}

TEMP_UNITS = {"c", "f", "k"}


def convert_length(value, from_unit, to_unit):
    if from_unit not in LENGTH_TO_METERS or to_unit not in LENGTH_TO_METERS:
        raise ValidationError("Unsupported length unit.")
    meters = value * LENGTH_TO_METERS[from_unit]
    return meters / LENGTH_TO_METERS[to_unit]


def convert_weight(value, from_unit, to_unit):
    if from_unit not in WEIGHT_TO_GRAMS or to_unit not in WEIGHT_TO_GRAMS:
        raise ValidationError("Unsupported weight unit.")
    grams = value * WEIGHT_TO_GRAMS[from_unit]
    return grams / WEIGHT_TO_GRAMS[to_unit]


def convert_temperature(value, from_unit, to_unit):
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    if from_unit not in TEMP_UNITS or to_unit not in TEMP_UNITS:
        raise ValidationError("Unsupported temperature unit.")

    # Normalize to Celsius first
    if from_unit == "f":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "k":
        celsius = value - 273.15
    else:
        celsius = value

    if to_unit == "f":
        return celsius * 9 / 5 + 32
    if to_unit == "k":
        return celsius + 273.15
    return celsius


UNIT_CONVERTERS = {
    "length": convert_length,
    "weight": convert_weight,
    "temperature": convert_temperature,
}


def convert_unit(category, value, from_unit, to_unit):
    if category not in UNIT_CONVERTERS:
        raise ValidationError(f"Unsupported category: {category}")
    return round(UNIT_CONVERTERS[category](value, from_unit, to_unit), 6)


# --- BMI ---

def calculate_bmi(weight_kg, height_cm):
    weight_kg = require_positive(weight_kg, "weight")
    height_cm = require_positive(height_cm, "height")
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {"bmi": round(bmi, 2), "category": category}


# --- Currency conversion ---

def convert_currency(amount, from_currency, to_currency, api_key=""):
    amount = require_positive(amount, "amount")
    from_currency, to_currency = from_currency.upper(), to_currency.upper()

    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        rates = resp.json().get("rates", {})
    except requests.RequestException:
        raise ValidationError("Currency service is currently unavailable. Please try again later.")

    if to_currency not in rates:
        raise ValidationError(f"Unsupported currency: {to_currency}")

    rate = rates[to_currency]
    return {"rate": rate, "converted": round(amount * rate, 4)}
