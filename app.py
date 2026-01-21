from flask import Flask, render_template
from extensions import db, bootstrap
from views.expenses import expenses_bp
from views.graphs import graphs_bp
from models import Expense
import os
import datetime as dt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'app.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(expenses_bp)
    app.register_blueprint(graphs_bp)

    @app.route("/")
    def index():
        current_date = dt.date.today()
        # Get first and last day of current month
        first_day = current_date.replace(day=1)
        if current_date.month == 12:
            last_day = current_date.replace(day=31)
        else:
            last_day = (current_date.replace(month=current_date.month + 1, day=1) - dt.timedelta(days=1))

        # Query all expenses in current month
        monthly_expenses = db.session.execute(
            db.select(Expense).filter(
                Expense.date >= first_day,
                Expense.date <= last_day
            )
        ).scalars().all()

        # Calculate monthly total
        monthly_total = sum(expense.amount for expense in monthly_expenses)

        return render_template("index.html", active_page="index", monthly_total=monthly_total)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
