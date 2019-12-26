<template>
    <div id="login">
        <div class="top">
            <img src='./../assets/top_logo3.png'>
            <h1>中国人民大学信息学院科研管理系统</h1>
        </div>
        <div id="login-inputgroup" style="margin:-5px">
            <div class="inputbox">
                <img src="./../assets/user.png" class="inputaddon"/>
                <input type="text" placeholder="学工号" id="inUsr" v-model="user.id" required autofocus/>
            </div>
            <div class="inputbox">
                <img src="./../assets/pwd.png" class="inputaddon"/>
                <input type="password" placeholder="密码" id="inPw" v-model="user.password" required/>
            </div>
        </div>
    <div>
        <button id="loginButton" title="账号登录" @click="dologin">
            <img src="./../assets/login.png" id="icon-login" />
            <span>登录</span><span style="display:none">登录中...</span>
        </button>
    </div>

    </div>
</template>

<script>

import $ from 'jquery';

var fly = require('flyio')

export default {
    name:"login",
    data(){
        return{
            user:{
                id:"",
                password:""
            },
        }
    },
    created(){
        this.$emit('header',false)
        this.user.id = localStorage.getItem('accessToken')
        var that = this;
        document.onkeydown = function(e) {
            var key = window.event.keyCode;
            if (key == 13) {
                that.enterSearchMember();
            }
        }
    },
    methods:{
        enterSearchMember() {
            this.dologin()
        },
        dologin(){
            $("#loginButton span").toggle();
            var usr = $("#inUsr").val();
            var pw = $("#inPw").val();
            //alert(usr+pw)
            fly.post('http://127.0.0.1:5000/login',{
                username:usr,
                password:pw
            }).then(function(response){
                console.log(response)
                if(parseInt(response.data.islogin)== 1){
                    sessionStorage.setItem('accessToken',usr)
                    localStorage.setItem('accessToken',usr)
                    window.location.href = '/'
                }else{
                    alert("用户名或密码错误")
                }
            })
        },
        
    }
}
</script>

<style scoped>
#login{
    /*position: absolute;*/
    width: 203vh;
    height: 80vh;
    padding: 50px 20px;
    background: rgb(23,162,207);

}
.top{
    margin:20px auto;
    padding: 0% 10%;
    text-align: center
}

#login-inputgroup{
    margin: 20px auto;
    text-align:center;
}
.inputbox{
    position: relative;
    width:290px;
    height:40px;
    margin:20px 10px;
    display: inline-block;
}
.inputbox input{
    width:240px;
    height:30px;
    padding:5px 5px 5px 45px;
    border:none;
    border-radius:1px;
    box-shadow:0px 2px 1px rgba(0,0,0,0.3);
}
.inputbox .inputaddon{
    position: absolute;
    left:14px;
    top:9px;
}
button{
    display:block;
    width:200px;
    height:40px;
    line-height:40px;
    background-color:rgb(35,45,59);
    color:#fff;
    border:none;
    margin:10px auto 0px auto;
    box-shadow:0px 2px 1px rgba(51,153,153,1);
    cursor:pointer;}

</style>