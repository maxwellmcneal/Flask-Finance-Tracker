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

from helper import get_todays_date, is_date_in_future
from constants import EXPENSE_CATEGORIES, PAYMENT_METHOD_CHOICES

def future_validator(form, field):
    if is_date_in_future(field.data):
        raise validators.ValidationError('Date cannot be in the future!')

class ExpenseForm(FlaskForm):
    date = DateField('Date', [validators.DataRequired(), future_validator], default=get_todays_date)
    amount = DecimalField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)])
    retailer = StringField('Retailer', [validators.DataRequired()])
    description = StringField('Description')
    category = SelectField('Category', [validators.DataRequired()], choices=EXPENSE_CATEGORIES)
    payment_method = SelectField('Payment Method', [validators.DataRequired()], choices=PAYMENT_METHOD_CHOICES)
    submit = SubmitField('Submit')