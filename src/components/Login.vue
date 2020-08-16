<template>
    <div id="login">
        <div class="top">
            <img src='./../assets/top_logo3.png'>
            <h2>中国人民大学信息学院科研管理系统</h2>
            <!--<a href="http://202.112.113.26/hhh.c" download="hhh.c">下载试试</a>-->
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
            <button type="button" class="btn btn-primary btn-lg" id="loginButton" title="账号登录" @click="dologin">
                <span>登录</span><span style="display:none">登录中...</span>
            </button>
        </div>
        <button type="button" id="alterButton" title="修改密码"   class="btn btn-primary btn-lg" data-toggle="modal" data-target="#myModal">
            修改密码
        </button>
        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h4 class="modal-title" id="myModalLabel">请填写个人信息以修改密码</h4>
                    </div>
                    <div class="modal-body">
                        <form role="form">
                            <div class="form-group">
                                <label for="name">学号</label>
                                <input v-model="alter.sid" type="text" class="form-control" id="sid" placeholder="请输入学号"
                                data-toggle="popover" data-placement="bottom" data-content="请输入您的学号">
                            </div>
                            <div class="form-group">
                                <label for="name">原密码</label>
                                <input v-model="alter.opwd" type="password" class="form-control" id="opwd" placeholder="请输入原密码"
                                data-toggle="popover" data-placement="bottom" data-content="请输入您的原始密码">
                            </div>
                            <div class="form-group">
                                <label for="name">密码（5-20位）</label>
                                <input v-model="alter.npwd" type="password" class="form-control" id="npwd" placeholder="请输入新密码"
                                 data-toggle="popover" data-placement="bottom" data-content="请输入新密码">
                            </div>
                            <div class="form-group">
                                <label for="name">请确认密码</label>
                                <input v-model="alter.cpwd" type="password" class="form-control" id="cpwd" placeholder="请输入新密码"
                                data-toggle="popover" data-placement="bottom" data-content="请重复输入新密码">
                            </div>
                            
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
                        <button type="button" class="btn btn-primary" @click="changepwd">确认修改</button>
                    </div>
                </div><!-- /.modal-content -->
            </div><!-- /.modal -->
        </div>

    </div>
</template>

<script>

import $ from 'jquery';
import global from './Global'
import axios from 'axios'
var fly = require('flyio')

export default {
    name:"login",
    data(){
        return{
            user:{
                id:"",
                password:""
            },
            alter:{
                sid:"",
                opwd:"",
                npwd:"",
                cpwd:""
            }
        }
    },
    created(){
        this.$emit('header',false)
        this.user.id = localStorage.getItem('accessToken')
        sessionStorage.clear();
        var that = this;
        document.onkeydown = function(e) {
            var key = window.event.keyCode;
            if (key == 13) {
                that.enterlogin();
            }
        }
    },
    methods:{
        changepwd(){
            if(this.alter.cpwd!=this.alter.npwd){
                alert("两次输入密码不相同")
                $("[data-toggle='popover']").popover('hide');
                $('#cpwd').popover('show')
            }else if(this.alter.sid==""){
                alert("请输入学号")
                $("[data-toggle='popover']").popover('hide');
                $('#sid').popover('show')
            }else if(this.alter.opwd==""){
                alert("请输入旧密码")
                $("[data-toggle='popover']").popover('hide');
                $('#opwd').popover('show')
            }else if(this.alter.npwd==""){
                alert("请输入密码")
                $("[data-toggle='popover']").popover('hide');
                $('#npwd').popover('show')
            }else{
                $('#myModal').modal('hide')
                let setting={
                    method: "POST",
                    url: global.Url+"revisepswd",
                    data: {
                        "uid":this.alter.sid,
                        "oldpswd": this.alter.opwd,
                        "newpswd1": this.alter.npwd,
                        "newpswd2": this.alter.cpwd,
                    },
                }
                this.$axios(setting).then((response)=>{
                    console.log(response)
                    if(response.data.status==0){
                        alert("密码修改成功")
                    }else if(response.data.status==1){
                        alert("原密码错误")
                    }else if(response.data.status==2){
                        alert("两次输入密码不一致")
                    }
                })
            }
        },
        enterlogin() {
            this.dologin()
        },
        dologin(){
            $("#loginButton span").toggle();
            var usr = $("#inUsr").val();
            var pw = $("#inPw").val();
            //alert(usr+pw)
            fly.post(global.Url+'login',{
                username:usr,
                password:pw
            }).then(function(response){
                console.log(response)
                if(parseInt(response.data.islogin)== 1){
                    sessionStorage.setItem('accessToken',usr)
                    sessionStorage.setItem('identity','student')
                    localStorage.setItem('accessToken',usr)
                    alert(response.data.name+"同学，欢迎回来")
                    window.location.href = '/'
                }else if(parseInt(response.data.islogin)== 2){
                    sessionStorage.setItem('accessToken',usr)
                    sessionStorage.setItem('identity','teacher')
                    localStorage.setItem('accessToken',usr)
                    alert(response.data.name+"老师，欢迎回来")
                    window.location.href = '#/teacher'
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
    position: absolute;
    top: 0%;
    bottom: 0%;
    width: 100%;
    height: 100%;
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
    position: relative;
    left:10%;
    top:0%;
}
#loginButton{
    position: absolute;
    left: 34%;
    text-align: center;
    width:15%;
    height:7%;
    color:#fff;
    box-shadow:0px 2px 1px rgba(51,153,153,1);
    cursor:pointer;
    }
#alterButton{
    position: absolute;
    left: 50%;
    text-align: center;
    width:15%;
    height:7%;
    color:#fff;
    box-shadow:0px 2px 1px rgba(51,153,153,1);
    cursor:pointer;
    }

</style>