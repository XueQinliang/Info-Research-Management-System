<template>
  <div id="upload_paper">
    <h2>论文信息填写</h2>
    <form v-if="!submitted">
        <div id="choices">
            <h3>论文主题信息</h3>
            <label>请输入论文题目</label>
            <input type="text" v-model="Papers.title" >
            <label>上传论文内容(PDF格式)</label>
            <input type="file" id="avatar-upload" >
            <label>请输入在这篇论文中您的作者顺序</label>
            <input type="text" v-model="Papers.author_order" >
            
        </div>
        
        <div id="choices">
            <h3>论文发表信息</h3>
            <label>请选择论文的线上发表时间</label>
            <input class="js-date-picker1" type="text" placeholder="选择发表日期" v-model="Papers.online_time" readonly >
            <br><br>
            <label>(如有在期刊上发表)请输入期刊全称</label>
            <input type="text" v-model="Papers.journal_name">
            <label>请选择期刊出版的时间</label>
            <input class="js-date-picker2" type="text" placeholder="选择发表日期" v-model="Papers.journal_time" readonly>
            <br><br>
            <label>(如有在会议上发表)请输入会议全称</label>
            <input type="text" v-model="Papers.meeting_name">
            <label>请选择会议举行的时间</label>
            <input class="js-date-picker3" type="text" placeholder="选择发表日期" v-model="Papers.meeting_time" readonly>
        </div>
    </form>
    <button v-if="!submitted" @click="post">上传论文信息</button>

    <hr v-if="!submitted">

    <div v-if="submitted">
        <h3>准备上传！请确认您的论文信息无误！</h3>
        <div id="preview">
            <h3>论文信息总览</h3>
            <div id="choices">
                <h4>您选择的文件</h4>
                <p>标题：{{order.title}}</p>
                <p>URL：{{src}}</p>
                <pdf :src="src" @num-pages="order.pages=$event"></pdf>
                <label>页数：{{order.pages}}</label>
            </div>
            <div id="choices">
                <h4>您的论文主体信息</h4>
                <p>论文题目：{{Papers.title}}</p>
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
        </div>
        <button>确定并上传</button>
        
    </div>
  </div>
</template>


<script>
document.title = "论文信息上传"

import PDFJS from 'pdfjs-dist'
import pdf from 'vue-pdf'
import PDF from 'react-pdf-js'

export default {
  components:{
        pdf
  },
  name: 'upload_paper',
  data () {
    return {
        Papers:{
            title:"",
            length:"",
            author_order:"",
            journal_name:"",
            meeting_name:"",
            online_time:"",
            journal_time:"",
            meeting_time:""
        },
        order:{
            title:"",
            pages:0,
        },
        id:"",
        src:"",
        submitted:false
    }
  },
  mounted(){
      this.DateSelect1();
      this.DateSelect2();
      this.DateSelect3();
  },
  methods:{
    DateSelect1() {
      var calendar = new datePicker();
      calendar.init({
        trigger: ".js-date-picker1" /*按钮选择器，用于触发弹出插件*/,
        type:
          "date" /*模式：date日期；datetime日期时间；time时间；ym年月；year:年*/,
        minDate: "1900-1-1" /*最小日期*/,
        maxDate: "2100-12-31" /*最大日期*/,
        onSubmit: function() {
          /*确认时触发事件*/
          var theSelectData = calendar.value;
        },
        onClose: function() {
          /*取消时触发事件*/
        }
      });
    },
    DateSelect2() {
      var calendar = new datePicker();
      calendar.init({
        trigger: ".js-date-picker2" /*按钮选择器，用于触发弹出插件*/,
        type:
          "date" /*模式：date日期；datetime日期时间；time时间；ym年月；year:年*/,
        minDate: "1900-1-1" /*最小日期*/,
        maxDate: "2100-12-31" /*最大日期*/,
        onSubmit: function() {
          /*确认时触发事件*/
          var theSelectData = calendar.value;
        },
        onClose: function() {
          /*取消时触发事件*/
        }
      });
    },
    DateSelect3() {
      var calendar = new datePicker();
      calendar.init({
        trigger: ".js-date-picker3" /*按钮选择器，用于触发弹出插件*/,
        type:
          "date" /*模式：date日期；datetime日期时间；time时间；ym年月；year:年*/,
        minDate: "1900-1-1" /*最小日期*/,
        maxDate: "2100-12-31" /*最大日期*/,
        onSubmit: function() {
          /*确认时触发事件*/
          var theSelectData = calendar.value;
        },
        onClose: function() {
          /*取消时触发事件*/
        }
      });
    },
     getName:function(){
        var avatarUpload = document.getElementById('avatar-upload')
        var fname = avatarUpload.value;
      },
      post:function(){
        var avatarUpload = document.getElementById('avatar-upload')
        var fname = avatarUpload.value;
        var pos=fname.lastIndexOf("\\");
        var filename=fname.substring(pos+1); 
        this.order.title = filename 
        if (this.Papers.title == ""){
          alert("请输入论文题目")
        }else if(this.order.title == ""){
          alert("请上传论文文件(PDF格式)")
        }else if(this.Papers.author_order == ""){
          alert("请输入您的作者顺序")
        }else if(this.Papers.online_time == "" && this.Papers.journal_time == "" && this.Papers.meeting_time == ""){
          alert("线上发表时间、会议发表时间、期刊发表时间请至少填写一项")
        }else if(this.Papers.journal_time != "" && this.Papers.journal_name == ""){
          alert("请填写期刊名称")
        }else if(this.Papers.meeting_time != "" && this.Papers.meeting_name == ""){
          alert("请填写会议名称")
        }else{
          //文件上传
          this.submitted = true
        }
      },
      update:function(){
        /*console.log('pages:',this.order.pages)
        var update = AV.Object.createWithoutData('testtest',this.id)
        update.set('pages',this.order.pages)
        update.save()
        .then((update)=>{
            console.log('pages:',this.order.pages)
        })*/
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#upload_paper *{
    box-sizing: border-box;
}
#upload_paper{
    margin:20px auto;
    max-width: 600px;
    padding:20px;
    background: rgb(222, 230, 193);
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
    background: rgb(49, 15, 199);
    color:#fff;
    border:0;
    padding:14px;
    border-radius: 4px;
    font-size: 18px;
    cursor: pointer;
}
#preview{
    padding: 10px 20px;
    border:1px dotted #ccc;
    margin:30px 0;
}
h3{
    margin-top: 10px;
}
</style>
