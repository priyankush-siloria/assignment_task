<template>
   <div class="row">
    <div class="col-md-6 offset-md-3" >
      <div>
        <div>
          <h3>Login Page</h3>
        <hr/>
        </div>
        <form>
          <div class="form-group">
            <label for="">Email</label>
            <input type="text" class="form-control" v-model="username">
          </div>
          <div class="form-group">
            <label for="">Password</label>
            <input type="Password" class="form-control" v-model="password" >
          </div>
          <div class="my-3">
            <button type="submit" class="btn btn-primary" :disabled="!username && !password" @click.prevent="login()">Login</button>
            <button type="submit" class="btn btn-secondary m-2" @click.prevent="registerUser()">Register</button>
          </div>
        </form>
      </div>
    </div>
  
   </div>
  </template>
  
  <script>

import axios from 'axios';
  export default {
    name: "Login",
    data(){
      return{
        username:"",
        password:""
      }
    },
    methods:{
      async login(){
        if(this.username && this.password){
          const url = "http://192.168.1.29:8000/login"
          await axios.post(url,{
              username: this.username,
              password: this.password
            }).then(res => {
              if(res){
                localStorage.setItem('token',res.data.token)
                localStorage.setItem('user',res.data.user)
                this.$router.push('/home')
              }
            }).catch(error => {
              alert(error.response.data.error)
            })
        }
      },
      registerUser(){
        this.$router.replace({name:"registerUser"})
      }
    }
   
  
  }
  </script>
  
 <style scoped>

.form{
  padding: 40px;
}
</style>