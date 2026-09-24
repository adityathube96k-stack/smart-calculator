from utils.validators import require_positive, require_non_negative, ValidationError


def calculate_gst(amount, gst_rate, mode="exclusive"):
    """mode='exclusive': amount is pre-GST. mode='inclusive': amount already includes GST."""
    amount = require_positive(amount, "amount")
    gst_rate = require_non_negative(gst_rate, "GST rate")

    if mode == "inclusive":
        base = amount / (1 + gst_rate / 100)
        gst_amount = amount - base
        total = amount
    else:
        gst_amount = amount * gst_rate / 100
        base = amount
        total = amount + gst_amount

    return {
        "base_amount": round(base, 2),
        "gst_amount": round(gst_amount, 2),
        "total_amount": round(total, 2),
    }


def calculate_emi(principal, annual_rate, tenure_months):
    principal = require_positive(principal, "principal")
    annual_rate = require_non_negative(annual_rate, "interest rate")
    tenure_months = int(require_positive(tenure_months, "tenure"))

    if annual_rate == 0:
        emi = principal / tenure_months
    else:
        monthly_rate = annual_rate / 12 / 100
        factor = (1 + monthly_rate) ** tenure_months
        emi = principal * monthly_rate * factor / (factor - 1)

    total_payment = emi * tenure_months
    total_interest = total_payment - principal

    return {
        "emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2),
    }


def calculate_loan(principal, annual_rate, tenure_years):
    """Simple-interest loan summary (distinct from amortizing EMI)."""
    principal = require_positive(principal, "principal")
    annual_rate = require_non_negative(annual_rate, "interest rate")
    tenure_years = require_positive(tenure_years, "tenure")

    total_interest = principal * annual_rate * tenure_years / 100
    total_payable = principal + total_interest

    return {
        "total_interest": round(total_interest, 2),
        "total_payable": round(total_payable, 2),
        "monthly_payment": round(total_payable / (tenure_years * 12), 2),
    }


def calculate_sip(monthly_investment, annual_rate, tenure_years):
    monthly_investment = require_positive(monthly_investment, "monthly investment")
    annual_rate = require_non_negative(annual_rate, "expected return rate")
    tenure_years = require_positive(tenure_years, "tenure")

    n = int(tenure_years * 12)
    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        future_value = monthly_investment * n
    else:
        future_value = monthly_investment * (((1 + monthly_rate) ** n - 1) / monthly_rate) * (1 + monthly_rate)

    invested_amount = monthly_investment * n
    estimated_returns = future_value - invested_amount

    return {
        "invested_amount": round(invested_amount, 2),
        "estimated_returns": round(estimated_returns, 2),
        "future_value": round(future_value, 2),
    }


def calculate_discount(original_price, discount_percent):
    original_price = require_positive(original_price, "original price")
    discount_percent = require_non_negative(discount_percent, "discount percent")
    if discount_percent > 100:
        raise ValidationError("Discount percent cannot exceed 100.")

    discount_amount = original_price * discount_percent / 100
    final_price = original_price - discount_amount

    return {
        "discount_amount": round(discount_amount, 2),
        "final_price": round(final_price, 2),
    }


def calculate_profit_loss(cost_price, selling_price):
    cost_price = require_positive(cost_price, "cost price")
    selling_price = require_non_negative(selling_price, "selling price")

    diff = selling_price - cost_price
    percent = abs(diff) / cost_price * 100

    return {
        "type": "profit" if diff > 0 else ("loss" if diff < 0 else "no profit no loss"),
        "amount": round(abs(diff), 2),
        "percent": round(percent, 2),
    }


def calculate_percentage(value, percent):
    value = require_non_negative(value, "value")
    percent = require_non_negative(percent, "percent")
    return {"result": round(value * percent / 100, 4)}
