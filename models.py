# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

db = SQLAlchemy()

class MedicalOffice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    officeName = db.Column(db.String(100), nullable=False)
    officeAddress = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    faxNumber = db.Column(db.String(20), nullable=False)

class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idNumber = db.Column(db.String(20), nullable=False, unique=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    dateOfBirth = db.Column(db.String, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)

class Patient(db.Model):
    patientID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bloodType = db.Column(db.String(5), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)
    personID = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = db.relationship('Person', backref='patients')

class Doctor(db.Model):
    doctorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    licenseNumber = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    personID = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = db.relationship('Person', backref='doctors')

class OfficeManager(db.Model):
    managerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personID = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = db.relationship('Person', backref='managers')

class StaffMember(db.Model):
    staffID = db.Column(db.Integer, primary_key=True)
    personID = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = db.relationship('Person', backref='staffmembers')

class Appointment(db.Model):
    appointmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointmentDate = db.Column(db.String, nullable=False)
    appointmentTime = db.Column(db.Time, nullable=False)
    appointmentType = db.Column(db.String(50), nullable=False)
    patientID = db.Column(db.Integer, db.ForeignKey('patient.patientID'), nullable=False)
    doctorID = db.Column(db.Integer, db.ForeignKey('doctor.doctorID'), nullable=False)
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

class Schedule(db.Model):
    scheduleID = db.Column(db.Integer, primary_key=True)
    doctorID = db.Column(db.Integer, db.ForeignKey('doctor.doctorID'), nullable=False)
    scheduleDay = db.Column(db.String(20), nullable=False)
    scheduleTimeFrom = db.Column(db.String(20), nullable=False)
    scheduleTimeTo = db.Column(db.String(20), nullable=False)
    doctor = db.relationship('Doctor', backref='schedules')
