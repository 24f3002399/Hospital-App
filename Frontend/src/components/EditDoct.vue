<template>
    <form @submit.prevent="Edit">
        <h1>Edit</h1>
    
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
        <input type="submit" class="btn btn-success" value="Update"> <br></div>
        <div style="text-align: center; padding: 10px;" >
            <RouterLink to="/admindash">
                <button class="btn btn-secondary">Go Back</button>
            </RouterLink></div>
        <!-- <button @click="" class="btn btn-primary">Add</button> <br> -->

        <div v-if="message" class="alert" :class="message.includes('success') ? 'alert-success' : 'alert-danger'">
            {{ message }}
        </div>

    </form>
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
            message: ""
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
    }
}
</script>