from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from extensions import db, bootstrap
from views.expenses import expenses_bp
from views.graphs import graphs_bp
from models import Expense
import os
import datetime as dt
from dotenv import load_dotenv
from helper import get_todays_date

# Load environment variables from .env file
load_dotenv()
# CSRF protection
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'app.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)
        
    csrf.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(expenses_bp)
    app.register_blueprint(graphs_bp)

    @app.route("/")
    def index():
        current_date = get_todays_date()
        # Get first and last day of current month
        first_day = current_date.replace(day=1)

        # Query all expenses from start of month to today
        monthly_expenses = db.session.execute(
            db.select(Expense).filter(
                Expense.date >= first_day,
                Expense.date <= current_date
            )
        ).scalars().all()

        # Calculate monthly expense total
        monthly_total = sum(expense.amount for expense in monthly_expenses)
        # Calculate zero spend days
        expense_dates = {expense.date for expense in monthly_expenses}
        days_elapsed = current_date.day
        zero_spend_days = days_elapsed - len(expense_dates)
        
        return render_template("index.html", active_page="index",
                               current_date=current_date,
                               monthly_total=monthly_total, 
                               zero_spend_days=zero_spend_days,
                               days_elapsed=days_elapsed)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
