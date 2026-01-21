<template>
    <form >
        <h1>Edit</h1>
    
        <div class="mb-3">
            <label for="Input3" class="form-label">Fullname</label>
            <input type="text" class="form-control" id="Input3" v-model="formData.name">
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
        if (this.$route.params.id) {
            this.patId = this.$route.params.id
        } 
    },
    data(){
        return {
            patId: null,
            formData: {
                name: "",
            },
            message: ""
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

        }
    }
}
</script>