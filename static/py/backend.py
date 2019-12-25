from flask import Flask, render_template, session, redirect, url_for, request, jsonify, make_response, send_file, send_from_directory
from flask_cors import CORS
import os
import time
import string
import json
import pymysql

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '123456'


information = {'1234':'薛钦亮'}



#由学号得到学生信息
#输入一个八位学号，返回一个字符串
def Get_Name_By_ID(data):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 3306,
            user = "test",
            password = "123456",
            database = "irms",
            charset = "utf8")
    cursor = conn.cursor();
    sql = """
    select Get_Name_By_ID(%s)
    """
    cursor.execute(sql,data)
    ret = cursor.fetchone()
    cursor.close()
    conn.close()
    return ret[0]


#录入学生信息
#参数为学生信息
#格式：[学号，姓名。年级，班级，学生类型]
#例：data = ['2017201984','朱子恒','大三','17级理科实验班','本科生']
def insert_into_Student(data):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 3306,
            user = "test",
            password = "123456",
            database = "irms",
            charset = "utf8")
    cursor = conn.cursor()
    sql = """
    call insert_into_Student(%s,%s,%s,%s,%s)
    """
    cursor.execute(sql,data)
    conn.commit()
    cursor.close()
    conn.close()

#录入论文信息
#参数为论文信息
#格式：[论文标题，论文作者，作者排序，论文篇幅，发表期刊，发表会议，会议时间，线上时间，期刊时间]
#例：data = ['论文A','陶云浩','一作','长文','test_J','test_M','2018-10-30','2019-01-01','2019-12-25']
def insert_into_Paper(data):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 3306,
            user = "test",
            password = "123456",
            database = "irms",
            charset = "utf8")
    cursor = conn.cursor()
    sql = """
    call insert_into_Paper(%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(sql,data)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/',methods = ['POST'])
def hello_world():
    temp = json.loads(request.get_data().decode())
    return jsonify(temp)

@app.route('/login',methods = ['POST'])
def dologin():
    global session
    session['password'] = request.json.get('password')
    session['username'] = request.json.get('username')
    print("DOLOGIN:",session)
    return jsonify({'pw':session['password'],'usr':session['username']})

@app.route('/islogin',methods = ['GET'])
def index():
  # 如果用户名和密码都存在，则跳转到index页面，登录成功
  print("ISLOGIN:",session)
  if 'username' in session and 'password' in session:
      print("pwd:",session['password']," usr:",session['username'])
      return jsonify({'LOGINSTATUS':'OK'})
  # 否则，跳转到login页面
  return jsonify({'LOGINSTATUS':'NOT'})

@app.route('/get_info',methods = ['POST'])
def get_info():
    sid = request.json.get('id')
    name = information[sid]
    return jsonify({'sid':sid,'name':name})

@app.route('/upload',methods = ['POST'])
def upload():
    value = []
    #value.append(request.json.get('sid'))
    value.append(request.json.get('title'))
    value.append(request.json.get('author_order'))
    value.append(request.json.get('length'))
    value.append(request.json.get('journal_name'))
    value.append(request.json.get('meeting_name'))
    value.append(request.json.get('meeting_time'))
    value.append(request.json.get('online_time'))
    value.append(request.json.get('journal_time'))
    name = Get_Name_By_ID(request.json.get('sid'))
    value.insert(1,name)
    print(value)
    insert_into_Paper(value)
    return jsonify({'isupload':"OK"})

if __name__ == '__main__':
    app.run()