# Info-Research-Management-System
该项目为中国人民大学信息学院科研管理系统<br/>
最终功能包含学生上传、修改、查看，老师审批、修改、查看、统计等功能，旨在方便师生，鼓励科研。
## 项目架构
vue.js + flask + mysql<br>
**src/** vue主要的代码和用到的图片等<br>
**static/** js,py代码，以及用户提交的文件的物理存放地址
## 运行环境
- Ubuntu 16.04.6
- python3.5
- Flask1.1.1
- npm6.13.4
## 服务器端运行方式
1. git clone https://github.com/XueQinliang/Info-Research-Management-System.git
2. cd Info-Research-Management-System
3. sudo npm install
这一步之后应该会出现node_modules文件夹<br>
已知这一步可能会发生错误，需要sudo npm install flyio可以修复<br>
4. sudo npm run build
这一步之后可以生成dist文件夹，内部包含生成的前端代码
5. 删除~/tools/apache-tomcat-8.0.24/webapps/ROOT文件夹的一切内容
6. 复制dist到~/tools/apache-tomcat-8.0.24/webapps/ROOT
7. 进入ROOT文件夹，建立软连接：ln -s ~/Info-Research-Management-System/static/usrupload download，将服务器的路径映射为真实的物理路径
8. 到~/目录下，sudo bash shutdown.sh，再sudo bash startup.sh<br>
这两个均为建立的软链接，真实位置在~/tools/apache-tomcat-8.0.24/bin下，sudo的原因是启动端口为80，1024以下端口均需要sudo权限
9. screen -r runpy，然后到~/Info-Research-Management-System/static/py/下，启动backend.py，运行后台程序
10. 打开浏览器，输入202.112.113.26或者绑定的域名：irms.ruc.edu.cn，即可打开网页
## 本地运行方式
前三步同服务器端<br>第四步命令为npm run build，推荐使用visual studio<br>第五步为启动python后台程序<br>第六步为打开localhost:8080。
## 注意事项
服务器端如果发现端口号问题，需要查看两个地方。
1. ~/Info-Research-Management-System/src/components/Global.vue中URL是否为http://202.112.113.26:5000/
2. ~/Info-Research-Management-System/static/py/backend.py中app.run中参数是否为(host='202.112.113.26',port=5000)
## 未来工作
- 进一步考虑存储及增删改查的需要，编写相关的函数及存储过程
- 为学生用户建立模糊匹配引擎，帮助用户更好录入会议及期刊信息
- 学生论文信息驳回之后修改
- 为教师用户建立完善的筛选及统计功能
- 用户个人信息的填写及修改
- 完成科研信息统计表的导出
- 美化前端界面，完善前端逻辑
- 系统试运行及维护……
## 团队成员
薛钦亮 陶俊屹 陈冠华 朱子恒 陶云浩<br>
如有任何反馈，联系邮箱：**2017202084@ruc.edu.cn**
