# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, MedicalOffice, Person, Patient, Doctor, OfficeManager, StaffMember, Appointment, Schedule
from forms import AppointmentForm, PatientForm, LoginForm, OfficeManagerForm, DoctorForm, OfficeClerkForm
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
@login_required
def appointments():
    all_appointments = Appointment.query.all()
    return render_template('appointmentsByPatient.html', appointments=all_appointments, name=current_user.userName)

@app.route('/appointmentsByPatient')
@login_required
def appointmentsByPatient():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()
    all_appointments = Appointment.query.filter_by(patientID = patient.patientID).all()
    return render_template('appointmentsByPatient.html', appointmentsByPatient=all_appointments, name=current_user.userName)

@app.route('/patients')
@login_required
def patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients, userName=current_user.userName)

@app.route('/clerks')
@login_required
def officeClerks():
    all_clerks = StaffMember.query.all()
    return render_template('officeClerks.html', clerks=all_clerks, userName=current_user.userName)

@app.route('/doctors')
@login_required
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors, userName=current_user.userName)

@app.route('/officeManagers')
@login_required
def officeManagers():
    all_managers = OfficeManager.query.all()
    return render_template('officeManagers.html', managers=all_managers, name=current_user.userName)


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

@app.route('/dashboard_managers')
@login_required
def dashboard_managers():
    person = Person.query.filter_by(userName=current_user.userName).first()
    return render_template('manager_dashboard.html', userName=current_user.userName, idNumber=person.idNumber,
                           lastName=person.lastName, firstName=person.firstName, gender=person.gender, dob=person.dateOfBirth,
                           address=person.address, phone=person.phone, email=person.email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        userName = form.username.data
        password = form.password.data

        user = Person.query.filter_by(userName=userName).first()
        patient = Patient.query.filter_by(personID=user.id).first()
        if patient and user.password == password:
            login_user(user)  # Create session for the user
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html', form=form)

@app.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    form = LoginForm()

    if form.validate_on_submit():
        userName = form.username.data
        password = form.password.data

        user = Person.query.filter_by(userName=userName).first()
        manager = OfficeManager.query.filter_by(personID=user.id).first()
        if manager and user.password == password:
            login_user(user)  # Create session for the user
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard_managers'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login_manager.html', form=form)

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
    form.doctor.choices = [(doctor.doctorID, doctor.person.firstName + " " + doctor.person.lastName) for doctor in Doctor.query.all()]

    if form.validate_on_submit():
        user = Person.query.filter_by(userName=current_user.userName).first()
        patient = Patient.query.filter_by(personID=user.id).first()
        if patient:
            appointment = Appointment(
                appointmentDate=form.appointmentDate.data,
                appointmentTime=form.appointmentTime.data,
                appointmentType=form.appointmentType.data,
                patientID=patient.patientID,
                doctorID=form.doctor.data
            )
            db.session.add(appointment)
            db.session.commit()

        flash("Appointment scheduled successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('new_appointment.html', form=form, name=current_user.userName)


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

@app.route('/new_patient_manager', methods=['GET', 'POST'])
@login_required
def new_patient_manager():
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
        return redirect(url_for('dashboard_managers'))

    return render_template('new_patient_manager.html', form=form, name=current_user.userName)

@app.route('/add_officeManager', methods=['GET', 'POST'])
@login_required
def add_officeManager():
    form = OfficeManagerForm()

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

        officeManager = OfficeManager(
            personID = person.id
        )
        db.session.add(officeManager)
        db.session.commit()

        flash("OfficeManager Added successfully!", "success")
        return redirect(url_for('dashboard_managers'))

    return render_template('add_officeManager.html', form=form, name=current_user.userName)

@app.route('/add_officeClerk', methods=['GET', 'POST'])
@login_required
def add_officeClerk():
    form = OfficeClerkForm()

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

        officeClerk = StaffMember(
            personID = person.id
        )
        db.session.add(officeClerk)
        db.session.commit()

        flash("Office Clerk Added successfully!", "success")
        return redirect(url_for('dashboard_managers'))

    return render_template('add_officeClerk.html', form=form, name=current_user.userName)

@app.route('/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    form = DoctorForm()

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

        doctor = Doctor(
            personID = person.id,
            licenseNumber = form.license.data,
            specialization = form.specialty.data
        )
        db.session.add(doctor)
        db.session.commit()

        flash("Doctor Added successfully!", "success")
        return redirect(url_for('dashboard_managers'))

    return render_template('new_doctor.html', form=form, name=current_user.userName)

if __name__ == '__main__':
    app.run(debug=True)
