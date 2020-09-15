<template>
    <div>
        <div class="header navbar navbar-fixed-top">
            <div class="logo">
                <h1>信研小屋~</h1>

                <div class="userinfo">
                    <button href="#" type="button" class="btn btn-default btn-lg" data-container="body" data-toggle="popover" 
                    data-placement="bottom" data-trigger="manul click"><span class="glyphicon glyphicon-user"></span>
                    </button>
                </div>
            </div>
        </div>
        <div id="left" class="navbar navbar-fixed-top">
            <nav>
            <ul class="nav nav-pills nav-stacked">
                <li><router-link to="/" exact>首页</router-link></li>
                <li role="presentation" id="bar-1">
                    <a href="#docCollapse" class="nav-header collapsed" data-toggle="collapse" id="collapseParent" @click="chevron_toggle()"><span class="glyphicon glyphicon-envelope"></span> 论文相关<span class="pull-right glyphicon glyphicon-chevron-down"></span></a>
                    <ul id="docCollapse" class="nav nav-list collapse">
                    <li><router-link to="/upload-paper" exact>上传论文信息</router-link></li>
                    <li><router-link to="/check_papers" exact>查看我的论文</router-link></li>
                    </ul>
                </li>
            </ul>
            </nav>
        <img src="./../assets/top_logo.jpg">
        </div>
        <div id="popovercontent" style="display:none">
            <p >学号：{{user.number}}</p>
            <p>姓名：{{user.name}}</p>
            <p>身份：学生用户</p>
            <button id="userbutton" type="button" class="btn btn-lg btn-block"><a href="/#/login">退出当前账户</a></button>
        </div>
    </div>
</template>


<script>
    import global from './Global'
    import $ from 'jquery'
    var fly = require("flyio")
    var e = {
        name:"blog-header",
        data(){
            return {
                user:{
                    name:"",
                    number:"",
                    identity:"普通用户"
                }
            }
        },
        created(){
            console.log(this)
            this.user.number = localStorage.getItem('accessToken')
            fly.post(global.Url+'get_info',{
                id:this.user.number
            }).then((response)=>{
                this.user.name = response.data.name
            })
            $(function (){
                $("[data-toggle='popover']").popover({
                    html : true,    
                    title: "个人信息",    
                    delay:{show:500},  
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
        },
        methods:{
            chevron_toggle(){
                $("#collapseParent").find(".pull-right").toggleClass("glyphicon-chevron-up");
                $("#collapseParent").find(".pull-right").toggleClass("glyphicon-chevron-down");
            },
        }
    }
    export default e
    
    
</script>

<style scoped>
.header{
    background: #1d50a2;
    height:13%;
    width: 100%;
}
.logo{
    margin:0px;
    width:100%;
    height: 100%;
    display: flex;
    padding:0px 40px;
    background: -webkit-linear-gradient(right,rgb(119, 173, 224),#1d50a2,) no-repeat;

}
.logo h1{
    color: white;
}

hr{
    margin-top:7px;
    *margin: 0;
    border: 0;
    color: #1d50a2;
    background-color: #1d50a2; 
    height: 2px
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
    top: 13%;
    width: 15%;
    height: 200vh;
    background:  -webkit-linear-gradient(top,rgb(119, 173, 224),rgb(203, 225, 245),white) no-repeat;
}
img{
    position: absolute;
    top: 41%;
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
p{
    font-size:15px;
    border-bottom:1px solid #D5D5D5;
}
#userbutton{
    background:rgb(119, 173, 224);
}

</style>