<template>
    <div id="single-blog">
        <h2>论文详细信息</h2>
        <div id="preview">
            <div id="choices">
                <h3>您选择的文件</h3>
                <p>文件名：{{file_name}}</p>
                <button class="mybutton" @click="downloadFileClick">下载</button>
            </div>
            <div id="choices">
                <h3>您的论文主体信息</h3>
                <p>论文题目：{{Papers.title}}</p>
                <p>论文篇幅：{{Papers.length}}</p>
                <p>作者：{{Papers.author}}</p>
                <p>您的作者顺序：{{Papers.author_order}}</p>
                <p>审核结果：{{Papers.status}}</p>
            </div>
            <div id="choices">
                <h3>论文的发表信息</h3>
                <p>在线发表日期：{{Papers.online_time}}</p>
                <p>期刊发表名称：{{Papers.journal_name}}</p>
                <p>期刊出版时间：{{Papers.journal_time}}</p>
                <p>会议发表名称：{{Papers.meeting_name}}</p>
                <p>会议召开时间：{{Papers.meeting_time}}</p>
            </div>
            <br><br>
            <div v-if="show" id="check_button">
                <button @click="check_pass">审核通过</button>
                <button @click="check_notpass">审核不通过</button>
            </div>
            <div v-if="show" id="change_button">
                <button class="mybutton2">
                    <router-link class="ptext" v-bind:to="'/teacher/alter_paper/'+title+'/'+author">修改信息</router-link>
                </button>
            </div>
            <div v-if="show2">
                <button class="mybutton2">
                    <router-link class="ptext" v-bind:to="'/alter_paper/'+title+'/'+author">修改信息</router-link>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import global from './Global'
import fly from 'flyio';
    export default {
        name:"single-blog",
        data(){
            return{
                title:this.$route.params.title,
                author:this.$route.params.author,
                file_name:"",
                Papers:{},
                url:"",
                save:"",
                show:false,
                show2:false
            }
        },
        created(){
            fly.post(global.Url+'get_detail',{
                p_title:this.title,
                author:this.author
            })
            .then((response)=>{
                this.Papers = response.data.paper;
                this.url = response.data.url
                this.save = response.data.save
                var temp=this.url.split('/')
                console.log(temp[temp.length-1].slice(6,))
                this.file_name = temp[temp.length-1].slice(6,)
                 if(response.data.paper.status == "审核通过"){
                    this.show2 = false
                    this.show = false
                }else if(sessionStorage.getItem('identity')=='teacher'){
                    this.show = true
                    this.show2 = false
                }else{
                    this.show = false
                    this.show2 = true
                }
            })
        },
        methods:{
            downloadFileClick() {
                console.log(this.url);
            　　//在本页打开窗口
                let $eleForm = $("<form method='get'></form>");
                $eleForm.attr("action",this.url);
                $(document.body).append($eleForm);
                //提交表单，实现下载
                $eleForm.submit();
            },
            check_pass(){
                fly.post(global.Url+'check_pass',{
                    title:this.title,
                    author:this.author
                })
                .then((response)=>{
                    if(response.data.issuccess == 'Success'){
                        this.Papers.status = '审查通过'
                        alert('审查更改成功')
                        window.location.href = '#/teacher'
                    }
                })
            },
            check_notpass(){
                fly.post(global.Url+'check_notpass',{
                    title:this.title,
                    author:this.author
                })
                .then((response)=>{
                    if(response.data.issuccess == 'Success'){
                        this.Papers.status = '审查不通过'
                        alert('审查更改成功')
                        window.location.href = '#/teacher'
                    }
                })
            }
        }
    }
</script>

<style scoped>
#single-blog{
    position: absolute;
    top: 13%;
    left: 26%;
    width: 60%;
    padding:20px;
    background:rgb(210, 225, 241);
    border:1px dotted #aaa;
}
label{
    display: block;
    margin:20px 0 10px;
}

.mybutton{
    display: block;
    background: rgb(35, 101, 223);
    color:#fff;
    border:0;
    border-radius: 4px;
    width:60px;
    height: 30px;
    cursor: pointer;
}

.mybutton2{
    display: block;
    background: rgb(35, 101, 223);
    color:#fff;
    border:0;
    border-radius: 4px;
    width:120px;
    height: 40px;
    font-size: 18px;
    cursor: pointer;
}

.ptext{
    color: #fff;
}

#preview{
    padding: 10px 20px;
    background: rgb(210, 225, 241);
    margin:0;
}
#choices{
    padding:20px;
    max-width: 800px;
    margin:10px 0 auto;
    background: #eee;
    border: 1px dotted #aaa;
}
#check_button{
    display: inline-block;
}
#check_button button{
    background: rgb(35, 101, 223);
    color:#fff;
    border:0;
    border-radius: 4px;
    width:120px;
    height: 40px;
    font-size: 18px;
    cursor: pointer;
}
#change_button{
    display: inline-block;
}
</style>