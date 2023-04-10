<template>
    <div class="row">
     <div class="col-md-6 offset-md-3" >
       <div>
         <div>
           <h3>Register User</h3>
         <hr/>
         </div>
         <form>
           <div class="form-group">
             <label for="">User Name</label>
             <input type="text" class="form-control" v-model="username">
           </div>
           <div class="form-group">
             <label for="">Password</label>
             <input type="Password" class="form-control" v-model="password" >
           </div>
           <div class="form-group">
             <label for="">First Name</label>
             <input type="text" class="form-control" v-model="first_name">
           </div>
           <div class="form-group">
             <label for="">Last Name</label>
             <input type="text" class="form-control" v-model="last_name">
           </div>
           <div class="my-3">
             <button type="submit" class="btn btn-primary" @click="SubmitUser()">Submit</button>
           </div>
         </form>
       </div>
     </div>
   
    </div>
   </template>
   
   <script>
 import axios from 'axios';

   export default {
     data(){
       return{
        username: "",
        password: "",
        first_name: "",
        last_name: "",
       }
     },
     methods:{
       getData(){
         if(this.email=="admin" && this.password=="pass"){
        this.$store.commit("setAuthentication", true)
        this.$router.replace({name:"home"})}
        else{
         alert("wrong password or username")
        }
       },
        async SubmitUser(){
        if(this.username == ''){
            alert("Please add user name")
        }else if(this.password == ''){
            alert("Please add password ")
        } else if(this.first_name == ''){
            alert("Please add first name")
        } else if(this.last_name == ''){
            alert("Please add last name")
        }else{
        const url = "http://192.168.1.29:8000/register"
          await axios.post(url,{
            username: this.username,
            password: this.password,
            first_name: this.first_name,
            last_name: this.last_name,
        }).then(res => {
            if(res){
                this.$router.push("/login");
        }
        }).catch(error => {
            alert(error.response.data.error)
        })
        }
       }
     }

   
   }
   </script>
   
  <style scoped>
 
 .form{
   padding: 40px;
 }
 </style>