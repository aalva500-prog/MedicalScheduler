# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, MedicalOffice, Person, Patient, Doctor, OfficeManager, StaffMember, Appointment, Schedule
from forms import AppointmentForm, PatientForm, LoginForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(personID):
    return Person.query.get(int(personID))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments')
def appointments():
    all_appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=all_appointments)

@app.route('/patients')
def patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dashboard')
@login_required
def dashboard():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()
    return render_template('patient_dashboard.html', userName=current_user.userName, idNumber=person.idNumber,
                           lastName=person.lastName, firstName=person.firstName, gender=person.gender, dob=person.dateOfBirth,
                           address=person.address, phone=person.phone, email=person.email, weight=patient.weight, height=patient.height,
                           bloodType = patient.bloodType)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        userName = form.username.data
        password = form.password.data

        user = Person.query.filter_by(userName=userName).first()
        if user and user.password == password:
            login_user(user)  # Create session for the user
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@login_required
@app.route('/new_appointment', methods=['GET', 'POST'])
def new_appointment():
    form = AppointmentForm()
    form.doctor.choices = [(doctor.id, doctor.name) for doctor in Doctor.query.all()]

    if form.validate_on_submit():
        patient = Patient.query.filter_by(email=form.patient_email.data).first()
        if not patient:
            patient = Patient(
                name=form.patient_name.data,
                email=form.patient_email.data,
                phone=form.patient_phone.data
            )
            db.session.add(patient)
            db.session.commit()

        appointment = Appointment(
            date=form.date.data,
            patient_id=patient.id,
            doctor_id=form.doctor.data
        )
        db.session.add(appointment)
        db.session.commit()

        flash("Appointment scheduled successfully!", "success")
        return redirect(url_for('appointments'))

    return render_template('new_appointment.html', form=form)


@app.route('/new_patient', methods=['GET', 'POST'])
def new_patient():
    form = PatientForm()

    if form.validate_on_submit():

        person = Person(
            idNumber = form.id_number.data.upper(),
            firstName = form.first_name.data,
            lastName = form.last_name.data,
            userName = form.username.data.lower(),
            password = form.password.data,
            gender = form.gender.data,
            dateOfBirth = form.birthday.data,
            address = form.address.data.lower(),
            phone = form.phone_number.data,
            email = form.email.data.lower()
        )
        db.session.add(person)
        db.session.commit()

        patient = Patient(
            weight = form.weight.data,
            height = form.height.data,
            bloodType = form.blood.data,
            isActive = True,
            personID = person.id
        )
        db.session.add(patient)
        db.session.commit()

        flash("Patient Added successfully!", "success")
        return redirect(url_for('login'))

    return render_template('new_patient.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
