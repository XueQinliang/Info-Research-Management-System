<template>
    <div id="single-blog">
        <h1>{{blog.title}}</h1>
        <article>{{blog.body}}</article>
        <br><br>
        <router-link v-bind:to="'/print_order/'+blog.id">我要打印</router-link>
    </div>
</template>

<script>
    export default {
        name:"single-blog",
        data(){
            return{
                id:this.$route.params.id,
                blog:{}
            }
        },
        created(){
            this.$http.get("https://jsonplaceholder.typicode.com/posts/" + this.id)
            .then(function(data){
                this.blog = data.body;
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
</style>