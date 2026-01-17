<script>
import axios from 'axios'
export default{
    data(){
        return {
            formData:{
                email: "",
                password: ""
            },
            token: "",
            error: "",
            role: ""
        }
    },
    methods:{
        LoginUser(event){
            event.preventDefault()
            const response = axios.post("http://127.0.0.1:5000/api/login", JSON.stringify(this.formData), {
                headers:{
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        })
        response
        .then(res => {
            this.token = res.data.access_token
            localStorage.setItem("token", res.data.access_token)  
            this.loadUser()
        }).catch(err => this.error =  err.response.data.message)
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
                   this.role = res.data.role;
                   if (this.role == "admin") {
                        this.$router.push('/admindash')
                    } 
                    else if (this.role == "doctor") {
                        this.$router.push('/doctordash')
                    }
                    else {
                        this.$router.push('/patientdash')
                    }
            }).catch(err => this.error = err.response.data.message)
        }
    }
}
</script>

<template>
    <div id="login"   >
        <h2 style="text-align: center; color:mediumvioletred; margin-bottom: 30px;" ><b>User Login</b></h2>
        <p class="err" v-if="error">{{ error }}</p>
        <form @submit="LoginUser">
        <div class="row mb-3">
            <label for="email" class="col-sm-4 col-form-label">Registered Email Id : </label>
            <div class="col-sm-6">
            <input type="email" class="form-control" id="email" v-model="formData.email">
            </div>
        </div>
        <div class="row mb-3">
            <label for="pass" class="col-sm-4 col-form-label" >Password : </label>
            <div class="col-sm-6">
            <input type="password" class="form-control" id="pass" v-model="formData.password">
            </div>
        </div>
        <div style="text-align: center;">
            <!-- <button @click="LoginUser" class="btn btn-primary">Login</button> -->
             <input type="submit" class="btn btn-info" value="Login">
        </div>
        <div style="text-align: center; padding: 10px;">
            <p style="margin-right: 14%;">New User  ?  
            <RouterLink to="/register">
                <button  class="btn btn-info" style="margin-left: 5px;">Register</button>
            </RouterLink></p></div>
        </form>
    </div>
</template>

<style scoped>
    #login{border: 2px solid black;
    width: 50%; height: 350px;
    margin: auto; margin-top: 150px;
    border-radius: 20px; padding: 10px; text-align: end;}

    #form-body{
        height: 337px;
    }
    .err{
        color: red;
        text-align: center;
    }
</style>