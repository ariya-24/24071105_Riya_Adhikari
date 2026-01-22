# Student ID: 24071105
# Student Name: Riya Adhikari

from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, SubmitField, PasswordField, StringField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional, Length, Email

class HotelForm(FlaskForm):
    total_capacity = IntegerField('Total Capacity', validators=[DataRequired(), NumberRange(min=1)])
    peak_rate = DecimalField('Peak Rate (£)', validators=[DataRequired(), NumberRange(min=0)])
    off_peak_rate = DecimalField('Off-Peak Rate (£)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Update Hotel')

class UserEditForm(FlaskForm):
    password = PasswordField('Reset Password', validators=[Optional(), Length(min=6)])
    submit = SubmitField('Update User')

class UserAddForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('customer', 'Customer'), ('admin', 'Admin')], default='customer')
    submit = SubmitField('Create User')

class CurrencyAddForm(FlaskForm):
    currency_code = StringField('Currency Code (e.g. USD)', validators=[DataRequired(), Length(min=3, max=3)])
    currency_name = StringField('Currency Name', validators=[DataRequired(), Length(max=50)])
    symbol = StringField('Symbol', validators=[DataRequired(), Length(max=5)])
    exchange_rate = DecimalField('Exchange Rate (1 GBP = ?)', validators=[DataRequired(), NumberRange(min=0.0001)])
    submit = SubmitField('Add Currency')

class CurrencyForm(FlaskForm):
    exchange_rate = DecimalField('Exchange Rate (1 GBP = ?)', validators=[DataRequired(), NumberRange(min=0.0001)])
    submit = SubmitField('Update Rate')
