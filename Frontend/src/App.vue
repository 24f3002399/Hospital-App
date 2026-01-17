<script >
import NavPage from './components/NavPage.vue'
import FootPage from './components/FootPage.vue'

export default{
  data(){
        return {
            token: ""
        }
  },
  components:{
    NavPage,
    FootPage
  },
  watch: {
    '$route': function() {
      this.token = localStorage.getItem('token');
    }
  }
}
</script>

<template>
  <div v-if="token">
    <NavPage />
    <RouterView />
    <FootPage />
  </div>
  <div v-else>
    <RouterView />
  </div>
</template>

<style scoped>
  
</style>
