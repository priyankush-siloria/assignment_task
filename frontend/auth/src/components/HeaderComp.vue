<template>
<nav class="navbar navbar-expand-lg bg-light">
  <div class="container-fluid"> 
    <div class="collapse navbar-collapse d-flex justify-content-between" id="navbarNav">
      <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/home">Home</router-link>
          </li>
      </ul>
      <ul class="navbar-nav">
        <li class="nav-item" v-if="!isActive">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
        <li class="nav-item" v-if="isActive">
            <div class="nav-link" @click="logout()" >Logout</div>
          </li>
      </ul>
    </div>
  </div>
</nav>
</template>

<script>
import axios from 'axios'

export default {
    name:"HeaderComp",
    data(){
      return{
        isActive: false,
      }
    },
    methods:{
      async logout(){
        const url = "http://192.168.1.29:8000/logout"
        axios.defaults.headers.get['Authorization'] = 'Token '+localStorage.getItem('token');
          await axios.get(url,{
              username: this.username,
              password: this.password
            },
            ).then(res => {
              if(res){
                localStorage.removeItem('token')
                this.$router.push('/login')
              }
            }).catch(error => {
              alert(error.response.data.error)
            })
      }
    },
    
    mounted(){
      var token = localStorage.getItem('token');
      if(token != 'undefined'){
        this.isActive = true;
      }
      }


}
</script>

<style scoped>
.link{
    margin: 0px 10px;
    font-weight: bold;
    text-decoration: none;
}

</style>