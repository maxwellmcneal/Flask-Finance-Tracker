from flask import Blueprint, render_template, url_for, redirect, flash, request
from extensions import db
from models import Income, IncomeAllocation, Expense, Reimbursement
from forms import IncomeForm, IncomeAllocationForm, ReimbursementForm
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
        if income.category.name == "Reimbursement":
            return redirect(url_for("income.manage_reimbursement", income_id=income.id))
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


@income_bp.route("/<int:income_id>/allocations", methods=["GET", "POST"])
def manage_allocations(income_id):
    income = db.get_or_404(Income, income_id)
    form = IncomeAllocationForm()

    allocated_total = sum(a.amount for a in income.allocations)
    remaining = float(income.amount) - allocated_total

    if form.validate_on_submit():
        alloc_amount = float(form.amount.data)
        if alloc_amount > remaining + 0.01:
            flash("Allocation amount exceeds remaining unallocated amount.")
        else:
            allocation = IncomeAllocation(
                income_id=income.id,
                account=form.account.data,
                amount=alloc_amount,
            )
            db.session.add(allocation)
            db.session.commit()
            flash("Allocation added!")
            return redirect(url_for("income.manage_allocations", income_id=income.id))

    return render_template(
        "income_allocations.html",
        income=income,
        form=form,
        allocated_total=allocated_total,
        remaining=remaining,
        active_page="income",
    )


@income_bp.route("/<int:income_id>/allocations/<int:alloc_id>/delete", methods=["POST"])
def delete_allocation(income_id, alloc_id):
    allocation = db.get_or_404(IncomeAllocation, alloc_id)
    if allocation.income_id != income_id:
        flash("Invalid allocation.")
        return redirect(url_for("income.manage_allocations", income_id=income_id))
    db.session.delete(allocation)
    db.session.commit()
    flash("Allocation deleted!")
    return redirect(url_for("income.manage_allocations", income_id=income_id))


@income_bp.route("/<int:income_id>/reimbursement", methods=["GET", "POST"])
def manage_reimbursement(income_id):
    income = db.get_or_404(Income, income_id)

    # Get expenses with unreimbursed balance
    all_expenses = db.session.execute(
        db.select(Expense).order_by(Expense.date.desc())
    ).scalars().all()
    eligible_expenses = [e for e in all_expenses if e.net_amount > 0.01]

    form = ReimbursementForm()
    form.expense.query_factory = lambda: eligible_expenses

    if form.validate_on_submit():
        reimb_amount = float(form.amount.data)
        expense = form.expense.data
        if reimb_amount > float(income.amount) + 0.01:
            flash("Amount exceeds the income amount.")
        elif reimb_amount > expense.net_amount + 0.01:
            flash("Amount exceeds expense's unreimbursed balance.")
        else:
            reimbursement = Reimbursement(
                income_id=income.id,
                expense=expense,
                amount=reimb_amount,
                date=income.date,
            )
            db.session.add(reimbursement)
            db.session.commit()
            flash("Reimbursement linked!")
            return redirect(url_for("income.manage_reimbursement", income_id=income.id))

    return render_template(
        "income_reimbursement.html",
        income=income,
        form=form,
        active_page="income",
    )


@income_bp.route("/<int:income_id>/reimbursement/<int:reimb_id>/delete", methods=["POST"])
def delete_reimbursement(income_id, reimb_id):
    reimbursement = db.get_or_404(Reimbursement, reimb_id)
    if reimbursement.income_id != income_id:
        flash("Invalid reimbursement.")
        return redirect(url_for("income.manage_reimbursement", income_id=income_id))
    db.session.delete(reimbursement)
    db.session.commit()
    flash("Reimbursement removed!")
    return redirect(url_for("income.manage_reimbursement", income_id=income_id))
