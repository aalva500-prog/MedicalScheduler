# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Person, Patient, Doctor, OfficeManager, StaffMember, Appointment
from forms import AppointmentForm, PatientForm, LoginForm, OfficeManagerForm, DoctorForm, OfficeClerkForm, \
    AppointmentManagerForm, UpdatePatientForm, SearchAppointmentForm, RescheduleAppointmentForm, DateRangeForm, \
    SearchAppointmentByManagerForm, UpdatePatientManagerForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message

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

mail = Mail(app)

@login_manager.user_loader
def load_user(id):
    return Person.query.get(int(id))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments')
@login_required
def appointments():
    all_appointments = Appointment.query.order_by(Appointment.appointmentDate.desc()).all()
    return render_template('appointments.html', appointments=all_appointments, name=current_user.userName)

@app.route('/appointments')
@login_required
def appointmentsByTime(patient_id):
    all_appointments = Appointment.query.order_by(Appointment.appointmentDate.desc()).all()
    return render_template('appointments.html', appointments=all_appointments, name=current_user.userName)

@app.route('/appointmentsByPatient')
@login_required
def appointmentsByPatient():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()
    all_appointments = Appointment.query.filter_by(patientID = patient.patientID).order_by(Appointment.appointmentDate.desc()).all()
    return render_template('appointmentsByPatient.html', appointmentsByPatient=all_appointments, name=current_user.userName)

@app.route('/patients')
@login_required
def patients():
    all_patients = Patient.query.order_by().all()
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
@app.route('/update_patient', methods=['GET', 'POST'])
@login_required
def update_patient():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()
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
        if user:
            patient = Patient.query.filter_by(personID=user.id).first()
            if patient and patient.isActive == True:
                if user.password == password:
                    login_user(user)  # Create session for the user
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password!', 'danger')
            else:
                flash('Your account is Inactive. Please contact the Administrator to active your Account!', 'danger')
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

# View and schedule appointments
@login_required
@app.route('/patientDetails/<int:patient_id>', methods=['GET', 'POST'])
def patientDetails(patient_id):
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
        msg.body = f"Patient Name: {patient.person.firstName} {patient.person.lastName}\nAppointment Type: {appointment.appointmentType} \n Appointment Date: {appointment.appointmentDate} \nAppointment Time: {appointment.appointmentTime}\n\nThanks & Regards,\nMedical Scheduler Application"

        # Send the email
        try:
            mail.send(msg)
            flash("Please check your email for a confirmation message!\n", "success")
        except Exception as e:
            flash(f"Failed to send message: {e}", "danger")

        flash(
            f"{appointment.appointmentType} appointment has been scheduled successfully for {appointment.appointmentDate} at {appointment.appointmentTime}!",
            "success")
        return redirect(url_for('patientDetails', patient_id=patient.patientID))
    return render_template('patientDetails.html', patient=patient, form=form, name=current_user.userName, appointments=all_appointments)

# View and schedule appointments
@login_required
@app.route('/modifyPatientDetails/<int:patient_id>', methods=['GET', 'POST'])
def modifyPatientDetails(patient_id):
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
        return redirect(url_for('new_patient'))

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
        return redirect(url_for('new_patient_manager'))

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

# Search Patient by ID Number
@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '').strip()
    if query:
        # Search patients by ID Number
        person = Person.query.filter_by(idNumber=query).first()
        if person:
            patient = Patient.query.filter_by(personID=person.id).first()
            if patient:
                return render_template('patientResults.html', patient=patient, query=query, name=current_user.userName)
    return render_template('searchPatient.html', patients=[], query=query, name=current_user.userName)

@app.route('/searchPatient', methods=['GET'])
@login_required
def searchPatient():
    query = request.args.get('query', '').strip()
    if query:
        # Search patients by ID Number
        person = Person.query.filter_by(idNumber=query).first()
        if person:
            patient = Patient.query.filter_by(personID=person.id).first()
            if patient:
                return render_template('modifyPatientResults.html', patient=patient, query=query, name=current_user.userName)
    return render_template('searchPatientManager.html', patients=[], query=query, name=current_user.userName)

# Search Appointment by Patient
@app.route('/searchAppointmentByManager', methods=["GET", "POST"])
@login_required
def searchAppointmentByManager():
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

@app.route('/search_appointment', methods=["GET", "POST"])
@login_required
def search_appointment():
    person = Person.query.filter_by(userName=current_user.userName).first()
    patient = Patient.query.filter_by(personID=person.id).first()
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

# View and reschedule appointments
@login_required
@app.route('/appointmentDetails/<int:appointment_id>', methods=['GET', 'POST'])
def appointmentDetails(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    form = RescheduleAppointmentForm()
    person = Person.query.filter_by(userName=current_user.userName).first()
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
@login_required
@app.route('/appointmentDetailsManager/<int:appointment_id>', methods=['GET', 'POST'])
def appointmentDetailsManager(appointment_id):
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

@login_required
@app.route('/deleteAppointment/<int:appointment_id>', methods=['GET', 'POST'])
def deleteAppointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    person = Person.query.filter_by(userName=current_user.userName).first()
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

@login_required
@app.route('/deleteAppointmentManager/<int:appointment_id>', methods=['GET', 'POST'])
def deleteAppointmentManager(appointment_id):
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

@app.route("/filter_appointments", methods=["GET", "POST"])
def filter_appointments():
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
