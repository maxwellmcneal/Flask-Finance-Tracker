from wtforms import (Form, 
                     IntegerField, 
                     DecimalField,
                     StringField,
                     DateField,
                     SubmitField,
                     SelectField,
                     validators
)
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from extensions import db
from models import ExpenseCategory, PaymentMethod
from helper import get_todays_date, is_date_in_future

def future_validator(form, field):
    if is_date_in_future(field.data):
        raise validators.ValidationError('Date cannot be in the future!')

class ExpenseForm(FlaskForm):
    date = DateField('Date', [validators.DataRequired(), future_validator], default=get_todays_date)
    amount = DecimalField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)], render_kw={'inputmode':'decimal'})
    retailer = StringField('Retailer', [validators.DataRequired()])
    description = StringField('Description')
    # category = SelectField('Category', [validators.DataRequired()], choices=EXPENSE_CATEGORIES)
    # payment_method = SelectField('Payment Method', [validators.DataRequired()], choices=PAYMENT_METHOD_CHOICES)
    category = QuerySelectField(
        'Category',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(ExpenseCategory).order_by(ExpenseCategory.name)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select category'
    )
    payment_method = QuerySelectField(
        'Payment Method',
        [validators.DataRequired()],
        query_factory=lambda: db.session.execute(db.select(PaymentMethod).order_by(PaymentMethod.id)).scalars(),
        get_label='name',
        allow_blank=True,
        blank_text='Select payment method'
    )
    submit = SubmitField('Submit')