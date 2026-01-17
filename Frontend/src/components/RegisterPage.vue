<script>
import axios from 'axios'
export default{
    data(){
        return {
            formData:{
                email: "",
                password: "",
                name: "",
            },
            message: "",
            error: ""
        }
    },
    methods:{
        RegisUser(event){
            event.preventDefault()
            const response = axios.post("http://127.0.0.1:5000/api/register", JSON.stringify(this.formData), {
                headers:{
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        })
        response
        .then(res => {
            this.message = res.data.message
            setTimeout(() => {
                this.$router.push('/login');
                }, 5000);
        }).catch(err => this.error =  err.response.data.message)
        }
    }
}
</script>

<template>
    <div id="regis"   >
        <h2 style="text-align: center; color:darkorange; margin-bottom: 30px; margin-left: 45px;">New Registration</h2>
        <p class="err" v-if="error">{{ error }}</p>
        <form @submit="RegisUser">
        <div class="row mb-3">
            <label for="name" class="col-sm-4 col-form-label">Name : </label>
            <div class="col-sm-6">
            <input type="text" class="form-control" id="name" v-model="formData.name">
            </div>
        </div>    
        <div class="row mb-3">
            <label for="email" class="col-sm-4 col-form-label">Email Id : </label>
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
             <input type="submit" class="btn btn-info" value="Register">
             <div style="text-align: center; padding: 10px;">
                <p style="margin-right: 26%;">Already have account ?  <RouterLink to="/login">
                <button  class="btn btn-info">Login</button>
            </RouterLink></p></div>
        </div>
        <div v-if="message" class="alert" >
            {{ message }}
        </div>
        </form>
    </div>
</template>

<style scoped>
    #regis{border: 2px solid black;
    width: 50%; height: 400px;
    margin: auto; margin-top: 120px;
    border-radius: 20px; padding: 10px; text-align: end;}

    #form-body{
        height: 337px;
    }
    .err{
        color: red;
        text-align: center;
    }
    .alert {
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        border-radius: 4px;
        text-align: center;
    }
</style>