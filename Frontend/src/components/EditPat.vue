<template>
    <form >
        <h1>Edit</h1>
        <div v-if="error" style="text-align: center; color: red;">{{ error }}</div>
        <div class="mb-3">
            <label for="Input1" class="form-label">Fullname</label>
            <input type="text" class="form-control" id="Input1" v-model="formData.name">
        </div>
        <div v-if="role == 'patient'" class="mb-3">
            <label for="Input2" class="form-label">Change Password</label>
            <input type="password" class="form-control" id="Input2" v-model="formData.password">
        </div>
        <div style="text-align: center;">
            <button @click.prevent="Edit" class="btn btn-info">Update</button><br>
        </div>
        <div style="text-align: center; padding: 10px;" >
            <button @click.prevent="$router.go(-1)" class="btn btn-secondary">Go Back</button>
        </div>

        <div v-if="message" class="alert" :class="message.includes('success') ? 'alert-success' : 'alert-danger'">
            {{ message }}
        </div>

    </form>
</template>

<script>
import axios from 'axios';
export default {
    mounted() {
        this.loadUser();
        if (this.$route.params.id) {
            this.patId = this.$route.params.id
        } 
    },
    data(){
        return {
            patId: null,
            formData: {
                name: "",
                password: ""
            },
            message: "",
            error: "",
            role: ""
        }
    },
    methods: {
        Edit: function() {
            const response = axios.post(`http://127.0.0.1:5000/api/editpat/${this.patId}`, JSON.stringify(this.formData), {
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
        loadUser: function() {
            const response = axios.get("http://127.0.0.1:5000/api/dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}` 
                }
            })
            response
            .then(res => {
                   this.role = res.data.role
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