<script>
export default {
    methods: {
        logoutUser(){
            localStorage.clear();
            this.$router.push('/')
        }
    }
}
</script>

<template>
    <nav class="navbar ">
        <div style="margin-left: 94%;">   
            <button @click="logoutUser" class="btn btn-danger">Logout</button>
        </div>
    </nav>
</template>