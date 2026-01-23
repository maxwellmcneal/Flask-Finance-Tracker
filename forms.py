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
import datetime as dt

def is_not_in_future(form, field):
    if field.data > dt.date.today():
        raise validators.ValidationError('Date cannot be in the future')

class ExpenseForm(FlaskForm):
    date = DateField('Date', [validators.DataRequired(), is_not_in_future], default=dt.date.today())
    amount = FloatField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)])
    retailer = StringField('Retailer', [validators.DataRequired()])
    description = StringField('Description')
    category = StringField('Category', [validators.DataRequired()])
    payment_method = StringField('Payment Method', [validators.DataRequired()])
    submit = SubmitField('Submit')