from flask import Blueprint, render_template, url_for, redirect, flash, request
from extensions import db
from models import Expense
from forms import ExpenseForm
import datetime as dt

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@expenses_bp.route("/", methods=["GET"])
def list_expenses():
    page = request.args.get("page", 1, type=int)
    
    pagination = db.paginate(db.select(Expense).order_by(Expense.id.desc()), page=page, per_page=10, error_out=False)
    expenses = pagination.items
    return render_template("expenses.html", pagination=pagination, expenses=expenses, Expense=Expense, active_page="expenses")


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


@expenses_bp.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id: int):
    expense = db.get_or_404(Expense, expense_id)
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
    return render_template("expenses_edit.html", form=form, expense=expense, active_page="expenses_edit")


@expenses_bp.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expense = db.get_or_404(Expense, expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense successfully deleted!")
    return redirect(url_for("expenses.list_expenses"))