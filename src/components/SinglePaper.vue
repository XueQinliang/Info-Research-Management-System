<template>
    <div id="single-blog">
        <h2>论文详细信息</h2>
        <div id="preview">
            <div id="choices">
                <h3>您选择的文件</h3>
                <p>标题：{{Papers.title}}</p>
            </div>
            <div id="choices">
                <h3>您的论文主体信息</h3>
                <p>论文题目：{{Papers.title}}</p>
                <p>论文篇幅：{{Papers.length}}</p>
                <p>作者：{{Papers.author}}</p>
                <p>您的作者顺序：{{Papers.author_order}}</p>
            </div>
            <div id="choices">
                <h3>论文的发表信息</h3>
                <p>在线发表日期：{{Papers.online_time}}</p>
                <p>期刊发表名称：{{Papers.journal_name}}</p>
                <p>期刊出版时间：{{Papers.journal_time}}</p>
                <p>会议发表名称：{{Papers.meeting_name}}</p>
                <p>会议召开时间：{{Papers.meeting_time}}</p>
            </div>
        </div>
    </div>
</template>

<script>
import fly from 'flyio';
    export default {
        name:"single-blog",
        data(){
            return{
                title:this.$route.params.title,
                author:this.$route.params.author,
                Papers:{}
            }
        },
        created(){
            console.log(this.$route.params.title)
            fly.post('http://127.0.0.1:5000/get_detail',{
                p_title:this.title,
                author:this.author
            })
            .then((response)=>{
                this.Papers = response.data;
            })
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