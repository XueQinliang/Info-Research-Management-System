<template>
  <div id="upload_paper">
    <h2>论文信息填写</h2>
    <form v-if="!submitted">
        <div id="choices">
            <h3>论文主题信息</h3>
            <label>请输入论文题目</label>
            <input type="text" v-model="Papers.title" >
            
            <label>请输入您的论文篇幅</label>
            <select name="length" v-model="Papers.length">
              <option value="长文">长文</option>
              <option value="短文">短文</option>
              <option value="demo">demo</option>
              <option value="poster">poster</option>
            </select>
            <label>请输入在这篇论文中您的作者顺序</label>
            <select name="order" v-model="Papers.author_order">
              <option value="一作">一作</option>
              <option value="二作">二作</option>
              <option value="通讯作者">通讯作者</option>
              <option value="其他">其他</option>
            </select>
            
            
        </div>
        
        <div id="choices">
            <h3>论文发表信息</h3>
            <label>请选择论文的线上发表时间</label>
            <input type="text" class="demo-input" placeholder="请选择日期" id="date1" v-model="Papers.online_time">
            <br><br>
            <label>(如有在期刊上发表)请输入期刊全称</label>

            <select class="selectpicker" id="sp1" data-live-search="true" v-model="Papers.journal_name" data-size="5" > 
            </select> 
            <label>请选择期刊出版的时间</label>
            <input type="text" class="demo-input" placeholder="请选择日期" id="date2" v-model="Papers.journal_time">
            <br><br>
            <label>(如有在会议上发表)请输入会议全称</label>
            <select class="selectpicker" id="sp2" data-live-search="true" v-model="Papers.meeting_name" data-size="5" >
            </select>
            <label>请选择会议举行的时间</label>
            <input type="text" class="demo-input" placeholder="请选择日期" id="date3" v-model="Papers.meeting_time"> 
        </div>
        <div id="choices">
          <form method="post" onsubmit ="
                  $('#file_form').ajaxSubmit({
                    async: false,
                    data:{'usr': sessionStorage.getItem('accessToken')},
                    success:function(message) {
                        console.log(message)
                        // 对于表单提交成功后处理，message为提交页面saveReport.htm的返回内容
                        if (message=='fail upload file'){
                          alert('上传文件失败')
                        }else{
                          alert('上传文件成功')
                          sessionStorage.setItem('url',message)
                          console.log(sessionStorage.getItem('url'))
                        }
                  }});
                  return false;"
            enctype="multipart/form-data" id="file_form">
              <label>上传论文内容(PDF格式)</label>
              <div id="filename">
                已选文件：{{order.title}}
              </div>
              <input type="file" id="avatar-upload" name="uploadfile" />
              <input id="upload_button" type='submit' @click="isupload" value='上传' />
            </form>
        </div>
    </form>
    <button v-if="!submitted" @click="post">预览论文信息</button>

    <hr v-if="!submitted">

    <div v-if="submitted">
        <h3>准备上传！请确认您的论文信息无误！</h3>
        <div id="preview">
            <h3>论文信息总览</h3>
            <div id="choices">
                <h4>您选择的文件</h4>
                <p>文件名：{{order.title}}</p>
            </div>
            <div id="choices">
                <h4>您的论文主体信息</h4>
                <p>论文题目：{{Papers.title}}</p>
                <p>论文篇幅：{{Papers.length}}</p>
                <p>您的作者顺序：{{Papers.author_order}}</p>
            </div>
            <div id="choices">
                <h4>论文的发表信息</h4>
                <p>在线发表日期：{{Papers.online_time}}</p>
                <p>期刊发表名称：{{Papers.journal_name}}</p>
                <p>期刊出版时间：{{Papers.journal_time}}</p>
                <p>会议发表名称：{{Papers.meeting_name}}</p>
                <p>会议召开时间：{{Papers.meeting_time}}</p>
            </div>
            <div id="chioces">
              <button @click="downloadFileClick">论文下载</button>
            </div>
        </div>
        <div>
          <button style="float:left;margin-right:10px;" @click="upload">确定并上传</button>
          <button style="float:left" @click="back">返回</button>
        </div>
        
    </div>
  </div>
</template>
<script>
import global from './Global'
import PDFJS from 'pdfjs-dist'
import pdf from 'vue-pdf'
import PDF from 'react-pdf-js'
import dataPicker from '../../static/js/dataPicker'
import $ from 'jquery'

var fly = require("flyio")


export default {
  components:{
        pdf
  },
  name: 'upload_paper',
  data () {
    return {
        fuzzymatchtest:'',
        Papers:{
            title:"",
            length:"",
            author_order:"",
            journal_name:"",
            meeting_name:"",
            online_time:"",
            journal_time:"",
            meeting_time:"",
            url:""
        },
        order:{
            title:"未选择文件",
            pages:0,
        },
        time:"",
        id:"",
        submitted:false,
        click:false,
        url:global.Url,
        journals:[]
    }
  },
  updated(){
    laydate.render({
        elem: '#date1',
        done: (value) => {
          this.Papers.online_time = value
          console.log(this.Papers.online_time)
        }
      })
      laydate.render({
        elem: '#date2',
        done: (value) => {
          this.Papers.journal_time = value
          console.log(this.Papers.journal_time)
        }
      })
      laydate.render({
        elem: '#date3',
        done: (value) => {
          this.Papers.meeting_time = value
          console.log(this.Papers.meeting_time)
        }
      })
  },
  mounted(){
    
    $(function(){
  file_form.action = global.Url+'upload_file'
  $(".selectpicker").selectpicker('refresh');
}),
      laydate.render({
        elem: '#date1',
        done: (value) => {
          this.Papers.online_time = value
          console.log(this.Papers.online_time)
        }
      })
      laydate.render({
        elem: '#date2',
        done: (value) => {
          this.Papers.journal_time = value
          console.log(this.Papers.journal_time)
        }
      })
      laydate.render({
        elem: '#date3',
        done: (value) => {
          this.Papers.meeting_time = value
          console.log(this.Papers.meeting_time)
        }
      })
  },
  methods:{
      downloadFileClick() {
        console.log(this.Papers.url);
        //在本页打开窗口
        let $eleForm = $("<form method='get'></form>");
        $eleForm.attr("action",'irms.ruc.edu.cn/download/'+this.Papers.url);
        $(document.body).append($eleForm);
        //提交表单，实现下载
        $eleForm.submit();
      },
      isupload(){
        var avatarUpload = document.getElementById('avatar-upload')
        var fname = avatarUpload.value;
        var pos=fname.lastIndexOf("\\");
        var filename=fname.substring(pos+1);
        this.order.title = filename 
        this.click = true
      },
      back(){
        this.submitted = false
        var _this = this
            setTimeout(function(){
                let setting1 = {
                    method: "POST",
                    url: global.Url+"fuzzyjournal",
                    data: {
                        "string":""
                    },
                }
                _this.$axios(setting1).then((response)=>{
                var temp = "空"
                $("#sp1").html('')
                $("#sp1").append("<option value=''>"+temp+"</option>")
                $.each(response.data,function(index,item){
                    var typestr = ""
                    if(item.J_Name==_this.Papers.journal_name){
                        typestr = "<option selected>"+item.J_Name+"</option>"
                    }else{
                        typestr = "<option>"+item.J_Name+"</option>"
                    }
                    $("#sp1").append(typestr)
                })
                $("#sp1").selectpicker('refresh');
                $("#sp1").selectpicker('show');
                
                })
                let setting2 = {
                    method: "POST",
                    url: global.Url+"fuzzymeeting",
                    data: {
                        "string":""
                    },
                }
                _this.$axios(setting2).then((response)=>{
                console.log(response)
                var temp = "空"
                $("#sp2").html('')
                $("#sp2").append("<option value=''>"+temp+"</option>")
                console.log(_this.Papers.meeting_name)
                $.each(response.data,function(index,item){
                    var typestr=""
                    if(item.M_FName==_this.Papers.meeting_name){
                        typestr = "<option selected>"+item.M_FName+"</option>"
                    }else{
                        typestr = "<option>"+item.M_FName+"</option>"
                    }
                    $("#sp2").append(typestr)
                })
                $("#sp2").selectpicker('refresh');
                $("#sp2").selectpicker('show');
                })
            },1000)
      },
     getName:function(){
        var avatarUpload = document.getElementById('avatar-upload')
        var fname = avatarUpload.value;
      },
      post:function(){ 
        
        if (this.Papers.title == ""){
          alert("请输入论文题目")
        }else if(this.order.title == ""){
          alert("请上传论文文件(PDF格式)")
        }else if(this.Papers.length == ""){
          alert("请填写论文篇幅")
        }else if(this.Papers.author_order == ""){
          alert("请输入您的作者顺序")
        }else if(this.Papers.online_time == ""){
          alert("请填写线上发表时间")
        }else if(this.Papers.journal_name == "" && this.Papers.meeting_name == ""){
          alert("会议发表、期刊发表请至少填写一项")
        }else if(this.Papers.journal_time == "" && this.Papers.journal_name != ""){
          alert("请填写期刊发表时间")
        }else if(this.Papers.meeting_time == "" && this.Papers.meeting_name != ""){
          alert("请填写会议发表时间")
        }else if(this.click==false){
          alert("请点击文件旁的上传按钮")
        }else{
          //文件上传
          this.Papers.url = sessionStorage.getItem('url')
          console.log(this.Papers.url)
          this.submitted = true
        }
      },
      upload(){
        fly.post(global.Url+'upload',{
          sid:sessionStorage.getItem('accessToken'),
          author:sessionStorage.getItem('name'),
          title:this.Papers.title,
          size:this.Papers.length,
          sequence:this.Papers.author_order,
          journal:this.Papers.journal_name,
          meeting:this.Papers.meeting_name,
          otime:this.Papers.online_time,
          jtime:this.Papers.journal_time,
          mtime:this.Papers.meeting_time,
          purl:sessionStorage.getItem('url'),
          jlevel:"",
          jsname:"",
          mlevel:"",
          msname:""
        }).then(function(response){
          alert("上传成功")
          window.location.href = '/'
        })
      },
     
  },
  created(){
    let setting1 = {
      method: "POST",
      url: global.Url+"fuzzyjournal",
      data: {
        "string":""
      },
    }
    this.$axios(setting1).then((response)=>{
      var temp = "空"
      $("#sp1").html('')
      $("#sp1").append("<option value=''>"+temp+"</option>")
      $.each(response.data,function(index,item){
        var typestr = '<option>'+item.J_Name+'</option>'
        $("#sp1").append(typestr)
      })
      $("#sp1").selectpicker('refresh');
      $("#sp1").selectpicker('show');
    })
    let setting2 = {
      method: "POST",
      url: global.Url+"fuzzymeeting",
      data: {
        "string":""
      },
    }
    this.$axios(setting2).then((response)=>{
      console.log(response)
      var temp = "空"
      $("#sp2").html('')
      $("#sp2").append("<option value=''>"+temp+"</option>")
      $.each(response.data,function(index,item){
        var typestr = '<option>'+item.M_FName+'</option>'
        $("#sp2").append(typestr)
      })
      $("#sp2").selectpicker('refresh');
      $("#sp2").selectpicker('show');
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#upload_paper *{
    box-sizing: border-box;
}
#upload_paper{
    position: absolute;
    top: 13%;
    left: 30%;
    width: 50%;
    padding:20px;
    background: rgb(210, 225, 241);
}
#upload_button{
    margin-top:10px;
}
#choices{
    padding:20px;
    max-width: 800px;
    margin:10px 0 auto;
    background: #eee;
    border: 1px dotted #aaa;
}
label{
    display: block;
    margin:20px 0 10px;
}
input[type="text"],input[type="number"],textarea{
    display: block;
    width:100%;
    padding:8px;
}
select{
    display: inline-block;
    width:100%;
    padding:8px;
}
textarea{
    height: 200px;
}
#checkboxes label{
    display: inline-block;
    margin-top: 10px;
}
#checkboxes input{
    display: inline-block;
    margin-right: 10px;
}
button{
    display: block;
    margin:20px 0;
    background: rgb(35, 101, 223);
    color:#fff;
    border:0;
    padding:14px;
    border-radius: 4px;
    font-size: 18px;
    cursor: pointer;
}
.upload{
  display: block;
  padding:6px;
  margin:20px 0;
  height:25px;
  width:75px;
  background: rgb(185, 184, 189);
  color:black;
  font-size:12px;
}
#preview{
    padding: 10px 20px;
    border:1px dotted #ccc;
    margin:30px 0 0 0;
}
h3{
    margin-top: 10px;
}
.selectpicker{
  position: relative;
  width: 100%;
}
</style>
