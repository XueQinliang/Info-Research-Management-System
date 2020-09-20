
<template>
    <div id="bh">
        <div class="header navbar navbar-fixed-top">
            <div class="logo">
                <h1>信研小屋~</h1>

                <div class="userinfo">
                    <button href="#" type="button" class="useravatar btn btn-default btn-lg" data-container="body" data-toggle="popover" 
                    data-placement="bottom"><span class="glyphicon glyphicon-user"></span>
                    </button>
                </div>
            </div>
        </div>
        <div id="left" class="navbar navbar-fixed-top">
            <nav>
            <ul class="nav nav-pills nav-stacked">
                <li><router-link to="/teacher" exact>首页</router-link></li>
                <li><router-link to="/teacher/import_sid" exact>导入账号</router-link></li>
            </ul>
            </nav>
            <img src="./../assets/top_logo.jpg">
            <div id="footer">
                <p>Copyright 2020 IRMS</p>
                <p>All Rights Reserved.</p>
            </div>
        </div>
        <div id="popovercontent" style="display:none">
            <p>学号：{{user.number}}</p>
            <p>姓名：{{user.name}}</p>
            <p>身份：教师用户</p>
           <div id="userbutton" type="button" class="useravatar btn btn-lg btn-block"><a href="/#/login">退出当前账户</a></div>
        </div>
    </div>
</template>

<script>
    import global from './Global'
    import $ from 'jquery'
    var fly = require("flyio")
    export default{
        name:"blog-header-t",
        data(){
            return {
                user:{
                    name:"",
                    number:"",
                    identity:""
                }
            }
        },
        created(){
            this.user.number = localStorage.getItem('accessToken')
            this.user.identity = '教师用户'
            fly.post(global.Url+'get_info',{
                id:this.user.number
            }).then((response)=>{
                this.user.name = response.data.name
            })
            $(function (){
                $("[data-toggle='popover']").popover({
                    html : true,
                    trigger:"manaul",    
                    title: "个人信息",
                    animation:false,      
                    content: function() {
                        
                        return $('#popovercontent').html();    
                    }   
                        
                }).on("mouseenter", function() {
                    // console.log($(".hx-flot_window li a").css)
                    var _this = this; // 这里的this触发的dom,需要存起来 否则在下面 .popover的逻辑中this会变为弹出的dom
                    $(this).popover("show");
                    $(".popover").on("mouseleave", function() {
                        $(_this).popover('hide');
                    });
                }).on("mouseleave", function() {
                    var _this = this;
                    setTimeout(function() {
                        if (!$(".popover:hover").length) {
                            $(_this).popover("hide");
                        }
                    }, 300);
                });
            });
        }
    }
    
</script>

<style scoped>
#bh{
    min-height: 100%;
}
.header{
    background: #1d50a2;
    height:10%;
    width: 100%;
}
.logo{
    margin:0px;
    width:100%;
    height: 100%;
    display: inline-block;
    padding:0px 30px;
    background: -webkit-linear-gradient(right,rgb(119, 173, 224),#1d50a2,) no-repeat;

}
.logo h1{
    position: absolute;
    color: white;
    bottom: 10%;
}

hr{
    margin-top:7px;
    *margin: 0;
    border: 0;
    color: #1d50a2;
    background-color: #1d50a2; 
    height: 2px
}

.useravatar{
    color: white;
}

.userinfo{
    position: absolute;
    top:0%;
    right:0%;
    height: 100%;
    width: 5%; 
}


a{
    color: black;
    text-decoration: none;
    padding:12px;
    border-radius: 5px;
    font-size: 20px
}
.la{
    font-weight: bold;
    font-size: 15px;
}
nav{
    margin-top: 5%;
    background: -webkit-linear-gradient(top,rgb(119, 173, 224),rgb(203, 225, 245)) no-repeat;;
    border-radius: 12px;
    width: 100%;
}
.router-link-active{
    background: rgba(226, 227, 243, 0.8);
    color:rgb(43, 61, 223);
    font:bold 20px Pingfang SC;
}
#docCollapse{
    padding: 0% 10px;
}
#docCollapse2{
    padding: 0% 10px;
}
#left{
    top: 10%;
    width: 15%;
    height: 90%;
    background:  -webkit-linear-gradient(top,rgb(119, 173, 224),rgb(203, 225, 245),rgb(218, 234, 252)) no-repeat;
}
img{
    position: relative;
    top: 65%;
    bottom: 0%;
    left: 0%;
    width: 100%;
}
h1{
    font-family:'Microsoft JhengHei';
}
button{
    background: rgba(0,0,0,0);
    height: 100%;
    border: hidden;
}
#popovercontent{
    height:30px;
    width:200px
}
#userbutton{
    background:rgb(119, 173, 224);
}
#footer{
    text-align: center;
    color: rgb(119, 173, 224);
    position: relative;
    top: 65%;
    bottom: 0%;
    left: 5%;
    z-index: 200;
    width: 90%;
}
</style>