from wtforms import (Form,
                     IntegerField,
                     DecimalField,
                     StringField,
                     DateField,
                     SubmitField,
                     SelectField,
                     ValidationError,
                     validators
)
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from extensions import db
from models import ExpenseCategory, Account, IncomeCategory
from helper import get_todays_date, is_date_in_future

def future_validator(form, field):
    if is_date_in_future(field.data):
        raise validators.ValidationError('Date cannot be in the future!')

class ExpenseForm(FlaskForm):
    date = DateField('Date', [validators.DataRequired(), future_validator], default=get_todays_date)
    amount = DecimalField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)], render_kw={'inputmode':'decimal'})
    retailer = StringField('Retailer', [validators.DataRequired()])
    description = StringField('Description')
    category = QuerySelectField(
        'Category',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(ExpenseCategory).order_by(ExpenseCategory.name)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select category'
    )
    account = QuerySelectField(
        'Account',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(Account).filter(Account.is_active == True).order_by(Account.name)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select account'
    )
    submit = SubmitField('Submit')
    
class IncomeForm(FlaskForm):
    date = DateField('Date', [validators.DataRequired(), future_validator], default=get_todays_date)
    amount = DecimalField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)], render_kw={'inputmode':'decimal'})
    source = StringField('Source', [validators.DataRequired()])
    description = StringField('Description')
    category = QuerySelectField(
        'Category',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(IncomeCategory).order_by(IncomeCategory.name)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select category'
    )
    account = QuerySelectField(
        'Account',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(Account).filter(Account.is_active == True).order_by(Account.name)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select account'
    )
    submit = SubmitField('Submit')


class IncomeAllocationForm(FlaskForm):
    account = QuerySelectField(
        'Account',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(Account).filter(Account.is_active == True).order_by(Account.name)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select account'
    )
    amount = DecimalField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)], render_kw={'inputmode': 'decimal'})
    submit = SubmitField('Add Allocation')


class TransferForm(FlaskForm):
    date = DateField('Date', [validators.DataRequired(), future_validator], default=get_todays_date)
    amount = DecimalField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)], render_kw={'inputmode': 'decimal'})
    from_account = QuerySelectField(
        'From Account',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(Account).filter(Account.is_active == True).order_by(Account.name)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select account'
    )
    to_account = QuerySelectField(
        'To Account',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(Account).filter(Account.is_active == True).order_by(Account.name)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select account'
    )
    description = StringField('Description')
    submit = SubmitField('Submit')

    def validate_to_account(self, field):
        if field.data and self.from_account.data and field.data.id == self.from_account.data.id:
            raise ValidationError('To Account must be different from From Account.')


class ReimbursementForm(FlaskForm):
    expense = QuerySelectField(
        'Expense',
        [validators.DataRequired()],
        query_factory=lambda: [],
        get_label=lambda e: f"{e.date.strftime('%m/%d/%Y')} - {e.retailer} (${e.net_amount:.2f} remaining)",
        allow_blank=True,
        blank_text='Select expense'
    )
    amount = DecimalField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)], render_kw={'inputmode': 'decimal'})
    submit = SubmitField('Link Reimbursement')