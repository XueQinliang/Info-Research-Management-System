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

dbinfo = {
    'host':"202.112.113.26",
    'port':3306,
    'user':"test",
    'password':"123456",
    'database':"irms",
    'charset':"utf8"
}

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
    sql1 = """
    select Get_Name_By_ID(%s)
    """
    sql2 = """
    select Get_Name_By_ID_T(%s)
    """
    cursor.execute(sql1,data)
    ret1 = cursor.fetchone()[0]
    cursor.execute(sql2,data)
    ret2 = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if ret1 != None:
        return ret1
    if ret2 != None:
        return ret2

def Get_Paper_By_any(infodict):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 3306,
            user = "test",
            password = "123456",
            database = "irms",
            charset = "utf8")
    cursor = conn.cursor();
    conditionlist = []
    for i in infodict:
        conditionlist.append(i+"="+"\""+infodict[i]+"\"")
    sql = """
    select * from Paper 
    """ 
    if conditionlist != []:
        sql += ('where ' + ' and '.join(conditionlist))
    print(sql)
    cursor.execute(sql)
    ret = cursor.fetchall()
    ret = list(ret)
    for i in range(len(ret)):
        ret[i] = list(ret[i])
        for j in range(len(ret[i])):
            if ret[i][j] == None:
                ret[i][j] = ''
        for k in [-1,-2,-3]:
            if ret[i][k] != '':
                ret[i][k] = ret[i][k].strftime("%Y-%m-%d")
    cursor.close()
    conn.close()
    return ret

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

#学生登录检测
#参数为学生用户名和密码，检测是否在数据库中有记录，有记录返回1，否则返回0
#格式:[用户名，密码]
#例：data = ['2017201985','123456']
def Student_Login(data):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 3306,
            user = "test",
            password = "123456",
            database = "irms",
            charset = "utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = '''
    select * from Student_Login 
    where S_ID = %s and Password = %s
    '''
    cursor.execute(sql1,data)
    ret1 = cursor.fetchmany(1)
    sql2 = '''
    select * from Teacher_Login 
    where T_ID = %s and Password = %s
    '''
    cursor.execute(sql2,data)
    ret2 = cursor.fetchmany(1)
    cursor.close()
    conn.close()
    if ret1==() and ret2==():
        return 0
    elif ret1!=():
        return 1
    else:
        return 2

@app.route('/',methods = ['POST'])
def hello_world():
    temp = json.loads(request.get_data().decode())
    return jsonify(temp)

@app.route('/login',methods = ['POST'])
def dologin():
    pwd = request.json.get('password')
    usr = request.json.get('username')
    data=[usr,pwd]
    print(data)
    ret1 = Student_Login(data)
    print("ret:",ret1)
    ret2 = Get_Name_By_ID(usr)
    return jsonify({'islogin':ret1,'name':ret2})

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
    print("Getinfo")
    sid = request.json.get('id')
    print(sid)
    name = Get_Name_By_ID(request.json.get('id'))
    print(sid,name)
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
    for i in range(len(value)):
        if value[i] == '':
            value[i] == None
    print(value)
    insert_into_Paper(value)
    return jsonify({'isupload':"OK"})
@app.route('/check_papers',methods = ['POST'])
def check_papers():
    value = {}
    name = Get_Name_By_ID(request.json.get('id'))
    value['P_Author'] = name
    ret = Get_Paper_By_any(value)
    print(ret)
    ret_value = []
    for x in ret:
        temp = {'title':x[0],'author':x[1],'sequence':x[2]}
        ret_value.append(temp)
    return jsonify(ret_value)

@app.route('/all_papers',methods = ['GET'])
def get_all():
    ret = Get_Paper_By_any({})
    print(ret)
    ret_value = []
    for x in ret:
        temp = {'title':x[0],'author':x[1],'sequence':x[2]}
        ret_value.append(temp)
    return jsonify(ret_value)
    
@app.route('/get_detail',methods = ['POST'])
def get_detail():
    value = {}
    value['P_Author'] = request.json.get('author')
    value['P_Title'] = request.json.get('p_title')
    print(value)
    ret = Get_Paper_By_any(value)
    ret_value = ret[0]
    value.clear()
    value['title'] = request.json.get('p_title')
    value['author'] = request.json.get('author')
    value['author_order'] = ret_value[2]
    value['length'] = ret_value[3]
    value['journal_name'] = ret_value[4]
    value['meeting_name'] = ret_value[5]
    value['meeting_time'] = ret_value[6]
    value['online_time'] = ret_value[7]
    value['journal_time'] = ret_value[8]
    
    return jsonify(value)


if __name__ == '__main__':
    app.run()