from flask import Blueprint, render_template, url_for, redirect, flash, request
from extensions import db
from models import Expense
from forms import ExpenseForm
import datetime as dt

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@expenses_bp.route("/", methods=["GET"])
def list_expenses():
    # optionally add one test expense if none exist
    # if not Expense.query.first():
    #     test_expense = Expense(
    #         id=123,
    #         date=dt.date(2025, 6, 1),
    #         amount=5.99,
    #         retailer="Spotify",
    #         description="June subscription",
    #         category="Entertainment",
    #         payment_method="Chase Credit Card (8458)"
    #     )
    #     db.session.add(test_expense)
    #     db.session.commit()

    page = request.args.get("page", 1, type=int)
    
    pagination = db.paginate(db.select(Expense).order_by(Expense.id.desc()), page=page, per_page=5, error_out=False)
    expenses = pagination.items
    return render_template("expenses.html", pagination=pagination, expenses=expenses, active_page="expenses")


@expenses_bp.route("/add", methods=["GET", "POST"])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            date=form.date.data,
            amount=form.amount.data,
            retailer=form.retailer.data,
            description=form.description.data,
            category=form.category.data,
            payment_method=form.payment_method.data,
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense successfully added!")
        return redirect(url_for("expenses.list_expenses"))
    return render_template("expenses_add.html", form=form, active_page="expenses_add")


@expenses_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id: int):
    expense = db.get_or_404(Expense, id)
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.date = form.date.data
        expense.amount = form.amount.data
        expense.retailer = form.retailer.data
        expense.description = form.description.data
        expense.category = form.category.data
        expense.payment_method = form.payment_method.data
        db.session.commit()
        flash("Expense successfully edited!")
        return redirect(url_for("expenses.list_expenses"))
    return render_template("expenses_edit.html", form=form, expense=expense, active_page="expenses")


@expenses_bp.route("/delete/<int:id>", methods=["POST"])
def delete_expense(id):
    expense = db.get_or_404(Expense, id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense successfully deleted!")
    return redirect(url_for("expenses.list_expenses"))