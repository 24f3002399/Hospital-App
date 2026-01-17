from .extentions import db
from datetime import date, time

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique= True)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.String, default="patient")
    status = db.Column(db.String, default="active")

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    patient_id =db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.doctor_id'))
    date = db.Column(db.Date)
    time = db.Column(db.String)
    status = db.Column(db.String, default = "booked")
    doctor = db.relationship("Doctor", backref="appointment_doctor")
    patient = db.relationship("Patient", backref="appointment_patient")

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    appointment_id = db.Column(db.Integer ,db.ForeignKey('appointment.id'))
    diagnosis = db.Column(db.String)
    prescription = db.Column(db.String)
    notes = db.Column(db.String)

class Department(db.Model):
    department_id = db.Column(db.Integer, primary_key = True)
    department_name = db.Column(db.String, unique = True)
    doctor_registered = db.Column(db.Integer)

class Doctor(db.Model):
    doctor_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    degree = db.Column(db.String)
    specialty = db.Column(db.String) 
    department = db.Column(db.String, db.ForeignKey('department.department_name'))
    exp_year = db.Column(db.Integer)
    status = db.Column(db.String, default="active")
    user = db.relationship("Users", backref="doctor_info", uselist=False)


class Slots(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    doctor_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    slot1 = db.Column(db.String(), default = 'available')
    slot2 = db.Column(db.String(), default = 'available')
    slot3 = db.Column(db.String(), default = 'available')

class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    status = db.Column(db.String, default="active")
    user = db.relationship("Users", backref="patient_profile", uselist=False)