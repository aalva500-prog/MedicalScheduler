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
    id_number = StringField("License Number", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    genders = [("male", "Male"), ("female", "Female")]
    gender = SelectField("Gender", validators=[DataRequired()], choices=genders)
    birthday = DateField('Birthday', format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    weight = FloatField("Weight (lb)", validators=[DataRequired()])
    height = FloatField("Height (cm)", validators=[DataRequired()])
    bloods = [("a", "A"),("b", "B"),("ab", "AB"),("o", "O")]
    blood = SelectField("Blood Type", validators=[DataRequired()], choices=bloods)
    submit = SubmitField("Add Patient")

