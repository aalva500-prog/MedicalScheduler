# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Person, Patient, Doctor, OfficeManager, StaffMember, Appointment
from forms import AppointmentForm, PatientForm, LoginForm, OfficeManagerForm, DoctorForm, OfficeClerkForm, \
    UpdatePatientForm, SearchAppointmentForm, RescheduleAppointmentForm, DateRangeForm, \
    SearchAppointmentByManagerForm, UpdatePatientManagerForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
import logging
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # For example, Gmail SMTP
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "aaapcsolutions@gmail.com"
app.config["MAIL_PASSWORD"] = "sglk hfnr bkkp bkey"

# Session Security
app.config['SESSION_COOKIE_SECURE'] = True  # Use only over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent access via JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent CSRF

mail = Mail(app)
csrf = CSRFProtect(app) # Cross-Site Request Forgery (CSRF) Protection


@login_manager.user_loader
def load_user(id):
    return Person.query.get(int(id))

# Load tables when App is run
@app.before_request
def create_tables():
    db.create_all()

# Logging and Monitoring. Log all access and error events to detect and respond to unauthorized activities.
logging.basicConfig(filename='app.log', level=logging.INFO)
@app.before_request
def log_request():
    logging.info(f"Accessed by: {request.remote_addr}, Endpoint: {request.endpoint}")

# Index Page route
@app.route('/')
def index():
    return render_template('index.html')

# Managers can see the list of all appointments
@app.route('/appointments')
@login_required
def appointments():
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page", "danger")
        return redirect(url_for('logout'))
    all_appointments = Appointment.query.order_by(Appointment.appointmentDate.desc()).all()
    return render_template('appointments.html', appointments=all_appointments, name=current_user.userName)

# Patients can see their appointments in their Dashboard
@app.route('/appointmentsByPatient')
@login_required
def appointmentsByPatient():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()
    if patient is None:
        flash(f"Error: You don't have access to see this page!", "danger")
        return redirect(url_for('logout'))
    all_appointments = Appointment.query.filter_by(patientID = patient.patientID).order_by(Appointment.appointmentDate.desc()).all()
    return render_template('appointmentsByPatient.html', appointmentsByPatient=all_appointments, name=current_user.userName)

# Managers can see the list of patients
@app.route('/patients')
@login_required
def patients():
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))
    all_patients = Patient.query.order_by().all()
    return render_template('patients.html', patients=all_patients, userName=current_user.userName)

# Managers can see the list of Office Clerks
@app.route('/clerks')
@login_required
def officeClerks():
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))
    all_clerks = StaffMember.query.all()
    return render_template('officeClerks.html', clerks=all_clerks, userName=current_user.userName)

# Managers can see the list of Doctors
@app.route('/doctors')
@login_required
def doctors():
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors, userName=current_user.userName)

# Managers can see the list of Managers
@app.route('/officeManagers')
@login_required
def officeManagers():
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))
    all_managers = OfficeManager.query.all()
    return render_template('officeManagers.html', managers=all_managers, name=current_user.userName)

# Route to the Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to the Patient's Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()
    if patient is None:
        flash(f"Error: You don't have access to see this page!", "danger")
        return redirect(url_for('logout'))
    return render_template('patient_dashboard.html', userName=current_user.userName, idNumber=person.idNumber,
                           lastName=person.lastName, firstName=person.firstName, gender=person.gender, dob=person.dateOfBirth,
                           address=person.address, phone=person.phone, email=person.email, weight=patient.weight, height=patient.height,
                           bloodType = patient.bloodType)

# Update Patient information in the Patient's Dashboard
@app.route('/update_patient', methods=['GET', 'POST'])
@login_required
def update_patient():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()

    if patient is None:
        flash(f"Error: You don't have access to see this page!", "danger")
        return redirect(url_for('logout'))

    # Create the form
    form = UpdatePatientForm()

    # Prepopulate the form with patient data
    if request.method == "GET":
        form.idNumber.data= person.idNumber
        form.firstName.data = person.firstName
        form.lastName.data = person.lastName
        form.gender.data = person.gender
        form.dateOfBirth.data = person.dateOfBirth
        form.address.data = person.address
        form.phone.data = person.phone
        form.email.data = person.email
        form.weight.data = patient.weight
        form.height.data = patient.height
        form.bloodType.data = patient.bloodType

    # Process form submission
    if form.validate_on_submit():
        person.idNumber=form.idNumber.data.upper()
        person.firstName=form.firstName.data
        person.lastName=form.lastName.data
        person.gender=form.gender.data
        person.dateOfBirth=form.dateOfBirth.data
        person.address=form.address.data.lower()
        person.phone=form.phone.data
        person.email=form.email.data.lower()
        patient.weight=form.weight.data
        patient.height=form.height.data
        patient.bloodType=form.bloodType.data

        # Commit changes to the database
        try:
            db.session.commit()
            flash("Patient information updated successfully!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating patient information: {str(e)}", "danger")
    return render_template('update_patient.html', name=current_user.userName, form=form)

# Route to the Manager Dashboard
@app.route('/dashboard_managers')
@login_required
def dashboard_managers():
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))
    return render_template('manager_dashboard.html', userName=current_user.userName, idNumber=person.idNumber,
                           lastName=person.lastName, firstName=person.firstName, gender=person.gender, dob=person.dateOfBirth,
                           address=person.address, phone=person.phone, email=person.email)

# Route to the Patient Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        userName = form.username.data
        password = form.password.data

        user = Person.query.filter_by(userName=userName).first()
        if user:
            patient = Patient.query.filter_by(personID=user.id).first()
            if patient:
                if patient.isActive == True:
                    if user.password == password:
                        login_user(user)  # Create session for the user
                        flash('Login successful!', 'success')
                        return redirect(url_for('dashboard'))
                    else:
                        flash('Invalid username or password!', 'danger')
                else:
                    flash('Your account is Inactive. Please contact the Administrator to activate your Account!', 'danger')
            else:
                flash('Invalid username or password!', 'danger')
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html', form=form)

# Route to the Manager Login Page
@app.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    form = LoginForm()

    if form.validate_on_submit():
        userName = form.username.data
        password = form.password.data

        user = Person.query.filter_by(userName=userName).first()
        if user:
            manager = OfficeManager.query.filter_by(personID=user.id).first()
            if manager and user.password == password:
                login_user(user)  # Create session for the user
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard_managers'))
            else:
                flash('Invalid username or password!', 'danger')
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login_manager.html', form=form)

# Logout route. When an user logs out, the system will take the user to the index page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Patient self-schedules a new appointment
@app.route('/new_appointment', methods=['GET', 'POST'])
@login_required
def new_appointment():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()

    if patient is None:
        flash(f"Error: You don't have access to see this page!", "danger")
        return redirect(url_for('logout'))

    form = AppointmentForm()
    form.doctor.choices = [(doctor.doctorID, doctor.person.firstName + " " + doctor.person.lastName) for doctor in Doctor.query.all()]

    if form.validate_on_submit():
        user = Person.query.filter_by(userName=current_user.userName).first()
        patient = Patient.query.filter_by(personID=user.id).first()

        # Check if an appointment exists for the same patient and date
        existing_appointment = Appointment.query.filter_by(
            patientID=patient.patientID,
            appointmentDate=form.appointmentDate.data
        ).first()

        if existing_appointment:
            flash('ERROR: An appointment for this patient already exists on the selected date!', 'danger')
            return redirect(url_for('new_appointment'))

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

            # Create the email
            msg = Message(
                subject="Appointment Confirmation",
                sender="aaapcsolutions@gmail.com",
                recipients=[user.email]
            )
            msg.body = f"Patient Name: {user.firstName} {user.lastName}\nAppointment Type: {appointment.appointmentType}\nAppointment Date: {appointment.appointmentDate}\nAppointment Time: {appointment.appointmentTime}\n\nThanks & Regards,\nMedical Scheduler Application"

            # Send the email
            try:
                mail.send(msg)
                flash("Please check your email for a confirmation message!\n", "success")
            except Exception as e:
                flash(f"Failed to send message: {e}", "danger")

            flash(
                f"{appointment.appointmentType} appointment has been scheduled successfully for {appointment.appointmentDate} at {appointment.appointmentTime}!",
                "success")
            return redirect(url_for('new_appointment'))

    return render_template('new_appointment.html', form=form, name=current_user.userName)

# Managers view and schedule appointments for a specific patient
@app.route('/patientDetails/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def patientDetails(patient_id):
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    patient = Patient.query.get_or_404(patient_id)

    form = AppointmentForm()
    form.doctor.choices = [(doctor.doctorID, doctor.person.firstName + " " + doctor.person.lastName) for doctor in
                           Doctor.query.all()]
    all_appointments = Appointment.query.filter_by(patientID=patient_id).order_by(Appointment.appointmentDate.desc()).all()

    if form.validate_on_submit():

        # Check if an appointment exists for the same patient and date
        existing_appointment = Appointment.query.filter_by(
            patientID=patient.patientID,
            appointmentDate=form.appointmentDate.data
        ).first()

        if existing_appointment:
            flash('ERROR: An appointment for this patient already exists on the selected date!', 'danger')
            return redirect(url_for('patientDetails', patient_id=patient.patientID))

        appointment = Appointment(
            appointmentDate=form.appointmentDate.data,
            appointmentTime=form.appointmentTime.data,
            appointmentType=form.appointmentType.data,
            patientID=patient_id,
            doctorID=form.doctor.data
        )
        db.session.add(appointment)
        db.session.commit()

        # Create the email
        msg = Message(
            subject="Appointment Confirmation",
            sender="aaapcsolutions@gmail.com",
            recipients=[patient.person.email]
        )
        msg.body = f"Patient Name: {patient.person.firstName} {patient.person.lastName}\nAppointment Type: {appointment.appointmentType}\n Appointment Date: {appointment.appointmentDate}\nAppointment Time: {appointment.appointmentTime}\n\nThanks & Regards,\nMedical Scheduler Application"

        # Send the email
        try:
            mail.send(msg)
            flash("Confirmation message sent to patient's email!\n", "success")
        except Exception as e:
            flash(f"Failed to send message: {e}", "danger")

        flash(
            f"{appointment.appointmentType} appointment has been scheduled successfully for {appointment.appointmentDate} at {appointment.appointmentTime}!",
            "success")
        return redirect(url_for('patientDetails', patient_id=patient.patientID))
    return render_template('patientDetails.html', patient=patient, form=form, name=current_user.userName, appointments=all_appointments)

# Managers modify a given patient information, including mark the Patient as Inactive
@app.route('/modifyPatientDetails/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def modifyPatientDetails(patient_id):
    # Verify if the current user is an Office Manager
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    patient = Patient.query.get_or_404(patient_id)

    # Create the form
    form = UpdatePatientManagerForm()

    # Prepopulate the form with patient data
    if request.method == "GET":
        form.idNumber.data = patient.person.idNumber
        form.firstName.data = patient.person.firstName
        form.lastName.data = patient.person.lastName
        form.gender.data = patient.person.gender
        form.dateOfBirth.data = patient.person.dateOfBirth
        form.address.data = patient.person.address
        form.phone.data = patient.person.phone
        form.email.data = patient.person.email
        form.weight.data = patient.weight
        form.height.data = patient.height
        form.bloodType.data = patient.bloodType
        form.isActive.data = patient.isActive

    # Process form submission
    if form.validate_on_submit():
        patient.person.idNumber = form.idNumber.data.upper()
        patient.person.firstName = form.firstName.data
        patient.person.lastName = form.lastName.data
        patient.person.gender = form.gender.data
        patient.person.dateOfBirth = form.dateOfBirth.data
        patient.person.address = form.address.data.lower()
        patient.person.phone = form.phone.data
        patient.person.email = form.email.data.lower()
        patient.weight = form.weight.data
        patient.height = form.height.data
        patient.bloodType = form.bloodType.data
        patient.isActive = form.isActive.data

        # Commit changes to the database
        try:
            db.session.commit()
            flash("Patient information updated successfully!", "success")
            return redirect(url_for('dashboard_managers'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating patient information: {str(e)}", "danger")
    return render_template('updatePatientManager.html', patient=patient, form=form, name=current_user.userName)

# Patient self-registration
@app.route('/new_patient', methods=['GET', 'POST'])
def new_patient():
    form = PatientForm()

    if form.validate_on_submit():

        if len(form.password.data) >= 8:
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
            return redirect(url_for('new_patient'))
        else:
            flash("ERROR: Password length must be greater than 7 characters!", "success")

    return render_template('new_patient.html', form=form)

# New patient added by a manager
@app.route('/new_patient_manager', methods=['GET', 'POST'])
@login_required
def new_patient_manager():
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    form = PatientForm()

    if form.validate_on_submit():

        if len(form.password.data) >= 8:

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
            return redirect(url_for('new_patient_manager'))
        else:
            flash("ERROR: Password length must be greater than 7 characters!", "success")

    return render_template('new_patient_manager.html', form=form, name=current_user.userName)

# An Office added by another Office Manager
@app.route('/add_officeManager', methods=['GET', 'POST'])
@login_required
def add_officeManager():
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

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

# Office Clerk added by an Office Manager
@app.route('/add_officeClerk', methods=['GET', 'POST'])
@login_required
def add_officeClerk():
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative permissions to see this page!", "danger")
        return redirect(url_for('logout'))

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

# Doctor added by an Office Manager
@app.route('/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

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

# Search Patient by ID Number, so that an Office Manager can schedule a new appointment for a give patient
@app.route('/search', methods=['GET'])
@login_required
def search():
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    query = request.args.get('query', '').strip()
    if query:
        # Search patients by ID Number
        person = Person.query.filter_by(idNumber=query).first()
        if person:
            patient = Patient.query.filter_by(personID=person.id).first()
            if patient:
                return render_template('patientResults.html', patient=patient, query=query, name=current_user.userName)
    return render_template('searchPatient.html', patients=[], query=query, name=current_user.userName)

# Search Patient by ID Number, so that an Office Manager can modify and mark a given patient as Inactive
@app.route('/searchPatient', methods=['GET'])
@login_required
def searchPatient():
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    query = request.args.get('query', '').strip()
    if query:
        # Search patients by ID Number
        person = Person.query.filter_by(idNumber=query).first()
        if person:
            patient = Patient.query.filter_by(personID=person.id).first()
            if patient:
                return render_template('modifyPatientResults.html', patient=patient, query=query, name=current_user.userName)
    return render_template('searchPatientManager.html', patients=[], query=query, name=current_user.userName)

# Managers search a specific Appointment by providing Date, Time, and Patient ID, so that the appointment can be re-scheduled or canceled
@app.route('/searchAppointmentByManager', methods=["GET", "POST"])
@login_required
def searchAppointmentByManager():
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    form = SearchAppointmentByManagerForm()
    results = None

    if form.validate_on_submit():
        # Get form data
        appointment_date = form.appointmentDate.data
        appointment_time = form.appointmentTime.data
        person_id = form.patientID.data

        # Build the query dynamically
        person = Person.query.filter_by(idNumber=person_id).first()
        patient = Patient.query.filter_by(personID=person.id).first()
        all_appointments = Appointment.query.filter_by(patientID=patient.patientID)
        if appointment_date:
            all_appointments = all_appointments.filter(Appointment.appointmentDate == appointment_date)
        if appointment_time:
            all_appointments = all_appointments.filter(Appointment.appointmentTime == appointment_time)

        # Execute query
        results = all_appointments.first()
    return render_template("searchAppointmentByManager.html", form=form, appointment=results, name=current_user.userName)

# Patients search a specific Appointment by providing Date and Time, so that the appointment can be re-scheduled or canceled
@app.route('/search_appointment', methods=["GET", "POST"])
@login_required
def search_appointment():
    # Verify if the current user is a patient
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()

    if patient is None:
        flash(f"Error: You don't have access to this page!", "danger")
        return redirect(url_for('logout'))

    form = SearchAppointmentForm()
    results = None

    if form.validate_on_submit():
        # Get form data
        appointment_date = form.appointmentDate.data
        appointment_time = form.appointmentTime.data

        # Build the query dynamically
        all_appointments = Appointment.query.filter_by(patientID=patient.patientID)
        if appointment_date:
            all_appointments = all_appointments.filter(Appointment.appointmentDate == appointment_date)
        if appointment_time:
            all_appointments = all_appointments.filter(Appointment.appointmentTime == appointment_time)

        # Execute query
        results = all_appointments.first()
    return render_template("searchAppointment.html", form=form, appointment=results, name=current_user.userName)

# Patient re-schedule or cancel a given appointment
@app.route('/appointmentDetails/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def appointmentDetails(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    form = RescheduleAppointmentForm()

    # Verify if the current user is a Patient
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()

    if patient is None:
        flash(f"Error: You don't have access to this page!", "danger")
        return redirect(url_for('logout'))

    # Prepopulate the form with patient data
    if request.method == "GET":
        form.appointmentDate.data = appointment.appointmentDate
        form.appointmentTime.data = appointment.appointmentTime
        form.appointmentType.data = appointment.appointmentType

    # Process form submission
    if form.validate_on_submit():
        # Check if an appointment exists for the same patient and date
        existing_appointment = Appointment.query.filter_by(
            patientID=patient.patientID,
            appointmentDate=form.appointmentDate.data
        ).first()

        if existing_appointment:
            flash('ERROR: An appointment for this patient already exists on the selected date!', 'danger')
            return redirect(url_for('appointmentDetails', appointment_id=appointment.appointmentID))

        appointment.appointmentDate = form.appointmentDate.data
        appointment.appointmentTime = form.appointmentTime.data
        appointment.appointmentType = form.appointmentType.data

        # Commit changes to the database
        try:
            db.session.commit()

            # Create the email
            msg = Message(
                subject="Reschedule Appointment Confirmation",
                sender="aaapcsolutions@gmail.com",
                recipients=[person.email]
            )
            msg.body = f"Patient Name: {patient.person.firstName} {patient.person.lastName}\nAppointment Type: {appointment.appointmentType}\nAppointment Date: {appointment.appointmentDate}\nAppointment Time: {appointment.appointmentTime}\n\nThanks & Regards,\nMedical Scheduler Application"

            # Send the email
            try:
                mail.send(msg)
                flash("Please check your email for a confirmation message!\n", "success")
            except Exception as e:
                flash(f"Failed to send message: {e}", "danger")

            flash(
                f"{appointment.appointmentType} appointment has been rescheduled successfully for {appointment.appointmentDate} at {appointment.appointmentTime}!",
                "success")
            return redirect(url_for('dashboard', name=current_user.userName))

        except Exception as e:
            db.session.rollback()
            flash(f"Error updating appointment information: {str(e)}", "danger")
    return render_template('appointmentDetails.html', appointment=appointment, form=form, name=current_user.userName)


# Cancel and reschedule appointments by Managers
@app.route('/appointmentDetailsManager/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def appointmentDetailsManager(appointment_id):
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    appointment = Appointment.query.get_or_404(appointment_id)

    form = RescheduleAppointmentForm()
    person = Person.query.filter_by(idNumber=appointment.patient.person.idNumber).first()
    patient = Patient.query.filter_by(personID=person.id).first()

    # Prepopulate the form with patient data
    if request.method == "GET":
        form.appointmentDate.data = appointment.appointmentDate
        form.appointmentTime.data = appointment.appointmentTime
        form.appointmentType.data = appointment.appointmentType

    # Process form submission
    if form.validate_on_submit():
        # Check if an appointment exists for the same patient and date
        existing_appointment = Appointment.query.filter_by(
            patientID=patient.patientID,
            appointmentDate=form.appointmentDate.data
        ).first()

        if existing_appointment:
            flash('ERROR: An appointment for this patient already exists on the selected date!', 'danger')
            return redirect(url_for('appointmentDetailsManager', appointment_id=appointment.appointmentID))

        appointment.appointmentDate = form.appointmentDate.data
        appointment.appointmentTime = form.appointmentTime.data
        appointment.appointmentType = form.appointmentType.data

        # Commit changes to the database
        try:
            db.session.commit()

            # Create the email
            msg = Message(
                subject="Reschedule Appointment Confirmation",
                sender="aaapcsolutions@gmail.com",
                recipients=[person.email]
            )
            msg.body = f"Patient Name: {patient.person.firstName} {patient.person.lastName}\nAppointment Type: {appointment.appointmentType}\nAppointment Date: {appointment.appointmentDate}\nAppointment Time: {appointment.appointmentTime}\n\nThanks & Regards,\nMedical Scheduler Application"

            # Send the email
            try:
                mail.send(msg)
                flash("Confirmation message sent!\n", "success")
            except Exception as e:
                flash(f"Failed to send message: {e}", "danger")

            flash(
                f"{appointment.appointmentType} appointment has been rescheduled successfully for {appointment.appointmentDate} at {appointment.appointmentTime}!",
                "success")
            return redirect(url_for('patientDetails', patient_id=appointment.patient.patientID))

        except Exception as e:
            db.session.rollback()
            flash(f"Error updating appointment information: {str(e)}", "danger")
    return render_template('appointmentDetailsManager.html', appointment=appointment, form=form, name=current_user.userName)

# Patient cancel a given appointment
@app.route('/deleteAppointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def deleteAppointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    # Verify if the current user is a Patient
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()

    if patient is None:
        flash(f"Error: You don't have access to this page!", "danger")
        return redirect(url_for('logout'))

    # Commit changes to the database
    try:
        # Create the email
        msg = Message(
            subject="Appointment Cancellation Confirmation",
            sender="aaapcsolutions@gmail.com",
            recipients=[person.email]
        )
        msg.body = f"Hello,\n\nPlease see details below for the cancelled appointment:\n\nPatient Name: {patient.person.firstName} {patient.person.lastName}\nAppointment Type: {appointment.appointmentType}\nAppointment Date: {appointment.appointmentDate}\nAppointment Time: {appointment.appointmentTime}\n\nThanks & Regards,\nMedical Scheduler Application"

        # Send the email
        try:
            mail.send(msg)
            flash("Please check your email for a confirmation message!\n", "success")
        except Exception as e:
            flash(f"Failed to send message: {e}", "danger")

        flash(
            f"{appointment.appointmentType} appointment has been canceled successfully for {appointment.appointmentDate} at {appointment.appointmentTime}!",
            "success")

        db.session.delete(appointment)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting appointment information: {str(e)}", "danger")
    return redirect(url_for('dashboard', name=current_user.userName))

# Managers cancel a given appointment for a specific patient
@app.route('/deleteAppointmentManager/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def deleteAppointmentManager(appointment_id):
    # Verify if the current user is an Office Manager
    person1 = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person1.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    appointment = Appointment.query.get_or_404(appointment_id)

    person = Person.query.filter_by(idNumber=appointment.patient.person.idNumber).first()
    patient = Patient.query.filter_by(personID=person.id).first()

    # Commit changes to the database
    try:
        # Create the email
        msg = Message(
            subject="Appointment Cancellation Confirmation",
            sender="aaapcsolutions@gmail.com",
            recipients=[person.email]
        )
        msg.body = f"Hello,\n\nPlease see details below for the cancelled appointment:\n\nPatient Name: {patient.person.firstName} {patient.person.lastName}\nAppointment Type: {appointment.appointmentType}\nAppointment Date: {appointment.appointmentDate}\nAppointment Time: {appointment.appointmentTime}\n\nThanks & Regards,\nMedical Scheduler Application"

        # Send the email
        try:
            mail.send(msg)
            flash("Confirmation message sent!\n", "success")
        except Exception as e:
            flash(f"Failed to send message: {e}", "danger")

        flash(
            f"{appointment.appointmentType} appointment has been canceled successfully for {appointment.appointmentDate} at {appointment.appointmentTime}!",
            "success")

        db.session.delete(appointment)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting appointment information: {str(e)}", "danger")
    return redirect(url_for('patientDetails', patient_id=appointment.patient.patientID))

# Manager can run a report and filter appointments by providing start and end date
@app.route("/filter_appointments", methods=["GET", "POST"])
@login_required
def filter_appointments():
    # Verify if the current user is an Office Manager
    person = Person.query.filter_by(userName=current_user.userName).first()
    manager = OfficeManager.query.filter_by(personID=person.id).first()
    if manager is None:
        flash(f"Error: You don't have administrative access to see this page!", "danger")
        return redirect(url_for('logout'))

    form = DateRangeForm()
    results = None

    if form.validate_on_submit():
        # Get start and end dates from the form
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Validate date range
        if start_date > end_date:
            flash("Start date cannot be after the end date.", "danger")
        else:
            # Query appointments within the date range
            results = Appointment.query.filter(
                Appointment.appointmentDate >= start_date,
                Appointment.appointmentDate <= end_date
            ).order_by(Appointment.appointmentDate.asc()).all()

    return render_template("filterAppointments.html", form=form, results=results)

if __name__ == '__main__':
    app.run(debug=True)
