<template>
  <div id="show-files">
      <h2>学生论文</h2>
      <img src="./../assets/main_background.jpg">
      <div id="select_box">
          <div id="selectpart1">
            <div class="selectinput">
                <label>作者姓名：</label>
                <input class="searchbox" type="text" v-model="search.author">
            </div>
            <div class="selectinput">
                <label>期刊：</label>
                <input class="searchbox" type="text" v-model="search.journal">
            </div>
            <div class="selectinput">
                <label>论文篇幅：</label><br>
                <select name="length" class="searchbox" v-model="search.size">
                    <option value="全部">全部</option>
                    <option value="长文">长文</option>
                    <option value="短文">短文</option>
                    <option value="demo">demo</option>
                    <option value="poster">poster</option>
                </select>
            </div>
            <div class="selectinput">
                <label>作者序：</label><br>
                <select name="order" v-model="search.sequence">
                    <option value="全部">全部</option>
                    <option value="一作">一作</option>
                    <option value="二作">二作</option>
                    <option value="通讯作者">通讯作者</option>
                    <option value="其他">其他</option>
                </select>
            </div>
          </div>
          <div id="selectpart2">
            <div class="selectinput">
                <label>会议：</label>
                <input class="searchbox" type="text" v-model="search.meeting">
            </div>
            <div class="selectinput">
                <label>线上发布年份(例：2019)：</label>
                <input class="searchbox" type="text" v-model="search.time">
            </div>
            <div class="selectinput">
                <label>审查结果</label><br>
                <select name="status" class="searchbox" v-model="search.status">
                    <option value="全部">全部</option>
                    <option value="审核通过">审核通过</option>
                    <option value="审核不通过">审核不通过</option>
                    <option value="待审核">待审核</option>
                </select>
            </div>
            <div id="searchbutton">
                <button type="button" class="btn btn-primary" @click="search_papers">搜索</button>
            </div>
            <div id="choices">
                <button class="btn btn-primary" @click="download_info">信息下载</button>
            </div>
          </div>
          
      </div>
      <div v-for="(paper,index) in papers" :key="index" class="single-blog">
          <router-link v-bind:to="'/teacher/paper_detail/'+paper.title+'/'+paper.author">
            <h2 v-rainbow>{{paper.title}}</h2>
          </router-link>
          <article>
              <b class="author">作者：{{paper.author}} </b>
              <b class="seq">作者序：{{paper.sequence}}</b>
              <b class="status">审查结果：{{paper.status}}</b>
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
          Papers:{
              author:[],
              title:[]
          },
          search:{
              author:null,
              journal:null,
              meeting:null,
              size:null,
              time:null,
              status:null,
              sequence:null
          }

      }
  },
  created(){
      //this.$emit('header',true)
      fly.get(global.Url+"all_papers")
      .then((response)=>{
          this.papers = response.data
          for(var i=0;i<this.papers.length;i++){
                this.Papers.title.push(this.papers[i].title)
                this.Papers.author.push(this.papers[i].author)
            }
      })
  },
  methods:{
      download_info(){
            console.log(this.Papers)
            let setting = {
                method: "POST",
                url: global.Url+"csvdownload",
                data: {
                    "title":this.Papers.title,
                    "author":this.Papers.author
                },
            }
            this.$axios(setting).then((response)=>{
                console.log(response)
                let $eleForm = $("<form method='get'></form>");
                $eleForm.attr("action","http://irms.ruc.edu.cn/"+response.data);
                $(document.body).append($eleForm);
                //提交表单，实现下载
                $eleForm.submit();
                    
            })
        },
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
#select_box{
    top: 15%;
    left: 5%;
    width: 90%;
}
#selectpart1{
    position: relative;
    top: 15%;
    left:5%;
    width: 100%;
}
#selectpart2{
    position: relative;
    top: 35%;
    left:5%;
    width: 120%;
    height: 10%;
}
#selectpart1 .selectinput{
    width: 22%;
    display: inline-block;
}
#selectpart2 .selectinput{
    width: 18.5%;
    display: inline-block;
}
.searchbox{
    height: 20px;
    width: 100%;
}

#searchbutton{
    text-align: center;
    display: inline-block;
    width: 11%;
}
.single-blog{
    padding:20px;
    margin: 20px 0;
    background: rgba(240, 243, 240,0.4);
    border:1px dotted #aaa;
}
#choices{
    text-align: center;
    display: inline-block;
    height: 20px;
    width: 11%;
    z-index: 100;
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
button{
    width: 100%;
    height: 30px;
}
img{
    z-index: -1;
    width: 40%;
    left: 33%;
    opacity: 0.3;
    position: fixed;
}
</style>
