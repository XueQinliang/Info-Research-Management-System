<template>
  <div id="print-order">
    <h2>订单状态查询</h2>
    <form v-if="!submitted">
        <div id="choices">
            <h3>请输入您要查询的订单号：</h3>
            <input type="text" v-model="id">
            <h3>请输入您提交订单时的手机号：</h3>
            <input type="text" v-model="phonenumber">
        </div>
        <button @click.prevent="search">查询</button>
    </form>
    <hr v-if="!submitted">

    <div v-if="submitted">
        <h3>您的订单信息</h3>
        <div id="preview">
            <h3>订单总览</h3>
            <div id="choices">
                <h4>您选择的文件</h4>
                <p>标题：{{order.title}}</p>
                <label>页数：{{order.pages}}</label>
            </div>
            <div id="choices">
                <h4>您打印的纸张信息</h4>
                <p>纸张材质：{{order.papertexture}}</p>
                <p>纸张大小：{{order.papersize}}</p>
            </div>
            <div id="choices">
                <h4>您打印的文件信息</h4>
                <p>打印颜色：{{order.printcolor}}</p>
                <p>装订方法：{{order.bookbinding}}</p>
                <p>单双面选择：{{order.twosize}}</p>
                <p>份数：{{order.amount}}</p>
            </div>
            <div id="choices">
                <h4>备注信息</h4>
                <p>是否共享：{{order.share}}</p>
                <p>页面选择：{{order.printway}}</p>
            </div>
            <div id="choices">
                <h4>您的个人信息</h4>
                <p>配送地址：{{order.address}}</p>
                <p>手机号码：{{order.phonenumber}}</p>
            </div>
            <div id="choices">
                <h4>配送情况</h4>
                <p>支付情况：{{order.pay}}</p>
                <p>打印情况：{{order.print}}</p>
                <p>配送情况：{{order.deliver}}</p>
            </div>
        </div>
        <button @click="back">返回</button>
    </div>
  </div>
</template>


<script>
import AV from 'leancloud-storage' 
import PDFJS from 'pdfjs-dist'
import pdf from 'vue-pdf'
import PDF from 'react-pdf-js'

export default {
  components:{
        pdf
  },
  name: 'print-order',
  data () {
    return {
      order:{
          title:"",
          pages:0,
          papertexture:"",
          papersize:"",
          printcolor:"",
          bookbinding:"",
          twosize:"",
          amount:1,
          share:"",
          printway:"",
          address:"",
          phonenumber:"",
          pay:"",
          print:"",
          deliver:""
      },
      
      id:"",
      phonenumber:"",
      src:"",
      submitted:false
    }
  },
  methods:{
      search:function(){
        var query = new AV.Query('testtest')
        query.equalTo('objectId',this.id)
        query.equalTo('phonenumber',this.phonenumber)
        query.count().then((count)=>{
            console.log('count',count)
            if(count != 0){
                var query = new AV.Query('testtest')
                query.equalTo('objectId',this.id)
                query.equalTo('phonenumber',this.phonenumber)
                query.first().then((find)=>{
                    for (var key in this.order){
                        this.order[key] = find.get(key)
                        if(this.order[key] == false){
                            this.order[key] = "未完成"
                        }else if(this.order[key] == true){
                            this.order[key] = "已完成"
                        }
                        console.log(key,":",this.order[key])
                    }
                    this.submitted = true
                })
            }else{
                alert('无法查到指定的订单，请检查信息正确无误')
            }
        })
      },
      back:function(){
          for(var key in this.order){
              if(key == 'pages' || key == 'amount'){
                  this.order[key] = 0
              }else{
                  this.order[key] = ""
              }
          }
          this.submitted = false
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#print-order *{
    box-sizing: border-box;
}
#print-order{
    margin:20px auto;
    max-width: 600px;
    padding:20px;
    background: goldenrod;
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
    margin:20px auto;
    background: crimson;
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
