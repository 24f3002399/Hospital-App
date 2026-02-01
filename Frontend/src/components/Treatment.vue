<template>
    <div>
    <form class="form">
        <div class="head">
        <h1 style="color:darkslategrey">Treatment</h1>
        <h4>Patient Name : {{ this.patient_name }}</h4>
        <h4>Department : {{ this.department }}</h4>
        </div>
        <div class="mb-3">
            <label for="Input1" class="form-label">Visit Type</label>
            <select v-model="formData.visit_type" class="form-select" required id="Input1">
                <option value="" disabled selected>Select Visit Type</option>
                <option value="In-person">In-person</option>
                <option value="Online">Online (Tele-consultation)</option>
            </select>
        </div>
        <div class="mb-3">
            <label for="Input2" class="form-label">Test Done</label>
            <input type="text" class="form-control" id="Input2" v-model="formData.test_done">
        </div>
        <div class="mb-3">
            <label for="Input3" class="form-label">Diagnosis</label>
            <input type="text" class="form-control" id="Input3" v-model="formData.diagnosis">
        </div>
        <div class="mb-3">
            <label for="Input4" class="form-label">Prescription</label>
            <input type="text" class="form-control" id="Input4" v-model="formData.prescription" >
        </div>
        <div class="mb-3">
            <label for="Input5" class="form-label">Medicines</label>
            <input type="text" class="form-control" id="Input5" v-model="formData.medicines">
        </div>
        <div class="mb-3">
            <label for="Input6" class="form-label">Notes</label>
            <input type="text" class="form-control" id="Input6" v-model="formData.notes">
        </div>
        <div style="text-align: center;">
            <button @click.prevent="Treatment" class="btn btn-success">Mark as Complete</button> <br>
        </div>
        <div style="text-align: center; padding: 10px;" >
            <button @click.prevent="$router.go(-1)" class="btn btn-info">Go Back</button>
        </div>

        <div v-if="mess" class="alert" :class="mess.includes('success') ? 'alert-success' : 'alert-danger'">
            {{ mess }}
        </div>
    </form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data(){
        return {
            formData: {
                visit_type: "",
                test_done: "",
                diagnosis: "",
                prescription: "",
                medicines: "",
                notes: ""
            },
            mess: "",
            patient_name: "",
            department: ""
        }
    },
    mounted(){
        this.Apnt_dt()
    },
    methods: {
        Apnt_dt: function(){
            const response = axios.get(`http://127.0.0.1:5000/api/apnt_dt/${this.$route.params.id}`, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.patient_name = res.data.patient_name
                    this.department = res.data.department
            }).catch(err => this.error = err.response.data.message)
        },
        Treatment: function() {
            const response = axios.post(`http://127.0.0.1:5000/api/treatment/${this.$route.params.id}`, JSON.stringify(this.formData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.mess = res.data.message
            }).catch(err => this.error = err.response.data.message)

        }
    }
}
</script>

<style scoped>
    .form{
        width: 60%;
        margin: auto;
        border: 2px solid green;
        border-radius: 10px;
        padding-left: 30px;
        padding-right: 30px;
        padding-top: 10px;
    }
    .head{
        text-align: center;
        color:darkred;
    }
</style>