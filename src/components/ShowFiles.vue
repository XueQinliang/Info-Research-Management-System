<template>
  <div v-theme:column="'wide'" id="show-files">
      <h1>文件总览</h1>
      <input type="text" v-model = "search" placeholder="搜索">
      <div v-for="(x,index) in filterblogs" :key="index" class="single-blog">
          <router-link v-bind:to="'/blog_detail/'+x.id">
            <h2 v-rainbow>{{x.title | to-uppercase}}</h2>
          </router-link>
          <article>
              {{x.body | snippet}}
          </article>
      </div>
  </div>
</template>

<script>
var fly = require('flyio')

export default {
  name: 'show-files',
  data(){
      return{
          files:[],
          search:""
      }
  },
//   beforeCreate(){
//       console.log("before")
//       fly.get('http://127.0.0.1:5000/islogin')
//       .then(function(response){
//           console.log(response)
//           if(response.data.LOGINSTATUS=='NOT'){
//               window.location.href = '/#/login'
//           }
//       })
//   },
  created(){
      //this.$emit('header',true)
      this.$http.get("https://jsonplaceholder.typicode.com/posts")
      .then(function(data){
          //console.log(data);
          this.files = data.body.slice(0,10);
      })
  },
  computed:{
      filterblogs:function(){
          return this.files.filter((x) =>{
              return x.title.match(this.search)
          })
      }
  },
  filters:{
      "to-uppercase":function(value){
          return value.toUpperCase();
      }
  },
  directives:{
      'rainbow':{
          bind(el,binding,vnode){
              el.style.color = "red";
          }
      }
  }
}
</script>

<style scoped>
#show-files{
    max-width: 800px;
    margin:0 auto;
}

.single-blog{
    padding:20px;
    margin: 20px 0;
    background: #eee;
    border:1px dotted #aaa;
}

#show-files a{
    color:#444;
    text-decoration: none;
}

input[type="text"]{
    padding: 8px;
    width:100%;
    box-sizing: border-box;
}
</style>
