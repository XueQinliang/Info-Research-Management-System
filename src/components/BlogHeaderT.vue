
<template>
    <div>
        <div class="header">
            <div class="logo">
                <img src='./../assets/top_logo.jpg'>
                <div class="userinfo">
                    <table class='tables' border="1">
                        <tr>
                            <td rowspan="4" height="130px" width="50px"><img src='./../assets/OIP.jpg' height="100%" width="100%"></td>
                            <td class='txttd' >{{user.name}}</td>
                        </tr>   
                        <tr>
                            <td class='txttd'>{{user.number}}</td>
                        </tr>
                        <tr>
                            <td class='txttd'>{{user.identity}}</td>
                        </tr>
                        <tr>
                            <td class='lktd'><a href="/#/login" class='la'>退出当前账户</a></td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        <nav>
            <ul>
                <li>
                    <router-link to="/teacher" exact>首页</router-link>
                    <router-link to="/upload-paper" exact>导出</router-link>
                </li>                
            </ul>   
        </nav>
           
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
/* .brand img{
    margin:0 auto;
    width:35%;
    text-align:center;
    display: flex;
    justify-content: center;
    align-items: center; 
    padding:0;
}
.brand{
    background: #1d50a2
} */
.header{
    background: #1d50a2
}
.logo{
    margin:0px;
    width:35%;
    display: flex;
    padding:0px 40px;
    background: #1d50a2;

}
hr{
    margin-top:7px;
    *margin: 0;
    border: 0;
    color: #1d50a2;
    background-color: #1d50a2; 
    height: 2px
}
ul{
    list-style-type: none;
    text-align: center;
    margin:0;
    margin-bottom: 20px;
    padding:20px 40px;
    border: 10px solid #1d50a2;
    border-left-width: 40px;
    border-right-width: 40px;
}
li{
    display: inline-block;
    margin: 0 10px;
    background: white;
}
.userinfo{
    position: absolute;
    top:10px;
    right:10px;
    height: 145px;
    width: 300px; 
    background: rgb(99, 185, 243);
    border: 1px solid rgb(25, 21, 226)
}
/* .liimgright{
    float:left;
    margin: 5px 5px;
    position: absolute;
    top:15px;
    right:150px;
}

.litxtleft{
    float:left;
    margin:5px 5px;
    position: absolute;
    top:15px;
    right:60px;
}  */
.tables{
    width: 300px;
    height: 145px;
    float:left;
    table-layout: fixed;
}
.txttd{
    width: 80px;
    height: 10px;
    font-size: 15px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    text-align:center;
    background-color: rgb(58, 234, 247);
}
.lktd{
    width: 80px;
    height: 10px;
    font-size: 15px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    text-align:center;
    border:1px solid rgb(121, 31, 3);
    background-color: rgb(121, 31, 3);
}
a{
    color: black;
    text-decoration: none;
    padding:12px;
    border-radius: 5px;
    font-size: 20px
}
.la{
    color: rgb(228, 243, 11);
    font-weight: bold;
    font-size: 15px;
}
nav{
    background: white;
    margin-bottom: 40px;
    
}

.router-link-active{
    background: rgba(175, 12, 12, 0.8);
    color:white;
}
</style>