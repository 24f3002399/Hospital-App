# 🏥 Full-Stack Hospital Management System (HMS)

![Vue.js](https://img.shields.io/badge/Vue.js-3.0-4FC08D?style=for-the-badge&logo=vue.js)
![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A robust, highly scalable, and asynchronous Full-Stack Hospital Management Application. This project bridges the gap between hospital administrators, doctors, and patients through a seamless digital interface. 

**Developed as a comprehensive project for the Bachelor of Science (BS) in Data Science and Applications program at the Indian Institute of Technology Madras (IITM).**

---

## ✨ Key Features & Functionalities

### 👨‍💼 1. Role-Based Access Control (RBAC) & Management
Secure dashboards tailored for specific users using **JWT (JSON Web Tokens)**:
*   **Admin:** Complete system control. Can onboard doctors, manage user access via soft-restricting (**Block/Unblock** functionality), permanently delete users, view platform statistics, and clear server caches.
*   **Doctor:** Can generate and manage real-time availability slots across multiple shifts, view scheduled appointments, and record patient treatments/diagnoses.
*   **Patient:** Can browse departments, search for doctors, book/reschedule/cancel appointments, edit profile credentials, and view their complete Electronic Health Record (EHR).

### 🔍 2. Instant Client-Side Search & Filtering
*   Implemented optimization using Vue `computed` properties for real-time filtering.
*   **Admin Dashboard:** Search registered doctors instantly by *Name* or *Department*, and patients by *ID* or *Name* without hitting the database repeatedly.
*   **Patient Dashboard:** Real-time instantaneous search for clinical departments as the user types.

### 📅 3. Dynamic Appointment & Slot Management
*   Doctors can toggle their availability dynamically across three major shifts (8 AM - 11 AM, 1 PM - 4 PM, 6 PM - 9 PM). 
*   **Concurrency Protection:** Active appointments are safely guarded. Once a patient books a slot, the frontend automatically disables that specific slot on the Doctor's availability panel, preventing accidental data overrides or deletion.
*   Overlapping or duplicate bookings are natively restricted by the backend API architecture.

### ⚕️ 4. Electronic Health Records (EHR) Module
*   Dedicated `Treatment` workflow where doctors log *Visit Type (In-person vs. Tele-consultation), Tests Done, Diagnosis, Prescriptions, and Notes*.
*   Patients have a custom toggle interface to separate *Completed Treatments* from *Cancelled/Past Appointments* smoothly on a single view.

### ⚡ 5. Asynchronous Background Jobs (Celery + Redis)
To ensure the Flask API never blocks during heavy data transactions, **Celery** handles background processing:
*   **Asynchronous CSV Export:** Patients can trigger a request to export their entire medical case history. The backend immediately drops an `HTTP 202 Accepted` response. The Vue frontend executes **Asynchronous Polling (Long Polling)** with `setTimeout` to track the task state, automatically triggering a native browser download once the file is ready (`HTTP 200 OK`).

### 🔔 6. Automated Cron Jobs & Notifications (Celery Beat)
*   **Google Chat Webhook Integration:** A automated daily batch script runs at 7:00 AM, scanning the SQLite DB for upcoming appointments of the day and pushing real-time alerts to a Google Chat Space.
*   **Monthly Performance Reports:** Automated Jinja2-templated HTML medical summaries are dispatched to active doctors on the 1st of every month, reporting their transactional metrics.

### 🚀 7. Caching & Performance Optimization
*   **Redis Caching (`Flask-Caching`):** High-frequency database queries are cached in Redis memory to enhance response delivery. Admins can flush this cache on-demand using a dedicated server sync layout.

---

## 🛠️ Technology Stack

### **Frontend:**
*   **Framework:** Vue.js 3 (Options API / Single File Components)
*   **Build Tool:** Vite (Optimized production asset compilation)
*   **Routing:** Vue Router v4 (with Global/Per-Route Navigation Guards)
*   **HTTP Client:** Axios (Interceptors for Bearer JWT Token Authorization)
*   **Styling:** Bootstrap 5 (Responsive Layout Grids) & Custom Scoped CSS

### **Backend:**
*   **Framework:** Python 3 & Flask (RESTful API Design)
*   **Database & ORM:** SQLite with Flask-SQLAlchemy
*   **Authentication:** Flask-JWT-Extended (Stateless Security)
*   **Message Broker & Cache:** Redis Server
*   **Task Workers:** Celery & Celery Beat Scheduler
*   **Automated Mailing:** Python `smtplib` & `email.mime`
*   **Integrations:** Google Chat Webhooks API

---

## 🗺️ Project Architecture & Routes

### Frontend Router Ecosystem
| Path | Component / Target | Description |
| :--- | :--- | :--- |
| `/` | `Content.vue` | Public Gateway Landing Page |
| `/login` , `/register` | Public Scope | Identity Management & Auth handles |
| `/admindash` | Admin Exclusive | Global Admin Command Center & Cache controller |
| `/doctordash` | Doctor Exclusive | Doctor's workflow portal |
| `/patientdash` | Patient Exclusive | Patient's center & department explorer |
| `/adminchangeav/:id` | Admin / Doctor | Shift Allocation & Grid config interface |
| `/treatment/:id` | Doctor | Diagnostic form & Prescription builder |
| `/book/:id` | Patient | Real-time calendar slot reservation gateway |
| `/patientdt/:id` | Shared Medical | Comprehensive Patient Medical History Record (EHR) |
| `/editpat/:id` | Shared Context | Profile information management form |

---

## 🚀 Local Installation & Setup Guide

### System Prerequisites
*   Node.js (v16+) & npm package manager
*   Python (v3.8+ architecture)
*   Redis Server running locally on standard port `6379`
*   MailHog local SMTP engine running on port `1025` (For local email verification)

### 1️⃣ Backend Setup
1. **Clone and navigate to backend directory:**
   ```bash
   git clone <your-repository-url>
   cd HMS-Project/backend

2. **Create and activate a virtual environment:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 2️⃣ Frontend Setup
1. **Navigate to the frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Install Node modules:**
  ```bash
   npm install
  ```
3. **Run the Vite Development Server:**
   ```bash
   npm run dev
   ```

4. **Access the application:** Open `http://localhost:5173` in your browser.

---

## 🔒 Security Measures
*   **Stateless Authentication:** Passwords are mathematically hashed, and sessions are managed via JWTs stored in local storage.
*   **API Protection:** All protected backend routes enforce `@role_required` decorators to prevent unauthorized cross-role access (e.g., a patient cannot access admin endpoints).
*   **CORS Configuration:** Strictly configured to allow traffic only from the Vite dev server origin.

---

## 👨‍💻 Author
**24f3002399 Mukesh Ram**  
*BS in Data Science and Applications, IIT Madras*

---
