<template>
    <div id="import">
        <img src="../assets/main_background.jpg" alt="">
        <div class="no-particle">
            <div class="main">
                <h2>导入学生信息</h2>
                <div class="submain">
                    <div class="content">
                        <h3>方法一：</h3>
                        <h4>请输入添加的学生学号</h4>
                        <input type="text" placeholder="学生学号" v-model="sid">
                        <h4>请输入添加的学生姓名</h4>
                        <input type="text" placeholder="学生姓名" v-model="name">
                        <button id="addbutton" class="btn btn-success btn-sm" @click="addone">添加</button>
                        <h3>方法二：</h3>
                        <h4>传入Excel文档<strong>(其中第一例标题为“学号”，第二列标题为“姓名”)</strong></h4> 
                        <input type="file" ref="upload" accept=".xls,.xlsx" @change="readExcel"/>
                        <br>
                        <div v-for="(member,index) in newmembers" :key="index" class="new">
                            <h5 id="addn">{{member.sid}}——{{member.name}}<button id="delete" class="btn btn-danger btn-sm" @click="remove(member)">删除</button></h5>

                        </div>
                        <hr>
                        <button class="btn btn-primary" @click="create_add_all">导入</button>
                        <button class="btn btn-primary" @click="clearall">清空</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script>
import XLSX from 'xlsx'
import global from './Global'
import axios from 'axios'
import $ from 'jquery';
export default {
    name:"import",
    data(){
        return{
            name:"",
            sid:"",
            newmembers:[],
            id:"",
        }
    },
    methods:{
        create_add_all(){
            let setting = {
                method: "POST",
                url: global.Url+"importsid",
                data: {
                    "students":this.newmembers,
                },
            };
            this.$axios(setting).then((response)=>{
                if(response.data.status=='OK'){
                    alert("信息导入成功")
                }else if(response.data.status=='error'){
                    alert("学号格式不规范，请检查")
                }
                
                
            })
            
        },
        clearall(){
            this.newmembers=[]
        },
        readExcel (e) {
            let that = this
            const files = e.target.files
            if (files.length < 1) {
                return false
            } else if (!/\.(xls|xlsx)$/.test(files[0].name.toLowerCase())) {
                this.$toast('上传文件格式不正确，请上传xls或者xlsx格式')
                return false
            }

            const fileReader = new FileReader()
            fileReader.onload = (ev) => {
                try {
                const data = ev.target.result
                const workbook = XLSX.read(data, {
                    type: 'binary'
                }) // 读取数据
                const wsname = workbook.SheetNames[0] // 取第一张表
                console.log(wsname)
                const ws = XLSX.utils.sheet_to_json(workbook.Sheets[wsname]) // 生成json表格内容
                that.newmembers = [] // 清空接收数据
                
                for (let i = 0; i < ws.length; i++) {
                    let sheetData = ws[i]
                    var temp ={sid:"",name:""}
                    temp.sid = sheetData['学号']
                    temp.name = sheetData['姓名']
                    that.newmembers.push(temp)
                }
                console.log(that.newmembers)
                this.$refs.upload.value = ''
                
                } catch (e) {
                console.log(e)
                return false
                }
            }
            fileReader.readAsBinaryString(files[0])
        },
        addone(){
            if(this.sid==""){
                alert("请输入学号")
            }else if(this.name==""){
                alert("请输入姓名")
            }else{
                this.newmembers.push({sid:this.sid,name:this.name})
                this.sid=""
                this.name=""
            }
            
        },
        remove(number){
            var temp=number
            let index = -1
            for(let i=0;i<this.newmembers.length;i++){
                let temp2=this.newmembers[i]
                if(temp2==temp){
                    index = i
                    break
                }
            }
            if(index>=0){
                this.newmembers.splice(index,1)
            }
        }
    }
    
}
</script>

<style scoped>
#import{
    position: absolute;
    top: 10%;
    left: 15%;
    width: 85%;
    height: 90%;
    margin:0 auto;
}
img{
    z-index: -1;
    width: 40%;
    left: 33%;
    opacity: 0.3;
    position: fixed;
}
.no-particle{
    position: absolute;
    z-index: 999;
    top: 5%;
    left: 15%;
    width: 65%;
    margin:0 auto;
}
.main{
    margin: 10px 5% auto;
    padding: 10px 20px;
    min-height: 65vh;
    max-height: 100%
}
.submain{
    width: 100%;
    background: -webkit-linear-gradient(left,rgba(255, 229, 156,0.8),rgba(248, 230, 182, 0.65),) no-repeat;
    margin: 0 auto;
    padding: 10px 0;
}

.new{
    width: 100%;
}
#delete{
    margin-left: 10%;
}
#addn{
    width: 100%;
}
.content{
    width:90%;
    margin: 10px 5% auto;
}
h4{
    margin: 20px 0;
}
hr{
    width:100%;
    margin-left: 0%;
}
h2{
    color: black;
}
</style>