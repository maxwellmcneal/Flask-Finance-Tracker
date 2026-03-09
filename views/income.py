from flask import Blueprint, render_template, url_for, redirect, flash, request
from extensions import db
from models import Income
from forms import IncomeForm
import datetime as dt

income_bp = Blueprint("income", __name__, url_prefix="/income")


@income_bp.route("/", methods=["GET"])
def list_income():
    page = request.args.get("page", 1, type=int)

    pagination = db.paginate(db.select(Income).order_by(Income.id.desc()), page=page, per_page=10, error_out=False)
    income = pagination.items
    return render_template("income.html", pagination=pagination, income=income, Income=Income, active_page="income")


@income_bp.route("/add", methods=["GET", "POST"])
def add_income():
    form = IncomeForm()
    if form.validate_on_submit():
        income = Income(
            date=form.date.data,
            amount=form.amount.data,
            source=form.source.data,
            description=form.description.data,
            category=form.category.data,
            account=form.account.data,
        )
        db.session.add(income)
        db.session.commit()
        flash("Income successfully added!")
        return redirect(url_for("income.list_income"))
    return render_template("income_add.html", form=form, active_page="income_add")


@income_bp.route("/edit/<int:income_id>", methods=["GET", "POST"])
def edit_income(income_id: int):
    income = db.get_or_404(Income, income_id)
    form = IncomeForm(obj=income)
    if form.validate_on_submit():
        income.date = form.date.data
        income.amount = form.amount.data
        income.source = form.source.data
        income.description = form.description.data
        income.category = form.category.data
        income.account = form.account.data
        db.session.commit()
        flash("Income successfully edited!")
        return redirect(url_for("income.list_income"))
    return render_template("income_edit.html", form=form, income=income, active_page="income_edit")


@income_bp.route("/delete/<int:income_id>", methods=["POST"])
def delete_income(income_id):
    income = db.get_or_404(Income, income_id)
    db.session.delete(income)
    db.session.commit()
    flash("Income successfully deleted!")
    return redirect(url_for("income.list_income"))
