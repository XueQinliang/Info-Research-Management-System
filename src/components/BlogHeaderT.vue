
<template>
    <div>
        <div class="header navbar navbar-fixed-top">
            <div class="logo">
                <h1>信研小屋~</h1>

                <div class="userinfo">
                    <table class='tables' border="1">
                        <tr>
                            <td class='txttd' >{{user.name}}</td>
                        </tr>  
                        <tr>
                            <td class='txttd'>{{user.number}}</td>
                        </tr>
                    </table>
                    <button type="button" id="userbutton" class="btn btn-info btn-lg btn-block">><a href="/#/login" class='la'>退出当前账户</a></button>
                </div>
            </div>
        </div>
        <div id="left" class="navbar navbar-fixed-top">
            <nav>
            <ul class="nav nav-pills nav-stacked">
                <li><router-link to="/teacher" exact>首页</router-link></li>
            </ul>
            </nav>
        <img src="./../assets/top_logo.jpg">
        </div>
           
    </div>
</template>

<script>
    import global from './Global'
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
        }
    }
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
    width: 22%; 
}
button{
    text-align: center;
    width: 100%;
    height: 100%;
    border: 1px solid black;
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

.tables{
    height: 100%;
    width: 45%;
    float:left;
    table-layout: fixed;
}
.txttd{
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    text-align:center;
    background-color: rgb(58, 234, 247);
}
#userbutton{
    height: 100%;
    width: 55%;
}
</style>