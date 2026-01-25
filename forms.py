from wtforms import (Form, 
                     IntegerField, 
                     FloatField,
                     StringField,
                     DateField,
                     SubmitField,
                     validators
)
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField

from helper import get_todays_date, is_date_in_future

def future_validator(form, field):
    if is_date_in_future(field.data):
        raise validators.ValidationError('Date cannot be in the future!')

class ExpenseForm(FlaskForm):
    date = DateField('Date', [validators.DataRequired(), future_validator], default=get_todays_date)
    amount = FloatField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)])
    retailer = StringField('Retailer', [validators.DataRequired()])
    description = StringField('Description')
    category = StringField('Category', [validators.DataRequired()])
    payment_method = StringField('Payment Method', [validators.DataRequired()])
    submit = SubmitField('Submit')