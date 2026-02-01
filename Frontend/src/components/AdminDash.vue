<script>
import axios from 'axios';

export default {
    data(){
        return {
            token: "",
            userData: "" ,
            search_doc_by: "",
            search_doc_for: "",
            search_pat_by: "",
            search_pat_for: "",
            search_apt_by: "upcoming",
            message: ""
        }
    },
    mounted(){
        this.loadToken()
        this.loadUser()
    },
    methods: {
        loadToken: function (){
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
        },
        loadUser: function() {
            const response = axios.get("http://127.0.0.1:5000/api/dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${this.token}` 
                }
            })
            response
            .then(res => {
                   this.userData = res.data;
            }).catch(err => this.error = err.response.data.message)
        },
        Block: function(b_id) {
            const response = axios.post(`http://127.0.0.1:5000/api/block/${b_id}`, JSON.stringify(this.formData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.message = res.data.message
                    this.loadUser()
            }).catch(err => this.error = err.response.data.message)
        },
        Unblock: function(u_id) {
            const response = axios.post(`http://127.0.0.1:5000/api/unblock/${u_id}`, JSON.stringify(this.formData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.message = res.data.message
                    this.loadUser()
            }).catch(err => this.error = err.response.data.message)
        },
        Delete: function(d_id) {
            const response = axios.post(`http://127.0.0.1:5000/api/delete/${d_id}`, JSON.stringify(this.formData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.message = res.data.message
                    alert("Deleted successfully")
                    this.loadUser()
            }).catch(err => this.error = err.response.data.message)
        },
        Ask_delete: function(a_id) {
            const result = confirm("Are you want to delete");
            if (result) {
                this.Delete(a_id)                
            } else {
                console.log("Denied")
            }
        },
        Cancel: function(c_id) {
            const response = axios.post(`http://127.0.0.1:5000/api/cancel/${c_id}`, {}, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.message = res.data.message
                    alert("Cancel successfully")
                    this.loadUser()
            }).catch(err => this.error = err.response.data.message)
        },
        Ask_cancel: function(c_id) {
            const result = confirm("Are you want to cancel this appointment");
            if (result) {
                this.Cancel(c_id)                
            } else {
                console.log("Denied")
            }
        },
        Cache_clear: function() {
            const response = axios.post(`http://127.0.0.1:5000/api/clear-cache`, {}, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    alert("Cache cleared successfully")
            }).catch(err => this.error = err.response.data.message)
        },
        Ask_cache_clear: function() {
            const result = confirm("Are you want to clear the cache");
            if (result) {
                this.Cache_clear()                
            } else {
                console.log("Denied")
            }
        },
    },
    computed: {
        doctors(){
            if (!this.userData.doct_detail) {
                    return []; 
                }

            return this.userData.doct_detail.filter(doctor => {
                if (this.search_doc_by === "doctor") {
                    return doctor.name.toLowerCase().includes(this.search_doc_for.toLowerCase())                   
                }
                else if (this.search_doc_by === "department") {
                    return doctor.department.toLowerCase().includes(this.search_doc_for.toLowerCase()) 
                }
                return true
            })
        },
        Patients(){

            if (!this.userData.pant_detail) {
                    return []; 
                }

            return this.userData.pant_detail.filter(patient => {
                if (this.search_pat_by === "id") {
                    return patient.id == this.search_pat_for                
                }
                else if (this.search_pat_by === "patient") {
                    return patient.name.toLowerCase().includes(this.search_pat_for.toLowerCase()) 
                }
                return true
            })
        },
        Appointments(){

            if (!this.userData.apnt_detail) {
                    return []; 
                }

            return this.userData.apnt_detail.filter(apnt => {
                if (this.search_apt_by === "upcoming") {
                    return apnt.status == "booked"  && new Date(apnt.date) >= new Date().setHours(0,0,0,0)                
                }
                else {
                    return apnt.status !== "booked" 
                }
            })
        },
    }
}
</script> 

<template>
    <div v-if="token">
        <div class="dash">
            <div style="display: flex;margin-bottom: 20px;" class="row">
                <div class="col-auto me-auto"><h3 style="color:darkorange; display: inline;"><b>Welcome {{ userData.user_name }}</b></h3></div>
                <div class="col-auto"><button @click="Ask_cache_clear" class="btn btn-outline-warning">Clear the Cache</button> </div>
            </div>
            <div class="row">
                <div class="col-auto me-auto"><h2>Registered Doctor ( {{ doctors.length }} )</h2></div>
                <div class="col-auto">
                    <select style="width: 130px; border-radius: 10px; margin-right: 3px;" v-model="search_doc_by">
                        <option value="">Search by</option>
                        <option value="doctor">Doctor name</option> 
                        <option value="department">Department name</option>
                    </select>
                    <input type="text" style="border-radius: 10px" v-model="search_doc_for" :placeholder="`search ${this.search_doc_by}...`">
                </div>
                <div class="col-auto">
                    <RouterLink to="/addDoctor">
                        <button class="btn btn-success">Add Doctor</button> 
                    </RouterLink>
                </div>
            </div>
            <div class="table-container" style="max-height: 200px; overflow-y: auto;">
                <table class="table table-bordered " style="text-align: center;">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Department</th>
                            <th>Action</th>
                            <th>Availability</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="doctor in doctors" :key="doctor.user_id">
                            <td>{{ doctor.id }}</td>
                            <td>{{ doctor.name }}</td>
                            <td>{{ doctor.department }}</td>
                            <td><div class="row justify-content-evenly">
                                    <div class="col-4"><RouterLink :to="'/editdoct/' + doctor.user_id">
                                        <button class="btn btn-info">Edit</button>
                                    </RouterLink></div>
                                    <div class="col-4">
                                        <button @click="Ask_delete(doctor.user_id)" class="btn btn-danger">Delete</button>
                                    </div>
                                    <div class="col-4">
                                    <div v-if="doctor.status == 'active'">
                                        <button @click="Block(doctor.user_id)" class="btn btn-dark">Block</button>
                                    </div>
                                    <div v-else>
                                        <button @click="Unblock(doctor.user_id)" class="btn btn-success">Unblock</button>
                                    </div></div>
                                </div>
                            </td>
                            <td>
                                <RouterLink :to="'/adminchangeav/' + doctor.id" >
                                    <button class="btn btn-outline-primary">Update</button>
                                </RouterLink>
                            </td>
                            <td>
                                <RouterLink :to="'/doctordt/' + doctor.user_id" >
                                    <button class="btn btn-warning">View</button>
                                </RouterLink>
                            </td>
                            
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="row" style="margin-top: 40px;">
                <div class="col-auto me-auto"><h2>Registered Patient ( {{ Patients.length }} )</h2></div>
                <div class="col-auto">
                    <select style="width: 130px; border-radius: 10px; margin-right: 3px;" v-model="search_pat_by">
                        <option value="">Search by</option>
                        <option value="id">Patient Id</option> 
                        <option value="patient">Patient name</option>
                    </select>
                    <input type="text" style="border-radius: 10px" v-model="search_pat_for" :placeholder="`search ${this.search_pat_by}...`">
                </div>
            </div>
            <div class="table-container" style="max-height: 200px; overflow-y: auto;">
                <table class="table table-bordered" style="text-align: center;">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Action</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="patient in Patients" :key="patient.name">
                            <td>{{ patient.id }}</td>
                            <td>{{ patient.name }}</td>
                            <td><div class="row justify-content-evenly">
                                    <div class="col-4">
                                        <RouterLink :to="'/editpat/' + patient.id">
                                        <button class="btn btn-info">Edit</button>
                                        </RouterLink>
                                    </div>
                                    <div class="col-4">
                                        <button @click="Ask_delete(patient.user_id)" class="btn btn-danger">Delete</button>
                                    </div>
                                    <div class="col-4">
                                    <div v-if="patient.status == 'active'">
                                        <button @click="Block(patient.user_id)" class="btn btn-dark">Block</button>
                                    </div>
                                    <div v-else>
                                        <button @click="Unblock(patient.user_id)" class="btn btn-success">Unblock</button>
                                    </div></div>
                                </div>
                            </td>
                            <td>
                                <RouterLink :to="'/patientdt/' + patient.user_id" >
                                    <button class="btn btn-warning">View</button>
                                </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="row" style="margin-top: 40px;">
                <div class="col-auto me-auto"><h2>Appointments ( {{ Appointments.length }} )</h2></div>
                <div class="col-auto">
                    <select style="width: 300px; border-radius: 10px; margin-right: 50px;" v-model="search_apt_by" >
                        <option value="upcoming">Upcoming Appointment</option> 
                        <option value="past">Past Appointment</option>
                    </select>
                </div>
            </div>
            <div class="table-container" style="max-height: 200px; overflow-y: auto;">
                <table class="table table-bordered" style="text-align: center;">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Patient Name</th>
                            <th>Doctor Name</th>
                            <th>Department</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="apt in Appointments" :key="apt.name">
                            <td>{{ apt.id }}</td>
                            <td>{{ apt.pt_name }}</td>
                            <td>{{ apt.doct_name }}</td>
                            <td>{{ apt.dept_name }}</td>
                            <td>{{ apt.date.split(' ').slice(1, 4).join(' ') }}</td>
                            <td>{{ apt.time }}</td>
                            <td>
                                <div v-if="apt.status == 'booked'">
                                    <button @click="Ask_cancel(apt.id)" class="btn btn-danger">Cancel</button>
                                </div>
                                <div v-else>
                                    <button class="btn btn-secondary" disabled>{{ apt.status }}</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div v-else>
        <h1>Please Login</h1>        
    </div>
</template>

<style scoped>
    .dash{
        margin-left: 20px;
        margin-right: 20px;
    }
</style>