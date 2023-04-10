import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../components/Login.vue";
import Home from '../components/Home.vue'
import RegisterUser from "../components/RegisterUser.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/registerUser",
    name: "registerUser",
    component: RegisterUser,
  },
  {
    path: "/",
    redirect:{
    name: "login",}
   
  },
  {
    path:"/login",
    name: "login",
    component:Login
  },
  {
    path:"/home",
    name:"home",
    component:Home,
  //  beforeEnter:(to,from,next)=>{
  //   if(store.state.authenticated == false){
  //     next(false)
  //   } else{
  //     next()
  //   }
  //  }
  }
];

const router = new VueRouter({
  routes,
});



export default router;
