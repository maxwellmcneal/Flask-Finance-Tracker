from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from extensions import db, bootstrap
from views.expenses import expenses_bp
from views.income import income_bp
from views.transfers import transfers_bp
from views.graphs import graphs_bp
from models import Account, Expense, Income, IncomeAllocation, IncomeCategory, Transfer
import os
import datetime as dt

from helper import get_todays_date

# CSRF protection
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'DATABASE_URL',
            f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'app.db')}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)
        
    csrf.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(expenses_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(transfers_bp)
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
        
        # Query all expenses from start of month to today
        monthly_income = db.session.execute(
            db.select(Income)
            .join(Income.category)
            .filter(
                Income.date >= first_day,
                Income.date <= current_date,
                IncomeCategory.name != 'Reimbursement'
            )
        ).scalars().all()

        # Calculate monthly expense total
        monthly_expenses_total = sum(expense.net_amount for expense in monthly_expenses)
        monthly_income_total = sum(income.amount for income in monthly_income)
        
        # Calculate zero spend days
        expense_dates = {expense.date for expense in monthly_expenses}
        days_elapsed = current_date.day
        zero_spend_days = days_elapsed - len(expense_dates)
        
        # Calculate account balances
        expense_subq = (
            db.select(
                Expense.account_id,
                db.func.sum(Expense.amount).label("total_expense")
            )
            .group_by(Expense.account_id)
            .subquery()
        )
        income_subq = (
            db.select(
                IncomeAllocation.account_id,
                db.func.sum(IncomeAllocation.amount).label("total_income")
            )
            .group_by(IncomeAllocation.account_id)
            .subquery()
        )
        transfer_out_subq = (
            db.select(
                Transfer.from_account_id.label("account_id"),
                db.func.sum(Transfer.amount).label("total_out")
            )
            .group_by(Transfer.from_account_id)
            .subquery()
        )
        transfer_in_subq = (
            db.select(
                Transfer.to_account_id.label("account_id"),
                db.func.sum(Transfer.amount).label("total_in")
            )
            .group_by(Transfer.to_account_id)
            .subquery()
        )
        stmt = (
            db.select(
                Account.id.label("account_id"),
                Account.name.label("name"),
                (
                    db.func.coalesce(Account.starting_balance, 0)
                    + db.func.coalesce(income_subq.c.total_income, 0)
                    - db.func.coalesce(expense_subq.c.total_expense, 0)
                    + db.func.coalesce(transfer_in_subq.c.total_in, 0)
                    - db.func.coalesce(transfer_out_subq.c.total_out, 0)
                ).label("balance")
            )
            .outerjoin(income_subq, income_subq.c.account_id == Account.id)
            .outerjoin(expense_subq, expense_subq.c.account_id == Account.id)
            .outerjoin(transfer_in_subq, transfer_in_subq.c.account_id == Account.id)
            .outerjoin(transfer_out_subq, transfer_out_subq.c.account_id == Account.id)
            .filter(
                (Account.type == "Credit Card") |
                (Account.type == "Checking") |
                (Account.type == "Savings") |
                (Account.type == "Cash") |
                (Account.type == "Other"))
        )
        
        account_balances = db.session.execute(stmt).all()
        
        return render_template("index.html", active_page="index",
                               current_date=current_date,
                               monthly_expenses_total=monthly_expenses_total,
                               monthly_income_total=monthly_income_total, 
                               zero_spend_days=zero_spend_days,
                               days_elapsed=days_elapsed,
                               account_balances=account_balances)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
