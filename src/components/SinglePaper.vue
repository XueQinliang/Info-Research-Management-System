<template>
    <div id="single-blog">
        <h2>论文详细信息</h2>
        <div id="preview">
            <div id="choices">
                <h3>您选择的文件</h3>
                <button @click="downloadFileClick">下载</button>
            </div>
            <div id="choices">
                <h3>您的论文主体信息</h3>
                <p>论文题目：{{Papers.title}}</p>
                <p>论文篇幅：{{Papers.length}}</p>
                <p>作者：{{Papers.author}}</p>
                <p>您的作者顺序：{{Papers.author_order}}</p>
                <p>审核状态：{{Papers.status}}</p>
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
            <div v-if="show">
                <button @click="check_pass">审核通过</button>
                <button @click="check_notpass">审核不通过</button>
            </div>
            <div v-if="show">
                <router-link v-bind:to="'/teacher/alter_paper/'+title+'/'+author">修改信息</router-link>
            </div>
            <div v-if="!show">
                <router-link v-bind:to="'/alter_paper/'+title+'/'+author">修改信息</router-link>
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
                Papers:{},
                url:"",
                save:"",
                show:false
            }
        },
        created(){
            if(sessionStorage.getItem('identity')=='teacher'){
                this.show = true
            }
            console.log(this.$route.params.title)
            fly.post(global.Url+'get_detail',{
                p_title:this.title,
                author:this.author
            })
            .then((response)=>{
                this.Papers = response.data.paper;
                this.url = response.data.url
                this.save = response.data.save
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
                    }
                })
            }
        }
    }
</script>

<style scoped>
#single-blog{
    max-width: 960px;
    margin:0 auto;
    padding:20px;
    background: #eee;
    border:1px dotted #aaa;
}
label{
    display: block;
    margin:20px 0 10px;
}
#preview{
    padding: 10px 20px;
    border:1px dotted #ccc;
    margin:30px 0;
}
#choices{
    padding:20px;
    max-width: 800px;
    margin:10px 0 auto;
    background: rgb(45, 179, 231);
    border: 1px dotted #aaa;
}
</style>