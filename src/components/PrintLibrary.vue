<template>
  <div id="print-order">
    <h2>文件及配送信息</h2>
    <form v-if="!submitted">
        <div id="choices">
            <h3>请选择所要进行打印的纸张信息</h3>
            <label >纸张材质</label>
            <select v-model="order.papertexture" required>
                <option v-for="(pt,index) in papertextures" :key="index">
                    {{pt}}
                </option>
            </select>
            <label >纸张大小</label>
            <select v-model="order.papersize" required>
                <option v-for="(ps,index) in papersizes" :key="index">
                    {{ps}}
                </option>
            </select>
        </div>
        <div id="choices">
            <h3>请选择所要进行打印的文件信息</h3>
            <label >打印颜色：</label>
            <div id="checkboxes">
                <label>黑白</label>
                <input type="radio" v-model="order.printcolor" value="黑白" >
                <label>彩色</label>
                <input type="radio" v-model="order.printcolor" value="彩色" >
            </div>
            <label >装订方法：</label>
            <select v-model="order.bookbinding" required>
                <option v-for="(bb,index) in bookbindings" :key="index">
                    {{bb}}
                </option>
            </select>
            <label >单双面选择：</label>
            <div id="checkboxes">
                <label>单面打印</label>
                <input type="radio" v-model="order.twosize" value="单面打印" >
                <label>双面打印</label>
                <input type="radio" v-model="order.twosize" value="双面打印" >
            </div>
            <label >份数：</label>
            <input type="number" value=1 v-model="order.amount">
        </div>
        <div id="choices">
            <h3>备注信息</h3>
            <label >是否共享：</label>
            <div id="checkboxes">
                <label>上传并共享</label>
                <input type="radio" v-model="order.share" value="上传并共享">
                <label>不共享仅打印</label>
                <input type="radio" v-model="order.share" value="不共享仅打印" >
            </div>
            <label >页面选择：</label>
            <div id="checkboxes">
                <label>不作为PPT打印</label>
                <input type="radio" v-model="order.printway" value="不作为PPT打印">
                <label>使用PPT格式打印（一页六张）</label>
                <input type="radio" v-model="order.printway" value="使用PPT格式打印（一页六张）" >
            </div>
        </div>
        <div id="choices">
            <h3>地址信息</h3>
            <label>请输入您要送达的地址：</label>
            <input type="text" v-model="order.address">
        </div>

        <button @click.prevent="post">提交订单</button>
    </form>

    <hr v-if="!submitted">

    <div v-if="submitted">
        <h3>您的订单提交成功！</h3>
        <div id="preview">
            <h3>订单总览</h3>
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
                <h4>您的地址信息</h4>
                <p>配送地址：{{order.address}}</p>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'print-order',
  data () {
    return {
      order:{
          papertexture:"",
          papersize:"",
          printcolor:"黑白",
          bookbinding:"",
          twosize:"单面打印",
          amount:1,
          share:"上传并共享",
          printway:"不作为PPT打印",
          address:""
      },
      papertextures:["普通纸","硬卡纸"],
      papersizes:["A4","A3","A5","B5"],
      bookbindings:["无装订","装订成书本","斜角装订"],
      submitted:false
    }
  },
  methods:{
      post:function(){
        this.$http.post(`https://jsonplaceholder.typicode.com/posts`,{
           
        })
        .then(function(data){
            console.log(data)
            this.submitted = true
        })
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
    margin:20px 0;
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
