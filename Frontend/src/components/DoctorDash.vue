<script>
import axios from 'axios';

export default {
    data(){
        return {
            token: "",
            userData: "" ,
            doctorId: null,
        }
    },
    mounted(){
        this.loadToken()
        this.loadUser()
    },
    methods: {
        Provide_av: function(){
            const response = axios.get(`http://127.0.0.1:5000/api/provide_av/${this.doctorId}`, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${this.token}` 
                }
            })
            response
            .then(res => {
                   this.$router.push(`/availability/${this.doctorId}`)
            }).catch(err => this.error = err.response.data.message)
        },
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
                   this.doctorId = res.data.doctor_id
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
        }
    },
    computed: {
        Appointments(){
            if (!this.userData.apnt_detail) {
                    return []; 
                }

            return this.userData.apnt_detail.filter(apnt => {
                return new Date(apnt.date) >= new Date().setHours(0,0,0,0)             
            })
        }
    }
}
</script>

<template>
    <div v-if="token" class="dash">
        <h1>Doctor {{ userData.user_name }}</h1>
        <div class="row">
            <div class="col-auto me-auto"><h2>Assigned Patients </h2></div>
        </div>
        <table class="table table-bordered">
            <tbody>
                <tr v-for="patient in userData.pant_detail" :key="patient.name">
                    <td>{{ patient.name }}</td>
                    <td>
                        <div style="text-align: center;">
                            <RouterLink :to="'/patientdt/' + patient.user_id" >
                                <button class="btn btn-warning">View</button>
                            </RouterLink>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="row">
            <div class="col-auto me-auto"><h2>Upcoming Appointments</h2></div>
        </div> 
        <table class="table table-bordered" style="text-align: center;">
            <thead>
                <tr>
                        <th>ID</th>
                        <th>Patient Name</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Action</th>
                    </tr>
            </thead>
            <tbody>
                <tr v-for="apt in Appointments">
                    <td>{{ apt.id }}</td>
                    <td>{{ apt.pt_name }}</td>
                    <td>{{ apt.date.split(' ').slice(1, 4).join(' ')}}</td>
                    <td>{{ apt.time }}</td>
                    <td><div class="row justify-content-evenly">
                            <div class="col-4">
                                <RouterLink :to="'/treatment/' + apt.id">
                                    <button class="btn btn-info">Mark as complete</button>
                                </RouterLink>
                            </div>
                            <div class="col-4">
                                <button @click="Ask_cancel(apt.id)" class="btn btn-danger">Cancel</button>
                            </div>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
        <div style="text-align: center;">
            <button @click="Provide_av" class="btn btn-success">Provide Availability</button> 
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