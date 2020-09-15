<template>
  <div  id="show-files">
      <!-- <h1>我的论文</h1> -->
      <img src="./../assets/main_background.jpg">
      <h3>根据审核状态筛选论文</h3><br>
      <div class="selectinput">
            <select name="status" class="searchbox" v-model="search.status">
                <option value="全部">全部</option>
                <option value="审核通过">审核通过</option>
                <option value="审核不通过">审核不通过</option>
                <option value="待审核">待审核</option>
            </select>
        </div>
      <button id="search" class="btn btn-primary" @click="search_papers">筛选</button>
      <div v-for="(paper,index) in papers" :key="index" class="single-blog">
          <router-link v-bind:to="'/paper_detail/'+paper.title+'/'+paper.author">
            <h2 v-rainbow>{{paper.title}}</h2>
          </router-link>
          <article>
              <b class="author">作者：{{paper.author}} </b>
              <b class="seq">作者序：{{paper.sequence}}</b>
              <b class="status">审核状态：{{paper.status}}</b>
          </article>
      </div>
  </div>
</template>

<script>
import global from './Global'
var fly = require('flyio')

export default {
  name: 'show-files',
  data(){
      return{
          papers:[

          ],
          search:{
              author:null,
              journal:null,
              meeting:null,
              size:null,
              time:null,
              status:"全部",
              sequence:null
          }
      }
  },
  methods:{
        search_papers(){
          if(this.search.size=="全部"){
              this.search.size = null
          }
          if(this.search.status=="全部"){
              this.search.status = null
          }
          if(this.search.sequence=="全部"){
              this.search.sequence = null
          }
          if(this.search.author==""){
              this.search.author = null
          }
          if(this.search.journal==""){
              this.search.journal = null
          }
          if(this.search.meeting==""){
              this.search.meeting = null
          }
          if(this.search.time==""){
              this.search.time = null
          }
          let setting={
            method: "POST",
            url: global.Url+"filter_papers",
            data: {
                "status":this.search.status,
                "author": this.search.author,
                "journal": this.search.journal,
                "meeting": this.search.meeting,
                "size": this.search.size,
                "time": this.search.time,
                "sequence": this.search.sequence
            },
          }
          this.$axios(setting).then((response)=>{
              console.log(response)
              this.papers = response.data
          })
      }
  },
  created(){
        this.search.author=sessionStorage.getItem('name')
        let setting={
            method: "POST",
            url: global.Url+"filter_papers",
            data: {
                "status":null,
                "author": sessionStorage.getItem('name'),
                "journal": null,
                "meeting": null,
                "size": null,
                "time": null,
                "sequence": null
            },
          }
          this.$axios(setting).then((response)=>{
              console.log(response)
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
    position: absolute;
    max-width: 800px;
    height: 100%;
    left: 24%;
    width: 68%;
    top: 13%;
    bottom: 0%;
}
.seq{
    padding-left: 20px;
}

.searchbox{
    height: 30px;
}

.single-blog{
    padding:20px;
    margin: 20px 0;
    background:  rgba(240, 243, 240,0.4);
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
.selectinput{
    width: 22%;
    display: inline-block;
}
img{
    z-index: -1;
    width: 40%;
    left: 33%;
    opacity: 0.3;
    position: fixed;
}
</style>
