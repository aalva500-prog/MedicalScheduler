# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, DateField
from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import DateInput
from wtforms import validators


class AppointmentForm(FlaskForm):
    patient_name = StringField("Patient Name", validators=[DataRequired()])
    patient_email = StringField("Patient Email", validators=[DataRequired(), Email()])
    patient_phone = StringField("Patient Phone", validators=[DataRequired()])
    doctor = SelectField("Doctor", coerce=int, validators=[DataRequired()])
    date = DateTimeField("Date and Time", validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Schedule Appointment")

class PatientForm(FlaskForm):
    id_number = StringField("License Number", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    first_name = StringField("First Name", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    last_name = StringField("Last Name", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    username = StringField("Username", render_kw={"autocapitalize": "off", "placeholder": "Enter your username"} , validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    genders = [("Male", "Male"), ("Female", "Female")]
    gender = SelectField("Gender", validators=[DataRequired()], choices=genders)
    birthday = DateField('Birthday', render_kw={"autocapitalize": "off"}, format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    address = StringField("Address", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    phone_number = StringField("Phone Number", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    email = StringField("Email", render_kw={"autocapitalize": "off"}, validators=[DataRequired(), Email()])
    weight = FloatField("Weight (lb)", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    height = FloatField("Height (cm)", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    bloods = [("A+", "A+"), ("A-", "A-"), ("B+", "B+"),("B-", "B-"),("AB+", "AB+"),("AB-", "AB-"),("O+", "O+"),("O-", "O-")]
    blood = SelectField("Blood Type", validators=[DataRequired()], choices=bloods)
    submit = SubmitField("Add Patient")

class LoginForm(FlaskForm):
    username = StringField("Username", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"autocapitalize": "off"}, validators=[DataRequired()])
    submit = SubmitField("Login")

