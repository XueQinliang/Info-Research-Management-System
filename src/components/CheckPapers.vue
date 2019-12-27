<template>
  <div v-theme:column="'wide'" id="show-files">
      <h1>我的论文</h1>
      <div v-for="(paper,index) in papers" :key="index" class="single-blog">
          <router-link v-bind:to="'/paper_detail/'+paper.title+'/'+paper.author">
            <h2 v-rainbow>{{paper.title}}</h2>
          </router-link>
          <article>
              <b class="author">作者：{{paper.author}} </b>
              <b class="seq">作者序：{{paper.sequence}}</b>
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
          papers:[

          ],
          search:""
      }
  },
  created(){
      //this.$emit('header',true)
      fly.post("http://127.0.0.1:5000/check_papers",{
          id:localStorage.getItem('accessToken')
      })
      .then((response)=>{
          this.papers = response.data
      })
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
.seq{
    padding-left: 20px;
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
