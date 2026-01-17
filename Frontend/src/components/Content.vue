<template>
    <div class="container-fluid forms">
        <div class="row align-items-center">
            <div class="col-8 content"></div>
            <div class="col-4 text-center">
                <div class="welcome"><h1>Welcome to <br><b>Hospital Management App</b></h1></div>
                <div class="m-3">
                    <button @click="this.$router.push('/login')" class="btn btn-outline-success">Login</button>
                </div>
                <div class="m-3">
                    <button @click="this.$router.push('/register')" class="btn btn-outline-success">Sign up</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .content{
        background-image: url("../assets/image.png");
        background-size: 100% 100%;
        height: 95vh;
        border-radius: 20px;
        border-bottom-right-radius: 0px;
        border-top-right-radius: 0px;
    }
    .forms{
        background-color:rgb(210, 231, 185);
        border: 3px solid black;
        width: 98%;
        margin-top: 10px;
        border-radius: 20px;
    }
    .btn {
        width: 80%;
    }
    .welcome {
        color:darkgreen;
        margin-bottom: 50px;
    }
</style>