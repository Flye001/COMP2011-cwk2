from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, Email, NumberRange
from .models import UserType


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class SignupForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    fname = StringField("First Name", validators=[DataRequired(), Length(max=100)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=100)])
    password = PasswordField("Password", validators=[DataRequired()])
    account_type = SelectField("Account Type", choices=[(a.value, a.name) for a in UserType], validators=[DataRequired()])

class AccountSettingsForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    fname = StringField("First Name", validators=[DataRequired(), Length(max=100)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=100)])
    password = PasswordField("Password (leave blank to not change)")

class UnavailabilityForm(FlaskForm):
    title = StringField("Name", validators=[DataRequired(), Length(max=200)])
    start_date_time = DateTimeLocalField("Start Date")
    end_date_time = DateTimeLocalField("End Date")

class ShiftForm(FlaskForm):
    title = StringField("Shift Title", validators=[DataRequired(), Length(max=200)])
    start_date_time = DateTimeLocalField("Start Date & Time", validators=[DataRequired()])
    end_date_time = DateTimeLocalField("End Date & Time", validators=[DataRequired()])
    workers_required = IntegerField("Workers Required", validators=[DataRequired(), NumberRange(min=1)])