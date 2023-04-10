<template>
  <div>
    <div class="allpost-btn">
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal" >Add post</button>
    </div>
    

    <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title postAdd" id="exampleModalLabel">Add Post</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <form>
          <div class="form-group">
            <label for="">Title</label>
            <input type="text" class="form-control" v-model="title">
          </div>
          <div class="form-group">
            <label for="">Description</label>
            <input type="text" class="form-control" v-model="body" >
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" @click="addPost()" data-dismiss="modal">Save</button>
      </div>
    </div>
  </div>
    </div>
    

    <div class="modal fade" id="exampleEditModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title postAdd" id="exampleModalLabel">Edit Post</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <form>
          <div class="form-group">
            <label for="">Title</label>
            <input type="text" class="form-control" v-model="title">
          </div>
          <div class="form-group">
            <label for="">Description</label>
            <input type="text" class="form-control" v-model="body" >
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" @click="updatePost()" data-dismiss="modal">Save</button>
      </div>
    </div>
  </div>
    </div>

  <table id="example" class="table table-striped" style="width:100%">
      <thead>
          <tr>
              <th>Title</th>
              <th>Body</th>
              <th>Action</th>
          </tr>

      </thead>
      <tbody>
          <tr v-for="element in this.postListing">
              <td>{{element.title}}</td>
              <td>{{element.body}}</td>
              <td>
                <div>
                  <button class="edit-btn" @click="editPost(element.id)" data-toggle="modal" data-target="#exampleEditModal">Edit</button>
                  <button class="edit-btn" @click="deletePost(element.id)">Delete</button>
                </div>
              </td>

            </tr>
      </tbody>
  </table>

  </div>

</template>

<script>

import axios from 'axios';

export default {
    name:"home",
    data(){
      return{
       postListing: [],
       title: '',
       body: '',
    }
    },
    methods:{
      async addPost(){
        if(this.title =='') {
          alert("Please add Title ")
        } else if(this.body == '') {
          alert("Please add Body")          
        }
        else {
        const url = "http://192.168.1.29:8000/post";
        axios.defaults.headers.post['Authorization'] = 'Token '+localStorage.getItem('token');
            await axios.post(url,{
                title: this.title,
                body: this.body,
                user: localStorage.getItem('user'),
                is_active: true,
            }).then(res => {
                if(res){
                  this.getPosts();
                  this.title = "";
                  this.body = "";
              }
            }).catch(error => {
              if(error){
              alert(error.response.data.error)
              }
            })
          }
     

      },

      async getPosts(){
      const url = "http://192.168.1.29:8000/post"
      axios.defaults.headers.get['Authorization'] = 'Token '+localStorage.getItem('token');
          await axios.get(url,{
                title: this.title,
                body: this.body,
                user: localStorage.getItem('user'),
                is_active: true,
          }).then(res => {
              if(res){
                this.postListing = res.data.data
              }
            }).catch(error => {
              if(error){
              alert(error.response.data.error)
              }
            })
      },
      async updatePost(){
      const url = "http://192.168.1.29:8000/post/"+this.updateId;
      axios.defaults.headers.put['Authorization'] = 'Token '+localStorage.getItem('token');
          await axios.put(url,{
            title: this.title,
            body: this.body,
            user: localStorage.getItem('user'),
            is_active: true,
          }).then(res => {
              if(res){
                this.postListing = res.data.data
                this.title = "";
                this.body = "";
                alert("Data Updated")
                location.reload();
              }
            }).catch(error => {
              if(error){
              alert(error.response.data.error)
              }
            })
      },
      async editPost(id){
        const url = "http://192.168.1.29:8000/post/"+id
        axios.defaults.headers.put['Authorization'] = 'Token '+localStorage.getItem('token');
          var res = await axios.put(url)
          if(res){
            this.title = res.data.data.title;
            this.body= res.data.data.body;
            this.updateId = id;
          }
          // .then(res => {
          //     if(res){
          //       this.postListing = res.data.data
          //       this.title = res.data.data.title;
          //       this.body= res.data.data.body;
          //     }
          //   }).catch(error => {
          //     if(error){
          //     alert(error.response.data.error)
          //     }
          //   })

      },
      async deletePost(id){
        const url = "http://192.168.1.29:8000/post/"+id
        axios.defaults.headers.delete['Authorization'] = 'Token '+localStorage.getItem('token');
          await axios.delete(url).then(res => {
              if(res){
                alert("Post deleted Successfully")
                location.reload();
              }
            }).catch(error => {
              if(error){
              alert(error.response.data.error)
              }
            })
      }
    },
    mounted(){
      this.getPosts();
    },
    



}
</script>

<style>
.edit-btn {
    padding: 2px 13px;
    background-color: #196dc4;
    margin: 0 4px;
    border: none;
    border-radius: 3px;
    font-size: 14px;
    font-weight: 400;
    color: #fff;
}
.postAdd{

}
</style>