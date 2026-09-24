# Smart Calculator

A multi-tool calculator web app built with Flask — basic and scientific math, age/date/time tools, unit and currency conversion, and financial calculators (GST, EMI, Loan, SIP, Discount, Profit & Loss, Percentage). Includes user accounts with saved calculation history.

## Features

- **Basic Calculator** — safe expression evaluation (no `eval()`), keyboard support
- **Scientific Calculator** — sqrt, power, log, ln, trig, factorial, constants
- **Age Calculator** — full breakdown, birthday countdown, zodiac sign
- **Date Difference / Time Calculator**
- **BMI Calculator**
- **Unit Converter** — length, weight, temperature
- **Currency Converter** — live exchange rates
- **Financial suite** — GST, EMI, Loan, SIP, Discount, Profit & Loss, Percentage
- **Accounts** — register/login, per-user calculation history, favorites
- **Dark mode**, responsive layout

## Tech Stack

- **Backend:** Flask 3, Flask-SQLAlchemy, Flask-Login
- **Database:** SQLite (dev) — swap `DATABASE_URL` for Postgres in production
- **Frontend:** Vanilla HTML/CSS/JS (no build step)

## Project Structure

```
smart-calculator/
├── app.py                 # Application factory & entry point
├── config.py               # Environment-based configuration
├── requirements.txt
├── database/               # SQLAlchemy models + db init
├── routes/                 # Flask blueprints (one per feature area)
├── utils/                  # Pure calculation logic, validators
├── templates/               # Jinja2 templates
├── static/{css,js}/         # Design system + per-page scripts
└── logs/                    # Rotating app log (production only)
```

## Setup

1. **Clone and enter the project**
   ```bash
   cd smart-calculator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # then edit .env and set a real SECRET_KEY
   ```

5. **Run the app**
   ```bash
   python app.py
   ```
   The app starts at `http://127.0.0.1:5000`. The SQLite database and tables are created automatically on first run.

## Running in Production

Don't use Flask's built-in dev server in production. Use Gunicorn behind Nginx:

```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

Set `SECRET_KEY` to a real random value — the app refuses to start in production with the default dev key. Consider switching `DATABASE_URL` to Postgres for anything beyond a single small deployment.

## Security Notes

- Passwords are hashed with Werkzeug's `generate_password_hash` (never stored in plaintext).
- The basic calculator uses a whitelist AST evaluator instead of `eval()` to prevent code injection.
- All numeric/date inputs are validated server-side, not just client-side.
- CSRF protection is enabled via Flask-WTF.

## Running Tests

Test files aren't included yet — recommended next step is `pytest` with the `TestingConfig` in `config.py`, which uses an in-memory SQLite database.
