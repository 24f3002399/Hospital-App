<script>
import axios from 'axios';
export default {
    mounted() {
        this.Detail()
    },
    data(){
        return {
            treatment: "",
            appointment: "",
            patient_detail: "",
            message: "",
            search_by: "completed"
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
                    this.patient_detail = res.data.pant_detail
                    this.message = res.data.message
                    this.treatment = res.data.treatment
                    this.appointment = res.data.appointment
            }).catch(err => this.error = err.response.data.message)

        },

    }
}
</script>

<template>
    <div class="detail">
        <h1 style="text-align: center; color:darkred;"><b>Patient History</b></h1>
        <div class="row" style="margin-top: 40px; margin-bottom: 20px;">
            <div class="col-auto me-auto"><h3>Patient Name : {{ patient_detail.name }}</h3></div>
            <div class="col-auto">
                <select style="width: 300px; border-radius: 10px; margin-right: 10px;" v-model="search_by" >
                    <option value="completed">Completed Appointments</option> 
                    <option value="cancelled">Cancelled Appointments</option>
                </select>
            </div>
        </div>
        <div >  
            <div v-if="search_by == 'completed'">
                <table class="table table-bordered table-secondary" style="text-align: center; ">
                    <thead>
                        <tr>
                            <th>Sr. No</th>
                            <th>Doctor Name</th>
                            <th>Department</th>
                            <th>Visit Type</th>
                            <th>Test Done</th>
                            <th>Diagnosis</th>
                            <th>Prescription</th>
                            <th>Medicines</th>
                            <th>Doctor Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(treat, index) in treatment">
                            <td>{{ index + 1}}</td>
                            <td>{{ treat.doctor }}</td>
                            <td>{{ treat.department }}</td>
                            <td>{{ treat.visit_type }}</td>
                            <td>{{ treat.test_done }}</td>
                            <td>{{ treat.diagnosis }}</td>
                            <td>{{ treat.prescription }}</td>
                            <td>{{ treat.medicines }}</td>
                            <td>{{ treat.notes }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <table class="table table-bordered table-secondary" style="text-align: center; ">
                    <thead>
                        <tr>
                            <th>Sr. No.</th>
                            <th>Doctor Name</th>
                            <th>Department</th>
                            <th>Date</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(apnt , index) in appointment">
                            <td>{{ index + 1 }}</td>
                            <td>{{ apnt.doct_name }}</td>
                            <td>{{ apnt.dept_name }}</td>
                            <td>{{ apnt.date.split(' ').slice(1, 4).join(' ') }}</td>
                            <td>{{ apnt.time }}</td>
                        </tr>
                    </tbody> 
                </table>
            </div>
        </div>
        <div style="text-align: center; margin-top: 10px;">
            <button @click="$router.go(-1)" class="btn btn-info">Go Back</button>
        </div>
    </div>
</template>

<style scoped>
    .detail{
        width: 95%;
        border: 2px solid black;
        border-radius: 20px;
        margin: auto; 
        padding: 20px; 
        background-color: blanchedalmond;
    }
</style>