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

class ExpenseForm(FlaskForm):
    date = DateField('Date', [validators.DataRequired()])
    amount = FloatField('Amount', [validators.DataRequired(), validators.NumberRange(min=0.01)])
    retailer = StringField('Retailer', [validators.DataRequired()])
    description = StringField('Description')
    category = StringField('Category', [validators.DataRequired()])
    payment_method = StringField('Payment Method', [validators.DataRequired()])
    submit = SubmitField('Submit')