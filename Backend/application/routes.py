from flask import current_app as app , jsonify , request , abort, send_from_directory
from .models import *
from flask_jwt_extended import create_access_token , current_user , jwt_required
from .extentions import db, cache
from functools import wraps
from celery.result import AsyncResult
from .tasks import *
from datetime import date, timedelta, datetime
import time

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role not in roles:
                return jsonify(massage = "You are not authorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


@app.route("/api/login" , methods = ["POST"])
def login():
    email = request.json.get("email" , None)
    password = request.json.get("password" , None)

    user = Users.query.filter_by(email = email).one_or_none()
    if not user or not user.password == password or user.status == "block":
        return jsonify(message = "Invalid email or password or you are Blocked") ,400
    access_token = create_access_token(identity=user)
    return jsonify(access_token = access_token)


@app.route("/api/dashboard")
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        doctors = Doctor.query.all()
        patient = Patient.query.all()
        appointment = Appointment.query.all()
        reg_doct_json = []
        reg_pat_json = []
        apnt_json = []
        for doctor in doctors:
            doct_detail = {}
            doct_detail["status"] = doctor.status
            doct_detail["name"] = doctor.name
            doct_detail["department"] = doctor.department
            doct_detail["user_id"] = doctor.user_id
            doct_detail["id"] = doctor.doctor_id
            reg_doct_json.append(doct_detail)

        for patient in patient:
            pant_detail = {}
            pant_detail["status"] = patient.status
            pant_detail["name"] = patient.name
            pant_detail["id"] = patient.patient_id
            pant_detail["user_id"] = patient.user_id
            reg_pat_json.append(pant_detail)

        for appointment in appointment:
            appt_detail = {}
            appt_detail["id"] = appointment.id
            appt_detail["pt_name"] = appointment.patient.name
            appt_detail["doct_name"] = appointment.doctor.name
            appt_detail["dept_name"] = appointment.doctor.department
            appt_detail["status"] = appointment.status
            appt_detail["date"] = appointment.date
            appt_detail["time"] = appointment.time
            apnt_json.append(appt_detail)

        return jsonify({
            "role": "admin",
            "user_name": current_user.name,
            "doct_detail": reg_doct_json,
            "pant_detail": reg_pat_json,
            "apnt_detail": apnt_json
        })

    elif current_user.role == "doctor":
        doctor_id = (Doctor.query.filter_by(user_id = current_user.id).first()).doctor_id
        patient = Patient.query.join(Appointment).filter(Appointment.doctor_id == doctor_id).distinct().all()
        appointment = Appointment.query.filter_by(status = "booked", doctor_id = doctor_id).all()
        reg_pat_json = []
        apnt_json = []
        for patient in patient:
            pant_detail = {}
            pant_detail["name"] = patient.name
            pant_detail["user_id"] = patient.user_id
            reg_pat_json.append(pant_detail)

        for appointment in appointment:
            appt_detail = {}
            appt_detail["id"] = appointment.id
            appt_detail["pt_name"] = appointment.patient.name
            appt_detail["date"] = appointment.date
            appt_detail["time"] = appointment.time
            apnt_json.append(appt_detail)

        return jsonify({
            "role": "doctor",
            "doctor_id": doctor_id,
            "status": current_user.status,
            "user_name": current_user.name,
            "pant_detail": reg_pat_json,
            "apnt_detail": apnt_json
        })

    else:
        patient_id = (Patient.query.filter_by(user_id = current_user.id).first()).patient_id
        appointment = Appointment.query.filter_by(patient_id = patient_id).all()
        departments = Department.query.filter(Department.doctor_registered > 0).all()
        dept_json = []
        apnt_json = []
        for appointment in appointment:
            appt_detail = {}
            appt_detail["id"] = appointment.id
            appt_detail["doct_name"] = appointment.doctor.name
            appt_detail["doct_id"] = appointment.doctor.doctor_id
            appt_detail["dept_name"] = appointment.doctor.department
            appt_detail["date"] = appointment.date
            appt_detail["time"] = appointment.time
            appt_detail["status"] = appointment.status
            apnt_json.append(appt_detail)

        for department in departments:
            dept_detail = {}
            dept_detail["name"] = department.department_name
            dept_json.append(dept_detail)

        return jsonify({
            "role": "patient",
            "user_id": current_user.id,
            "status": current_user.status,
            "patient_id": patient_id,
            "user_name": current_user.name,
            "dept_detail": dept_json,
            "apnt_detail": apnt_json
        })

@app.route("/api/register" ,methods = ["POST"])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    name = request.json.get("name", None)

    user = Users.query.filter_by(email = email).first()
    if user:
        return jsonify(message = "User already exists") ,409
    
    if email and password and name:
        user = Users(name = name, email = email , password = password)
        db.session.add(user)
        db.session.commit()

        p_user = Users.query.filter_by(email = email).first()

        patient = Patient(name = name, user_id = p_user.id)
        db.session.add(patient)
        db.session.commit()

        return jsonify(message = "Registration successfully you can login now")
    else:
        return jsonify(message = "Form should not be empty") , 400

@app.route("/api/add_doctor", methods = ["POST"])
@role_required("admin")
def add_doct():
    email = request.json.get("email",None)
    password = request.json.get("password", None)
    name = request.json.get("name", None)
    department = request.json.get("department", None)
    exp_year = request.json.get("exp_year", None)
    degree = request.json.get("degree", None)
    specialty = request.json.get("specialty", None)

    user = Users.query.filter_by(email = email).first()
    if user:
        return jsonify(message = "User already exists") ,400

    if name and email and password and department and exp_year and degree and specialty:
        user = Users(name = name, email = email , password = password, role = "doctor")
        db.session.add(user)
        dept = Department.query.filter_by(department_name = department).first()
        if dept:
            dept.doctor_registered += 1
            db.session.commit()
        else:
            depart = Department(department_name = department, doctor_registered = 1)
            db.session.add(depart)
            db.session.commit()

        n_user = Users.query.filter_by(email = email).first()

        new_doct = Doctor(name = name, department = department, exp_year = exp_year , user_id = n_user.id , degree = degree, specialty = specialty)
        db.session.add(new_doct)
        db.session.commit()
        cache.delete_memoized(dept_doctor, department)
        return jsonify(message = "doctor added successfully")
    
    else:
        return jsonify(message = "Form should not be empty") , 400

@app.route("/api/editdoct/<int:id>" ,methods = ["GET", "POST"])
@role_required("admin")
def editdoct(id):
    user = Users.query.filter_by(id = id).first()
    name = request.json.get("name", None)
    department = request.json.get("department", None)
    exp_year = request.json.get("exp_year", None)
    degree = request.json.get("degree", None)
    specialty = request.json.get("specialty", None)

    if request.method == "POST":
        if name and department and exp_year and degree and specialty:
            doctor = Doctor.query.filter_by(user_id = id).first()
            doctor.name = name
            doctor.department = department
            doctor.degree = degree
            doctor.specialty = specialty
            doctor.exp_year = exp_year
            user.name = name
            db.session.commit()
            cache.delete_memoized(detail, id)
            cache.delete_memoized(dept_doctor, department)
            return jsonify(message = "edit successfully")
        else:
            return jsonify(message = "Form should not be empty") , 400

    

@app.route("/api/editpat/<int:id>" ,methods = ["GET", "POST"])
@jwt_required()
def editpat(id):
    patient = Patient.query.filter_by(patient_id = id).first()
    user = Users.query.filter_by(id = patient.user_id).first()
    name = request.json.get("name", None)

    if request.method == "POST":
        if current_user.role == "patient":
            password = request.json.get("password", None)
            if name and password:
                user.password = password
                user.name = name
                patient.name = name
                db.session.commit()
                cache.delete_memoized(detail, patient.user_id)
                return jsonify(message = "edit successfully")
            else:
                return jsonify(message = "Form should not be empty") , 400
        else:
            if name:
                user.name = name
                patient.name = name
                db.session.commit()
                cache.delete_memoized(detail, patient.user_id)
                return jsonify(message = "edit successfully")
            else:
                return jsonify(message = "Form should not be empty") , 400


@app.route("/api/delete/<int:id>" ,methods = ["POST"])
@role_required("admin")
def delete(id):
    user = Users.query.filter_by(id = id).first()
    if user.role == "doctor":
        doctor = Doctor.query.filter_by(user_id = id).first()
        depart = Department.query.filter_by(department_name = doctor.department).first()
        if request.method == "POST":
            db.session.delete(doctor)
            db.session.delete(user)
            depart.doctor_registered -= 1
            db.session.commit()
            cache.delete_memoized(dept_doctor, doctor.department)
    
    if user.role == "patient":
        patient = Patient.query.filter_by(user_id = id).first()
        if request.method == "POST":
            db.session.delete(patient)
            db.session.delete(user)
            db.session.commit()

    return jsonify(message = "Delete successfully")

@app.route("/api/block/<int:id>" ,methods = ["POST"])
@role_required("admin")
def Block(id):
    user = Users.query.filter_by(id = id).first()
    
    if user.role == "doctor":
        doctor = Doctor.query.filter_by(user_id = id).first()
        Depart = Department.query.filter_by(department_name = doctor.department).first()
        if request.method == "POST":
            doctor.status = "block"
            user.status = "block"
            Depart.doctor_registered -= 1
            db.session.commit()
            cache.delete_memoized(dept_doctor, doctor.department)

    if user.role == "patient":
        patient = Patient.query.filter_by(user_id = id).first()
        if request.method == "POST":
            patient.status = "block"
            user.status = "block"
            db.session.commit()

    return jsonify(message = "Block successfully")

@app.route("/api/unblock/<int:id>" ,methods = ["POST"])
@role_required("admin")
def unblock(id):
    user = Users.query.filter_by(id = id).first()

    if user.role == "doctor":
        doctor = Doctor.query.filter_by(user_id = id).first()
        Depart = Department.query.filter_by(department_name = doctor.department).first()
        if request.method == "POST":
            doctor.status = "active"
            user.status = "active"
            Depart.doctor_registered += 1
            db.session.commit()
            cache.delete_memoized(dept_doctor, doctor.department)

    if user.role == "patient":
        patient = Patient.query.filter_by(user_id = id).first()
        if request.method == "POST":
            patient.status = "active"
            user.status = "active"
            db.session.commit()

    return jsonify(message = "unblock successfully")


@app.route("/api/provide_av/<int:id>",methods = ["GET", "POST"])
@role_required("doctor")
def provide_av(id):
    doctor = Doctor.query.filter_by(doctor_id = id).first()
    if doctor:
        for i in range(7):
            dates = date.today() + timedelta(days=i)
            already_av = Slots.query.filter_by(date = dates, doctor_id = id).first()
            if not already_av:
                slot = Slots(doctor_id = id , date = dates)
                db.session.add(slot)
        db.session.commit()
        date3 = date.today()
        slot = Slots.query.filter_by(doctor_id = id).filter(Slots.date >= date3).all()
        slot_json = []
        for slot in slot:
            slot_detail = {}
            slot_detail["id"] = slot.id
            slot_detail["date"] = slot.date
            slot_detail["slot1"] = slot.slot1
            slot_detail["slot2"] = slot.slot2
            slot_detail["slot3"] = slot.slot3
            slot_json.append(slot_detail)
        return jsonify({
            "slot_detail": slot_json
        }) 
    else:
        return jsonify(message = "Doctor does not exist")
    
@app.route("/api/change/<int:doctor_id>/<int:id>/<int:st>",methods = ["POST"])
@role_required("doctor", "admin")
def save(doctor_id, id, st):   
    slot = Slots.query.filter_by(doctor_id = doctor_id , id = id).first()
    if request.method == "POST":
        if st == 1:
            if slot.slot1 == "available":
                slot.slot1 = "na"
            elif slot.slot1 == "na":
                slot.slot1 = "available"
            db.session.commit()

        elif st == 2:
            if slot.slot2 == "available":
                slot.slot2 = "na"
            elif slot.slot2 == "na":
                slot.slot2 = "available"
            db.session.commit()

        else:
            if slot.slot3 == "available":
                slot.slot3 = "na"
            elif slot.slot3 == "na":
                slot.slot3 = "available"
            db.session.commit()
    return jsonify(message = "Availability Provide Successfully")


@app.route("/api/detail/<int:id>")
@cache.memoize(timeout=0)
@jwt_required()
def detail(id):
    # time.sleep(5)  -> for demonstration
    user = Users.query.filter_by(id = id).first()
    if user:
        if user.role == "doctor":
            doctor = Doctor.query.filter_by(user_id = id).first()
            doct_detail = {}
            doct_detail["status"] = doctor.status
            doct_detail["name"] = doctor.name
            doct_detail["department"] = doctor.department
            doct_detail["user_id"] = doctor.user_id
            doct_detail["id"] = doctor.doctor_id
            doct_detail["degree"] = doctor.degree
            doct_detail["specialty"] = doctor.specialty
            doct_detail["exp_year"] = doctor.exp_year
            return jsonify({
                "doct_detail": doct_detail
            })
        
        if user.role == "patient":
            patient = Patient.query.filter_by(user_id = id).first()
            patient_id = patient.patient_id
            appointment = Appointment.query.filter_by(patient_id = patient_id , status = "cancelled").all()
            treatment = Treatment.query.join(Appointment).filter(Appointment.patient_id == patient_id).all()
            
            apnt_json = []
            treat_json = []

            for appointment in appointment:
                appt_detail = {}
                appt_detail["id"] = appointment.id
                appt_detail["doct_name"] = appointment.doctor.name
                appt_detail["dept_name"] = appointment.doctor.department
                appt_detail["date"] = appointment.date
                appt_detail["time"] = appointment.time
                apnt_json.append(appt_detail)

            for treatment in treatment:
                treat_detail = {}
                treat_detail["id"] = treatment.id
                treat_detail["visit_type"] = treatment.visit_type
                treat_detail["test_done"] = treatment.test_done
                treat_detail["medicines"] = treatment.medicines
                treat_detail["diagnosis"] = treatment.diagnosis
                treat_detail["prescription"] = treatment.prescription
                treat_detail["notes"] = treatment.notes
                treat_detail["doctor"] = treatment.appointment.doctor.name
                treat_detail["department"] = treatment.appointment.doctor.department
                treat_json.append(treat_detail)


            pant_detail = {}
            pant_detail["status"] = patient.status
            pant_detail["name"] = patient.name
            pant_detail["user_id"] = patient.user_id
            pant_detail["id"] = patient.patient_id

            return jsonify({
                "pant_detail": pant_detail,
                "appointment": apnt_json,
                "treatment": treat_json
            })
    else:
        return jsonify(message = "User doesn't exists")


@app.route("/api/dept_doctor/<name>")
@cache.memoize(timeout=0)
@jwt_required()
def dept_doctor(name):
    # time.sleep(5) -> for demonstration
    doctors = Doctor.query.filter_by(department = name, status = "active").all()
    reg_doct_json = []
    for doctor in doctors:
        doct_detail = {}
        doct_detail["name"] = doctor.name
        doct_detail["user_id"] = doctor.user_id
        doct_detail["id"] = doctor.doctor_id
        reg_doct_json.append(doct_detail)

    return jsonify({
        "doct_detail": reg_doct_json,
    })


@app.route("/api/slot_dt/<int:id>")
@role_required("patient" , "admin")
def slot_dt(id):
    date1 = date.today()
    slot = Slots.query.filter_by(doctor_id = id).filter(Slots.date >= date1).all()
    slot_json = []
    for slot in slot:
        slot_detail = {}
        slot_detail["id"] = slot.id
        slot_detail["date"] = slot.date
        slot_detail["slot1"] = slot.slot1
        slot_detail["slot2"] = slot.slot2
        slot_detail["slot3"] = slot.slot3
        slot_json.append(slot_detail)
    return jsonify({
        "slot_detail": slot_json
    }) 


@app.route("/api/book/<int:doctor_id>/<int:patient_id>/<int:id>/<int:st>/<path:dates>",methods = ["POST"])
@role_required("patient")
def book(doctor_id, patient_id, id, st, dates):   
    slot = Slots.query.filter_by(doctor_id = doctor_id , id = id).first()
    date_n = datetime.strptime(dates, '%a, %d %b %Y %H:%M:%S %Z').date()
    if request.method == "POST":
        if st == 1:
            apt_detail = Appointment.query.filter_by(patient_id = patient_id, time = "8 AM - 11 AM", date = date_n, status = "booked").first()
            if apt_detail:
                return jsonify(message = "You already booked an appointment on this time so book another slot"), 400
            
            appointment = Appointment(patient_id = patient_id, doctor_id = doctor_id, time = "8 AM - 11 AM", date = date_n)
            db.session.add(appointment)
            slot.slot1 = "booked"
            db.session.commit()

        elif st == 2:
            apt_detail = Appointment.query.filter_by(patient_id = patient_id, time = "1 PM - 4 PM", date = date_n, status = "booked").first()
            if apt_detail:
                return jsonify(message = "You already booked an appointment on this time so book another slot"), 400
            
            slot.slot2 = "booked"
            appointment = Appointment(patient_id = patient_id, doctor_id = doctor_id, time = "1 PM - 4 PM", date = date_n)
            db.session.add(appointment)
            db.session.commit()

        else:
            apt_detail = Appointment.query.filter_by(patient_id = patient_id, time = "6 PM - 9 PM", date = date_n, status = "booked").first()
            if apt_detail:
                return jsonify(message = "You already booked an appointment on this time so book another slot"), 400

            slot.slot3 = "booked"
            appointment = Appointment(patient_id = patient_id, doctor_id = doctor_id, time = "6 PM - 9 PM", date = date_n)
            db.session.add(appointment)
            db.session.commit()
    return jsonify(message = "Booked Successfully")


@app.route("/api/cancel/<int:id>" ,methods = ["POST"])
@jwt_required()
def cancel(id):
    appointment = Appointment.query.filter_by(id = id).first()
    user_id = appointment.patient.user_id
    doctor_id = appointment.doctor_id
    date = appointment.date
    time = appointment.time
    appointment.status = "cancelled"
    slot = Slots.query.filter_by(doctor_id = doctor_id, date = date).first()
    if time == "8 AM - 11 AM":
        slot.slot1 = "available"
        db.session.commit()

    elif time == "1 PM - 4 PM":
        slot.slot2 = "available"
        db.session.commit()

    else:
        slot.slot3 = "available"
        db.session.commit()

    cache.delete_memoized(detail, user_id)
    return jsonify(message = "Cancel successfully")

@app.route("/api/reschedule/<int:id>" ,methods = ["POST"])
@jwt_required()
def reschedule(id):
    appointment = Appointment.query.filter_by(id = id).first()
    doctor_id = appointment.doctor_id
    date = appointment.date
    time = appointment.time
    db.session.delete(appointment)
    slot = Slots.query.filter_by(doctor_id = doctor_id, date = date).first()
    if time == "8 AM - 11 AM":
        slot.slot1 = "available"
        db.session.commit()

    elif time == "1 PM - 4 PM":
        slot.slot2 = "available"
        db.session.commit()

    else:
        slot.slot3 = "available"
        db.session.commit()

    return jsonify(message = "Rescheduled successfully")

@app.route("/api/treatment/<int:id>", methods = ["GET","POST"])
@role_required("doctor")
def treatment(id):
    visit_type = request.json.get("visit_type",None)
    test_done = request.json.get("test_done", None)
    diagnosis = request.json.get("diagnosis", None)
    prescription = request.json.get("prescription", None)
    medicines = request.json.get("medicines", None)
    notes = request.json.get("notes", None)

    if request.method == "POST":
        treatment = Treatment(appointment_id = id, visit_type = visit_type, test_done = test_done, diagnosis = diagnosis, prescription = prescription, medicines = medicines, notes = notes)
        db.session.add(treatment)
    
        appointment = Appointment.query.filter_by(id = id).first()
        patient_user_id = appointment.patient.user_id
        doctor_id = appointment.doctor_id
        date = appointment.date
        time = appointment.time
        appointment.status = "completed"
        slot = Slots.query.filter_by(doctor_id = doctor_id, date = date).first()
        if time == "8 AM - 11 AM":
            slot.slot1 = "complete"
            db.session.commit()

        elif time == "1 PM - 4 PM":
            slot.slot2 = "complete"
            db.session.commit()

        else:
            slot.slot3 = "complete"
            db.session.commit()

        cache.delete_memoized(detail, patient_user_id)
        return jsonify(message = "Treatment successfully")


@app.route("/api/apnt_dt/<int:id>")
@role_required("doctor")
def apnt_dt(id):  
    appointment = Appointment.query.filter_by(id = id).first()
    patient_name = appointment.patient.name
    department = appointment.doctor.department

    return jsonify({
        "patient_name": patient_name,
        "department": department
    })



# Caching
@app.route("/api/clear-cache" ,methods = ["POST"])
@role_required("admin")
def clear_cache():
    cache.clear()
    return "All cache cleared!"



# Backend Job
@app.route('/api/export_csv/<int:patient_id>')
@role_required("patient")
def export(patient_id):
    result = csv_report.delay(patient_id)
    return {
        "id": result.id,
    }

@app.route('/api/csv_result/<task_id>')
@role_required("patient")
def csv_result(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        if res.successful():
            return send_from_directory('static', res.result), 200
        else:
            return jsonify(message = "Failed"), 400
    else:
        return jsonify(message = "Pending"), 202
