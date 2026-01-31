from celery import shared_task 
import csv
from jinja2 import Template
from .mail import send_email
from .models import *
from datetime import datetime , date , timedelta
import requests


# task 1 - Download CSV report for patient
@shared_task(ignore_results = False, name = "download_csv_report")
def csv_report(patient_id):
    treatment = Treatment.query.join(Appointment).filter(Appointment.patient_id == patient_id).all()
    csv_file_name = f"card_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.csv" 
    with open(f'static/{csv_file_name}', 'w', newline = "") as csvfile:
        sr_no = 1
        card_csv = csv.writer(csvfile, delimiter = ',')
        card_csv.writerow(['Sr No.', 'Doctor Name', 'Department', 'Date', 'Visit Type', 'Test done', 'Prescription', 'Medicines', 'Diagnosis', 'Doctor Notes'])
        for treat in treatment:
            detail = [sr_no, treat.appointment.doctor.name, treat.appointment.doctor.department, treat.appointment.date.strftime('%d-%m-%Y'), treat.visit_type, treat.test_done, treat.prescription, treat.medicines, treat.diagnosis, treat.notes]
            card_csv.writerow(detail)
            sr_no += 1

    return csv_file_name


# task 2 - Monthly report sent via mail 
@shared_task(ignore_results = False, name = "monthly_report")
def monthly_report():
    doctors = Users.query.filter_by(role = "doctor").all()
    previous_month = (date.today() - timedelta(days=30)).strftime("%B")

    for doctor in doctors:
        cancelled_appoint = Appointment.query.join(Doctor).filter(Appointment.status == "cancelled", Appointment.date >= (date.today() - timedelta(days=30)) , Appointment.date < date.today()).filter(Doctor.user_id == doctor.id).all()
        details = []
        treatment = Treatment.query.join(Appointment).join(Doctor).filter(Appointment.date >= (date.today() - timedelta(days=30)) , Appointment.date < date.today()).filter(Doctor.user_id == doctor.id).all()
        for info in treatment:
            info_dict = {}
            info_dict["patient_name"] = info.appointment.patient.name
            info_dict["visit_type"] = info.visit_type
            info_dict["test_done"] = info.test_done
            info_dict["medicines"] = info.medicines
            info_dict["diagnosis"] = info.diagnosis
            info_dict["prescription"] = info.prescription
            info_dict["notes"] = info.notes
            details.append(info_dict)
        doctor_data = {
        "doctor_name" : doctor.name,
        "email" : doctor.email,
        "details": details,
        "cancelled_appoint": len(cancelled_appoint),
        "patient_seen": len(treatment),
        "previous_month": previous_month

        }

        mail_template = """
        <h3>Dear Dr.&nbsp;{{ doctor_data.doctor_name }}</h3>
        <p>This email is being sent on behalf of Hospital Management Team to provide you with the consolidated appointment summary for the month of&nbsp;{{ doctor_data.previous_month }}.</p>
        <p>Below are the details of the patient consultations and visits handled during this period:</p>
        <table border="1">
            <tr>
                <th>Sr.No.</th>
                <th>Patient Name</th>
                <th>Visit Type</th>
                <th>Test Done</th>
                <th>Diagnosis</th>
                <th>Prescription</th>
                <th>Medicines</th>
                <th>Doctor Notes</th>
            </tr>
            {% for detail in doctor_data.details %}
            <tr>
                <td>{{ loop.index }} </td>
                <td>{{ detail.patient_name }}</td>
                <td>{{ detail.visit_type }}</td>
                <td>{{ detail.test_done }}</td>
                <td>{{ detail.diagnosis }}</td>
                <td>{{ detail.prescription }}</td>
                <td>{{ detail.medicines }}</td>
                <td>{{ detail.notes }}</td>
            </tr>
            {% endfor %}
        </table>
        <h4>Summary of the Month :</h4>

        <h4>Total Patients Seen : {{ doctor_data.patient_seen }} </h4>

        <h4>Total Cancellations/No-shows: {{ doctor_data.cancelled_appoint }}</h4>
        <p>Please feel free to reach out to the administration department if you require any specific data or adjustments in the upcoming schedule.</p>    
        <p>Thank you for your continued service and dedication.</p>
        <h5>Best Regards</h5>
        <h5>Hospital Management Team</h5>
        <h5>IITM BS Degree</h5>
        """
        message = Template(mail_template).render(doctor_data = doctor_data)

        send_email(doctor.email, subject = f"{previous_month} Month Report", message = message)
    return "Monthly reports sent" 



# task 3 - g-chat webhook
@shared_task(ignore_results = False, name = "daily_update")
def daily_update():
    patients = Patient.query.join(Appointment).filter(Appointment.date == date.today()).all()
    for patient in patients:
        doctors = Doctor.query.join(Appointment).join(Patient).filter(Appointment.date == date.today()).filter(Patient.patient_id == patient.patient_id).all()
        for doctor in doctors: 
            apt_time = Appointment.query.join(Patient).join(Doctor).filter(Doctor.doctor_id == doctor.doctor_id).filter(Appointment.date == date.today(), Appointment.status == "booked").filter(Patient.patient_id == patient.patient_id).all()
            apt_tm = [item.time for item in apt_time]
            time_string = " and ".join(apt_tm)
            text = f"Hi {patient.name}, You have an appointment scheduled for today at { time_string } with Doctor { doctor.name}. Please remember to bring: your ID card and previous prescriptions/reports."
            response = requests.post("https://chat.googleapis.com/v1/spaces/AAQANiJ4z3A/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=egWj2BApV2897JLzY39yh0QBzOUt3JpCvKZ4rriwGRE", json = {"text": text})
            print(response.status_code)
    return "The delivery is sent to user"
