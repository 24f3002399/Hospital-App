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
            <div class="col-auto me-auto"><h2>Registered Patient {{  }}</h2></div>
        </div>
        <table class="table table-bordered">
            <tbody>
                <tr v-for="patient in userData.pant_detail" :key="patient.name">
                    <td>{{ patient.name }}</td>
                    <td>
                        <div style="text-align: center;">
                            <RouterLink :to="'/doctordt/' + patient.user_id" >
                                <button class="btn btn-warning">View</button>
                            </RouterLink>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="row">
            <div class="col-auto me-auto"><h2>Upcoming Appointment</h2></div>
        </div> 
        <table class="table table-bordered">
            <tbody>
                <tr v-for="apt in Appointments">
                    <td>{{ apt.id }}</td>
                    <td><div class="row justify-content-evenly">
                            <div class="col-4"><RouterLink to="/register">
                                <button class="btn btn-primary">View</button>
                            </RouterLink></div>
                            <div class="col-4">
                            <RouterLink to="/register">
                                <button class="btn btn-primary">View</button>
                            </RouterLink></div>
                            <div class="col-4">
                            <RouterLink to="/register">
                                <button class="btn btn-primary">View</button>
                            </RouterLink></div>
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