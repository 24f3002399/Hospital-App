<template>
    <div class="form">
    <form>
        <h1 style="text-align: center; color: darkolivegreen;">Edit</h1>
        <div v-if="error" style="text-align: center; color: red;">{{ error }}</div>
        <div class="mb-3">
            <label for="Input1" class="form-label">Fullname</label>
            <input type="text" class="form-control" id="Input1" v-model="formData.name">
        </div>
        <div class="mb-3">
            <label for="Input2" class="form-label">Departrment</label>
            <input type="text" class="form-control" id="Input2" v-model="formData.department" >
        </div>
        <div class="mb-3">
            <label for="Input3" class="form-label">Degree</label>
            <input type="text" class="form-control" id="Input3" v-model="formData.degree">
        </div>
        <div class="mb-3">
            <label for="Input4" class="form-label">Specialization</label>
            <input type="text" class="form-control" id="Input4" v-model="formData.specialty">
        </div>
        <div class="mb-3">
            <label for="Input5" class="form-label">Experience (in years)</label>
            <input type="number" class="form-control" id="Input5" v-model="formData.exp_year" >
        </div>
        <div style="text-align: center;">
            <button @click.prevent="Edit" class="btn btn-success">Update</button> <br>
        </div>
        <div style="text-align: center; padding: 10px;" >
            <button @click.prevent="$router.go(-1)" class="btn btn-info">Go Back</button>
        </div>

        <div v-if="message" class="alert" :class="message.includes('success') ? 'alert-success' : 'alert-danger'">
            {{ message }}
        </div>
    </form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    mounted() {
        if (this.$route.params.id) {
            this.doctorId = this.$route.params.id; 
        } 
    },
    data(){
        return {
            doctorId: null,
            formData: {
                name: "",
                department: "",
                exp_year: 0,
                degree: "",
                specialty: ""
            },
            message: "",
            error: ""
        }
    },
    methods: {
        Edit: function() {
            const response = axios.post(`http://127.0.0.1:5000/api/editdoct/${this.doctorId}`, JSON.stringify(this.formData), {
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
</style>