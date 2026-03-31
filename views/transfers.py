from flask import Blueprint, render_template, url_for, redirect, flash, request
from extensions import db
from models import Transfer
from forms import TransferForm
import datetime as dt

transfers_bp = Blueprint("transfers", __name__, url_prefix="/transfers")


@transfers_bp.route("/", methods=["GET"])
def list_transfers():
    page = request.args.get("page", 1, type=int)

    pagination = db.paginate(db.select(Transfer).order_by(Transfer.id.desc()), page=page, per_page=10, error_out=False)
    transfers = pagination.items
    return render_template("transfers.html", pagination=pagination, transfers=transfers, active_page="transfers")


@transfers_bp.route("/add", methods=["GET", "POST"])
def add_transfer():
    form = TransferForm()
    if form.validate_on_submit():
        transfer = Transfer(
            date=form.date.data,
            amount=form.amount.data,
            from_account=form.from_account.data,
            to_account=form.to_account.data,
            description=form.description.data,
        )
        db.session.add(transfer)
        db.session.commit()
        flash("Transfer successfully added!")
        return redirect(url_for("transfers.list_transfers"))
    return render_template("transfers_add.html", form=form, active_page="transfers_add")


@transfers_bp.route("/edit/<int:transfer_id>", methods=["GET", "POST"])
def edit_transfer(transfer_id: int):
    transfer = db.get_or_404(Transfer, transfer_id)
    form = TransferForm(obj=transfer)
    if form.validate_on_submit():
        transfer.date = form.date.data
        transfer.amount = form.amount.data
        transfer.from_account = form.from_account.data
        transfer.to_account = form.to_account.data
        transfer.description = form.description.data
        db.session.commit()
        flash("Transfer successfully edited!")
        return redirect(url_for("transfers.list_transfers"))
    return render_template("transfers_edit.html", form=form, transfer=transfer, active_page="transfers_edit")


@transfers_bp.route("/delete/<int:transfer_id>", methods=["POST"])
def delete_transfer(transfer_id):
    transfer = db.get_or_404(Transfer, transfer_id)
    db.session.delete(transfer)
    db.session.commit()
    flash("Transfer successfully deleted!")
    return redirect(url_for("transfers.list_transfers"))
