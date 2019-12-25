
<template>
    <div>
        <div class="header">
            <div class="logo">
                <img src='./../assets/top_logo.jpg'>
                <div class="userinfo">
                    <div class="litxtright">
                        <span>{{user.name}}</span><br>
                        <span>{{user.number}}</span>
                    </div>
                    <div class="liimgright">
                        <img src='./../assets/OIP.jpg' height="60px" width="50px">
                    </div>
                </div>
            </div>
        </div>
        <nav>
            <ul>
                <li>
                    <router-link to="/" exact>首页</router-link>
                    <router-link to="/upload-paper" exact>上传论文信息</router-link>
                    <router-link to="/check_order" exact>查看我的论文</router-link>
                </li>                
            </ul>   
        </nav>
           
    </div>
</template>

<script>
    export default{
        name:"blog-header",
        data(){
            return {
                user:{
                    name:"薛钦亮",
                    number:"2017202084"
                }
            }
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
    right:100px;
    height: 70px;
    width: 150px; 
    background: rgb(99, 185, 243);
    border: 1px solid rgb(25, 21, 226)
}
.liimgright{
    float:left;
    margin: 5px 5px;
    /* position: absolute;
    top:15px;
    right:150px; */
}

.litxtright{
    float:right;
    margin:5px 5px;
    /* position: absolute;
    top:15px;
    right:60px; */
} 

a{
    color: black;
    text-decoration: none;
    padding:12px;
    border-radius: 5px;
    font-size: 20px
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