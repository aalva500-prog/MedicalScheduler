# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, DateField
from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import DateInput

class AppointmentForm(FlaskForm):
    patient_name = StringField("Patient Name", validators=[DataRequired()])
    patient_email = StringField("Patient Email", validators=[DataRequired(), Email()])
    patient_phone = StringField("Patient Phone", validators=[DataRequired()])
    doctor = SelectField("Doctor", coerce=int, validators=[DataRequired()])
    date = DateTimeField("Date and Time", validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Schedule Appointment")

class PatientForm(FlaskForm):
    id_number = StringField("License Number", render_kw={"autocomplete": "off", "placeholder": "Enter ID Number"}, validators=[DataRequired()])
    first_name = StringField("First Name", render_kw={"autocomplete": "off", "placeholder": "Enter First Name"}, validators=[DataRequired()])
    last_name = StringField("Last Name", render_kw={"autocomplete": "off", "placeholder": "Enter Last Name"}, validators=[DataRequired()])
    username = StringField("Username", render_kw={"autocomplete": "off", "placeholder": "Enter username"} , validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"autocomplete": "off", "placeholder": "Enter password"}, validators=[DataRequired()])
    genders = [("Male", "Male"), ("Female", "Female")]
    gender = SelectField("Gender", validators=[DataRequired()], choices=genders)
    birthday = DateField('Birthday', render_kw={"autocomplete": "off", "placeholder": "Enter Date of Birth"}, format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    address = StringField("Address", render_kw={"autocomplete": "off", "placeholder": "Enter Address"}, validators=[DataRequired()])
    phone_number = StringField("Phone Number", render_kw={"autocomplete": "off", "placeholder": "Enter Phone Number"}, validators=[DataRequired()])
    email = StringField("Email", render_kw={"autocomplete": "off", "placeholder": "Enter email address"}, validators=[DataRequired(), Email()])
    weight = FloatField("Weight (lb)", render_kw={"autocomplete": "off", "placeholder": "Enter Weight (lb)"}, validators=[DataRequired()])
    height = FloatField("Height (cm)", render_kw={"autocomplete": "off", "placeholder": "Enter Height (cm)"}, validators=[DataRequired()])
    bloods = [("A+", "A+"), ("A-", "A-"), ("B+", "B+"),("B-", "B-"),("AB+", "AB+"),("AB-", "AB-"),("O+", "O+"),("O-", "O-")]
    blood = SelectField("Blood Type", validators=[DataRequired()], choices=bloods)
    submit = SubmitField("Add Patient")

class LoginForm(FlaskForm):
    username = StringField("Username", render_kw={"autocomplete": "off", "placeholder": "Enter your username"}, validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"autocomplete": "off", "placeholder": "Enter your password"}, validators=[DataRequired()])
    submit = SubmitField("Login")

class OfficeManagerForm(FlaskForm):
    id_number = StringField("License Number", render_kw={"autocomplete": "off", "placeholder": "Enter ID Number"}, validators=[DataRequired()])
    first_name = StringField("First Name", render_kw={"autocomplete": "off", "placeholder": "Enter First Name"}, validators=[DataRequired()])
    last_name = StringField("Last Name", render_kw={"autocomplete": "off", "placeholder": "Enter Last Name"}, validators=[DataRequired()])
    username = StringField("Username", render_kw={"autocomplete": "off", "placeholder": "Enter username"}, validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"autocomplete": "off", "placeholder": "Enter password"}, validators=[DataRequired()])
    genders = [("Male", "Male"), ("Female", "Female")]
    gender = SelectField("Gender", validators=[DataRequired()], choices=genders)
    birthday = DateField('Birthday', render_kw={"autocomplete": "off", "placeholder": "Enter Date of Birth"}, format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    address = StringField("Address", render_kw={"autocomplete": "off", "placeholder": "Enter Address"}, validators=[DataRequired()])
    phone_number = StringField("Phone Number", render_kw={"autocomplete": "off", "placeholder": "Enter Phone Number"}, validators=[DataRequired()])
    email = StringField("Email", render_kw={"autocomplete": "off", "placeholder": "Enter email address"}, validators=[DataRequired(), Email()])
    submit = SubmitField("Add Office Manager")

class OfficeClerkForm(FlaskForm):
    id_number = StringField("License Number", render_kw={"autocomplete": "off", "placeholder": "Enter ID Number"}, validators=[DataRequired()])
    first_name = StringField("First Name", render_kw={"autocomplete": "off", "placeholder": "Enter First Name"}, validators=[DataRequired()])
    last_name = StringField("Last Name", render_kw={"autocomplete": "off", "placeholder": "Enter Last Name"}, validators=[DataRequired()])
    username = StringField("Username", render_kw={"autocomplete": "off", "placeholder": "Enter username"}, validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"autocomplete": "off", "placeholder": "Enter password"}, validators=[DataRequired()])
    genders = [("Male", "Male"), ("Female", "Female")]
    gender = SelectField("Gender", validators=[DataRequired()], choices=genders)
    birthday = DateField('Birthday', render_kw={"autocomplete": "off", "placeholder": "Enter Date of Birth"}, format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    address = StringField("Address", render_kw={"autocomplete": "off", "placeholder": "Enter Address"}, validators=[DataRequired()])
    phone_number = StringField("Phone Number", render_kw={"autocomplete": "off", "placeholder": "Enter Phone Number"}, validators=[DataRequired()])
    email = StringField("Email", render_kw={"autocomplete": "off", "placeholder": "Enter email address"}, validators=[DataRequired(), Email()])
    submit = SubmitField("Add Office Clerk")

class DoctorForm(FlaskForm):
    id_number = StringField("License Number", render_kw={"autocomplete": "off", "placeholder": "Enter ID Number"}, validators=[DataRequired()])
    first_name = StringField("First Name", render_kw={"autocomplete": "off", "placeholder": "Enter First Name"}, validators=[DataRequired()])
    last_name = StringField("Last Name", render_kw={"autocomplete": "off", "placeholder": "Enter Last Name"}, validators=[DataRequired()])
    username = StringField("Username", render_kw={"autocomplete": "off", "placeholder": "Enter username"}, validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"autocomplete": "off", "placeholder": "Enter password"}, validators=[DataRequired()])
    genders = [("Male", "Male"), ("Female", "Female")]
    gender = SelectField("Gender", validators=[DataRequired()], choices=genders)
    birthday = DateField('Birthday', render_kw={"autocomplete": "off", "placeholder": "Enter Date of Birth"}, format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    address = StringField("Address", render_kw={"autocomplete": "off", "placeholder": "Enter Address"}, validators=[DataRequired()])
    phone_number = StringField("Phone Number", render_kw={"autocomplete": "off", "placeholder": "Enter Phone Number"}, validators=[DataRequired()])
    email = StringField("Email", render_kw={"autocomplete": "off", "placeholder": "Enter email address"}, validators=[DataRequired(), Email()])
    specialty = StringField("Specialty", render_kw={"autocomplete": "off", "placeholder": "Enter Specialty"}, validators=[DataRequired()])
    license = StringField("Doctor's License", render_kw={"autocomplete": "off", "placeholder": "Enter Doctor's License"}, validators=[DataRequired()])
    submit = SubmitField("Add Doctor ")

