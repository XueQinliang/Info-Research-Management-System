<template>
  <div id="show-files" :style="bgimg">
      <br>
      <div id="text">
        <h1>欢迎来到中国人民大学信息学院科研管理系统</h1>
        <br><br>
        <p>本系统为信息学院学生的科研成果一个统一的管理系统；</p>
        <p>对于学生：</p>
        <p>可以简便、直观地上传自己取得的科研成果；</p>
        <p>查看、修正自己已经上传的记录；</p>
        <p>对于老师：</p>
        <p>可以查看、审核、导出学生上传的科研成果信息；</p>
        <p>下载相关的佐证材料，如论文PDF、出版物照片等</p>
      </div>
      <br><br><br>
  </div>
</template>

<script>
var fly = require('flyio')

export default {
  name: 'show-files',
  data(){
      return{
          bgimg:{
              backgroundImage: 'url(' + require('../assets/indexbg.jpg') + ')'
          }
      }
  }
}
</script>

<style scoped>
#show-files{
    position: absolute;
    top: 13%;
    width: 100%;
    height: 100%;
    margin:0 auto;
    background-repeat: space;
    background-size: 100% 100%;
}


#show-files p{
    color:black;
    text-decoration: none;
    text-align: center;
    font-size: 20px;
}
#show-files h1{
    text-align: center;
    padding: 30px
}
#text{
    position: absolute;
    width:50%;
    left: 30%;
    height: 80%;
    border: 2px solid;
    background: rgba(255, 255, 255, 0.6)
}
</style>
