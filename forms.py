# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, DateField
from wtforms.fields.datetime import TimeField
from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import DateInput

class AppointmentForm(FlaskForm):
    appointmentDate = DateField('Appointment Date', render_kw={"autocomplete": "off"}, format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    appointmentTime = TimeField("Appointment Time",  render_kw={"autocomplete": "off"}, format='%H:%M', validators=[DataRequired()])
    types = [("New Patient Visit", "New Patient Visit"), ("Follow Up Visit", "Follow Up Visit")]
    appointmentType = SelectField("Appointment Type", validators=[DataRequired()], choices=types)
    doctor = SelectField("Doctor", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Schedule Appointment")

class RescheduleAppointmentForm(FlaskForm):
    appointmentDate = StringField('Appointment Date', render_kw={"autocomplete": "off"}, widget=DateInput(), validators=[DataRequired()])
    appointmentTime = TimeField("Appointment Time",  render_kw={"autocomplete": "off"}, format='%H:%M', validators=[DataRequired()])
    types = [("New Patient Visit", "New Patient Visit"), ("Follow Up Visit", "Follow Up Visit")]
    appointmentType = SelectField("Appointment Type", validators=[DataRequired()], choices=types)
    submit = SubmitField("Reschedule Appointment")

class AppointmentManagerForm(FlaskForm):
    appointmentDate = DateField('Appointment Date', render_kw={"autocomplete": "off"}, format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    appointmentTime = TimeField("Appointment Time",  render_kw={"autocomplete": "off"}, format='%H:%M', validators=[DataRequired()])
    types = [("New Patient Visit", "New Patient Visit"), ("Follow Up Visit", "Follow Up Visit")]
    appointmentType = SelectField("Appointment Type", validators=[DataRequired()], choices=types)
    patient = SelectField("Patient", coerce=int, validators=[DataRequired()])
    doctor = SelectField("Doctor", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Schedule Appointment")

class PatientForm(FlaskForm):
    id_number = StringField("License Number", render_kw={"autocomplete": "off", "placeholder": "Enter ID Number"}, validators=[DataRequired()])
    first_name = StringField("First Name", render_kw={"autocomplete": "off", "placeholder": "Enter First Name"}, validators=[DataRequired()])
    last_name = StringField("Last Name", render_kw={"autocomplete": "off", "placeholder": "Enter Last Name"}, validators=[DataRequired()])
    username = StringField("Username", render_kw={"autocomplete": "off", "placeholder": "Enter username"} , validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"autocomplete": "off", "placeholder": "Enter password"}, validators=[DataRequired()])
    genders = [("Male", "Male"), ("Female", "Female")]
    gender = SelectField("Gender", validators=[DataRequired()], choices=genders)
    birthday = DateField('Birthday', render_kw={"autocomplete": "off"}, format='%Y-%m-%d', widget=DateInput(), validators=[DataRequired()])
    address = StringField("Address", render_kw={"autocomplete": "off", "placeholder": "Enter Address"}, validators=[DataRequired()])
    phone_number = StringField("Phone Number", render_kw={"autocomplete": "off", "placeholder": "Enter Phone Number"}, validators=[DataRequired()])
    email = StringField("Email", render_kw={"autocomplete": "off", "placeholder": "Enter email address"}, validators=[DataRequired(), Email()])
    weight = FloatField("Weight (lb)", render_kw={"autocomplete": "off", "placeholder": "Enter Weight (lb)"}, validators=[DataRequired()])
    height = FloatField("Height (cm)", render_kw={"autocomplete": "off", "placeholder": "Enter Height (cm)"}, validators=[DataRequired()])
    bloods = [("A+", "A+"), ("A-", "A-"), ("B+", "B+"),("B-", "B-"),("AB+", "AB+"),("AB-", "AB-"),("O+", "O+"),("O-", "O-")]
    blood = SelectField("Blood Type", validators=[DataRequired()], choices=bloods)
    submit = SubmitField("Add Patient")

class UpdatePatientForm(FlaskForm):
    idNumber = StringField("License Number", render_kw={"autocomplete": "off"}, validators=[DataRequired()])
    firstName = StringField("First Name", render_kw={"autocomplete": "off"}, validators=[DataRequired()])
    lastName = StringField("Last Name", render_kw={"autocomplete": "off"}, validators=[DataRequired()])
    genders = [("Male", "Male"), ("Female", "Female")]
    gender = SelectField("Gender", validators=[DataRequired()], choices=genders)
    dateOfBirth = StringField('Birthday', render_kw={"autocomplete": "off"}, widget=DateInput(), validators=[DataRequired()])
    address = StringField("Address", render_kw={"autocomplete": "off"}, validators=[DataRequired()])
    phone = StringField("Phone Number", render_kw={"autocomplete": "off"}, validators=[DataRequired()])
    email = StringField("Email", render_kw={"autocomplete": "off"}, validators=[DataRequired(), Email()])
    weight = FloatField("Weight (lb)", render_kw={"autocomplete": "off"}, validators=[DataRequired()])
    height = FloatField("Height (cm)", render_kw={"autocomplete": "off"}, validators=[DataRequired()])
    bloods = [("A+", "A+"), ("A-", "A-"), ("B+", "B+"),("B-", "B-"),("AB+", "AB+"),("AB-", "AB-"),("O+", "O+"),("O-", "O-")]
    bloodType = SelectField("Blood Type", validators=[DataRequired()], choices=bloods)
    submit = SubmitField("Modify Patient")

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

class SearchAppointmentForm(FlaskForm):
    appointmentDate = StringField('Appointment Date', render_kw={"autocomplete": "off"}, widget=DateInput(), validators=[DataRequired()])
    appointmentTime = TimeField("Appointment Time", render_kw={"autocomplete": "off"}, format='%H:%M', validators=[DataRequired()])
    submit = SubmitField("Search Appointment")

class DateRangeForm(FlaskForm):
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    submit = SubmitField("View Appointments")
