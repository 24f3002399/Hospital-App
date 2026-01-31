<template>
    <form>
        <h1>Add a new Doctor</h1>
        <div v-if="error" style="text-align: center; color: red;">{{ error }}</div>
        <div class="mb-3">
            <label for="Input1" class="form-label">Email</label>
            <input type="email" class="form-control" id="Input1" v-model="formData.email">
        </div>
        <div class="mb-3">
            <label for="Input2" class="form-label">Password</label>
            <input type="password" class="form-control" id="Input2" v-model="formData.password">
        </div>
        <div class="mb-3">
            <label for="Input3" class="form-label">Fullname</label>
            <input type="text" class="form-control" id="Input3" v-model="formData.name">
        </div>
        <div class="mb-3">
            <label for="Input4" class="form-label">Departrment</label>
            <input type="text" class="form-control" id="Input4" v-model="formData.department" >
        </div>
        <div class="mb-3">
            <label for="Input5" class="form-label">Degree</label>
            <input type="text" class="form-control" id="Input5" v-model="formData.degree">
        </div>
        <div class="mb-3">
            <label for="Input6" class="form-label">Specialization</label>
            <input type="text" class="form-control" id="Input6" v-model="formData.specialty">
        </div>
        <div class="mb-3">
            <label for="Input7" class="form-label">Experience (in years)</label>
            <input type="number" class="form-control" id="Input7" v-model="formData.exp_year" >
        </div>
        <div style="text-align: center;">
            <button @click.prevent="addDoctor" class="btn btn-success">Add Doctor</button> <br>
        </div>
        <div style="text-align: center; padding: 10px;" >
            <button @click.prevent="$router.go(-1)" class="btn btn-info">Go Back</button>
        </div>

        <div v-if="mess" class="alert" :class="mess.includes('success') ? 'alert-success' : 'alert-danger'">
            {{ mess }}
        </div>
    </form>
</template>

<script>
import axios from 'axios';
export default {
    data(){
        return {
            formData: {
                email: "",
                password: "",
                name: "",
                department: "",
                exp_year: 0,
                degree: "",
                specialty: ""
            },
            mess: "",
            error: ""
        }
    },
    methods: {
        addDoctor: function() {
            const response = axios.post(`http://127.0.0.1:5000/api/add_doctor`, JSON.stringify(this.formData), {
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
    },
    watch: {
        error(newValue) {
        if (newValue) {
            setTimeout(() => {
            this.error = null;
            }, 10000);
        }
        }
    }
}
</script>