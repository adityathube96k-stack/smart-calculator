from datetime import date, datetime, time

ZODIAC_RANGES = [
    ((1, 20), (2, 18), "Aquarius"),
    ((2, 19), (3, 20), "Pisces"),
    ((3, 21), (4, 19), "Aries"),
    ((4, 20), (5, 20), "Taurus"),
    ((5, 21), (6, 20), "Gemini"),
    ((6, 21), (7, 22), "Cancer"),
    ((7, 23), (8, 22), "Leo"),
    ((8, 23), (9, 22), "Virgo"),
    ((9, 23), (10, 22), "Libra"),
    ((10, 23), (11, 21), "Scorpio"),
    ((11, 22), (12, 21), "Sagittarius"),
]


def get_zodiac_sign(birth_date: date) -> str:
    month_day = (birth_date.month, birth_date.day)
    for start, end, sign in ZODIAC_RANGES:
        if start <= month_day <= end:
            return sign
    return "Capricorn"  # Dec 22 - Jan 19 wraps around the year boundary


def calculate_age(birth_date: date, birth_time: time = None, reference: datetime = None) -> dict:
    if reference is None:
        reference = datetime.now()

    birth_dt = datetime.combine(birth_date, birth_time or time(0, 0))
    if birth_dt > reference:
        raise ValueError("Date of birth cannot be in the future.")

    delta = reference - birth_dt

    years = reference.year - birth_date.year
    months = reference.month - birth_date.month
    days = reference.day - birth_date.day
    if days < 0:
        months -= 1
        prev_month = reference.month - 1 or 12
        prev_year = reference.year if reference.month > 1 else reference.year - 1
        days_in_prev_month = (date(prev_year, prev_month % 12 + 1, 1) - date(prev_year, prev_month, 1)).days
        days += days_in_prev_month
    if months < 0:
        years -= 1
        months += 12

    next_birthday = date(reference.year, birth_date.month, birth_date.day)
    if next_birthday <= reference.date():
        next_birthday = date(reference.year + 1, birth_date.month, birth_date.day)
    countdown_days = (next_birthday - reference.date()).days

    return {
        "years": years,
        "months": months,
        "days": days,
        "total_days": delta.days,
        "total_weeks": delta.days // 7,
        "total_hours": int(delta.total_seconds() // 3600),
        "total_minutes": int(delta.total_seconds() // 60),
        "total_seconds": int(delta.total_seconds()),
        "day_of_birth": birth_date.strftime("%A"),
        "zodiac_sign": get_zodiac_sign(birth_date),
        "next_birthday": next_birthday.isoformat(),
        "birthday_countdown_days": countdown_days,
    }


def date_difference(start: date, end: date) -> dict:
    if end < start:
        start, end = end, start
    delta = end - start
    return {
        "total_days": delta.days,
        "total_weeks": delta.days // 7,
        "years": end.year - start.year - ((end.month, end.day) < (start.month, start.day)),
    }
