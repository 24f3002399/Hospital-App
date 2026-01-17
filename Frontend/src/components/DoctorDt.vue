<script>
import axios from 'axios';
export default {
    mounted() {
        this.Detail()
    },
    data(){
        return {
            doctor_detail: "",
            message: "",
            specialist: {
                'Cardiology': 'Cardiologist',
                'Pediatrics': 'Pediatrician',
                'Gynecology': 'Gynecologist',
                'Orthopedics': 'Orthopedic Surgeon',
                'Dermatology': 'Dermatologist',
                'Neurology': 'Neurologist',
                'Ophthalmology': 'Ophthalmologist',
                'ENT': 'ENT Specialist',
                'Dentistry': 'Dentist',
                'General Medicine': 'General Physician'
            }
        }
    },
    computed:{
        d_speciality(){
            return this.specialist[this.doctor_detail.department] || this.doctor_detail.department
        }
    },
    methods: {
        Detail: function() {
            const response = axios.get(`http://127.0.0.1:5000/api/detail/${this.$route.params.id}`, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => { 
                    this.doctor_detail = res.data.doct_detail
                    this.message = res.data.message
            }).catch(err => this.error = err.response.data.message)

        },

    }
}
</script>

<template>
    <div class="detail">
        <div>                
            <h1>Dr. {{ doctor_detail.name }}</h1>
            <h3>{{ doctor_detail.degree }} , {{ doctor_detail.specialty }}</h3>
             <h4>{{ d_speciality }}</h4>
            <h5>{{ doctor_detail.exp_year }} Years Experience Overall</h5>
        </div>
        <div style="margin-top: 50px;">
            <h5>Dr. {{ doctor_detail.name }} is a dedicated {{ d_speciality }} 
                in India with overall {{ doctor_detail.exp_year }} years of experience. 
                Specializing in {{ doctor_detail.department }}, 
                he is committed to providing high-quality patient care and advanced medical treatments. 
                He focuses on a patient-centric approach, ensuring personalized diagnosis and effective recovery plans for every individual.</h5>
        </div>
        <div style="text-align: center; padding: 10px; margin-top: 20px;" >
            <button @click="$router.go(-1)" class="btn btn-info">Go Back</button>
        </div>
    </div>
</template>

<style>
    .detail{
        width: 60%;
        border: 2px solid black;
        border-radius: 20px;
        margin: auto;
        padding: 20px;
        border-style: outset;
        background-color: blanchedalmond;
    }
</style>