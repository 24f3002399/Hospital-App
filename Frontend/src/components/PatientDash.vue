<script>
import axios from 'axios';

export default {
    data(){
        return {
            token: "",
            userData: "" ,
            message: "",
            search_dept_for: "",
            search_apt_by: "upcoming"
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
        Reschedule: function(a_id) {
            const response = axios.post(`http://127.0.0.1:5000/api/reschedule/${a_id}`, {}, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.message = res.data.message
            }).catch(err => this.error = err.response.data.message)
        },
        Ask_res: function(a_id, d_id) {
            const result = confirm("Are you want to reschedule this appointment");
            if (result) {
                this.Reschedule(a_id)
                this.$router.push('/book/' + d_id)

            } else {
                console.log("Denied")
            }
        }
    },
    computed: {
        department(){
            if (!this.userData.dept_detail) {
                    return []; 
                }

            return this.userData.dept_detail.filter(depart => {
                return depart.name.toLowerCase().includes(this.search_dept_for.toLowerCase())                   
            })
        },
        Appointments(){

            if (!this.userData.apnt_detail) {
                    return []; 
                }

            return this.userData.apnt_detail.filter(apnt => {
                if (this.search_apt_by === "upcoming") {
                    return apnt.status == "booked" && new Date(apnt.date) >= new Date().setHours(0,0,0,0)             
                }
                else {
                    return apnt.status !== "booked" 
                }
            })
        }
    }
}
</script>

<template>
    <div v-if="token">
        <div class="dash">
            <div style="margin-bottom: 20px;" class="row">
                <div class="col-auto me-auto"><h3 style="color:darkorange; display: inline;"><b>Welcome {{ userData.user_name }}</b></h3></div>
                <div class="col-auto" style="float: left;">
                    <RouterLink :to="'/editpat/' + userData.patient_id">
                    <button class="btn btn-outline-success">Edit Profile</button>
                    </RouterLink>
                </div>
                <div class="col-auto">
                    <RouterLink :to="'/patientdt/' + userData.user_id" >
                        <button class="btn btn-outline-success">History</button>
                    </RouterLink>
                </div>
            </div>
            <div class="row">
                <div class="col-auto me-auto"><h2>Departments</h2></div>
                <div class="col-auto">
                    <input type="text" style="border-radius: 10px" v-model="search_dept_for" :placeholder="`search department...`">
                </div>
            </div>
            <table class="table table-bordered" style="text-align: center;">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="depart in department">
                        <td>{{ depart.name }}</td>
                        <td><div class="row justify-content-evenly">
                                <div class="col-4">
                                    <RouterLink :to="'/department/' + depart.name">
                                        <button class="btn btn-info">View Details</button>
                                    </RouterLink>
                                </div>                              
                            </div>
                        </td>                       
                    </tr>
                </tbody>
            </table>
            <div class="row">
                <div class="col-auto me-auto"><h2>Appointment</h2></div>
                <div class="col-auto">
                    <select style="width: 300px; border-radius: 10px; margin-right: 5px;" v-model="search_apt_by" >
                        <option value="upcoming">Upcoming Appointment</option> 
                        <option value="past">Past Appointment</option>
                    </select>
                </div>
            </div>
            
            <table class="table table-bordered" style="text-align: center;">
                <thead>
                    <tr>
                        <th>Sr. No.</th>
                        <th>Doctor Name</th>
                        <th>Department</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(apt, index) in Appointments">
                        <td>{{ index + 1 }}</td>
                        <td>{{ apt.doct_name }}</td>
                        <td>{{ apt.dept_name }}</td>
                        <td>{{ apt.date.split(' ').slice(1, 4).join(' ') }}</td>
                        <td>{{ apt.time }}</td>
                        <td>
                            <div class="row justify-content-evenly" v-if="apt.status == 'booked' && search_apt_by == 'upcoming'">
                                <div class="col-4"><button @click="Ask_res(apt.id, apt.doct_id)" class="btn btn-warning">Reschedule</button></div>
                                <div class="col-4"><button @click="Ask_cancel(apt.id)" class="btn btn-danger">Cancel</button></div>
                            </div>
                            <div class="justify-content-evenly" v-else>
                                <button class="btn btn-secondary" disabled>{{ apt.status }}</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
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