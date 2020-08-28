from flask import Flask, render_template, session, redirect, url_for, request, jsonify, make_response, send_file, send_from_directory
from flask_cors import CORS
import os
import datetime
import time
import string
import random
import json
import pymysql

app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config['SECRET_KEY'] = 'T8mT#DS!NVjrR8*ATUUR'
UPLOAD_FOLDER = r'../usrupload/'
ALLOWED_EXTENSIONS = set(['xlsx','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc','docx','pptx','ppt','zip','tar','rar','7z'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


dbinfo = {
    'host':"202.112.113.26",
    'port':5412,
    'user':"root",
    'password':"j&ipH9yITl^3Sce8AvsO",
    'database':"irmsdata",
    'charset':"utf8"
}


information = {'1234':'薛钦亮'}

#生成随机字符串
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#论文审核状态查询
def Paper_Status(Title,Name):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)   
    sql = '''
            select Status from Paper_Status
            where P_Title = %s and P_Author = %s
        '''
    data = [Title,Name]
    cursor.execute(sql,data)
    ret = cursor.fetchmany(1)
    return ret[0]['Status']

#判断后缀名
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#由学号得到学生信息
#输入一个八位学号，返回一个字符串
def Get_Name_By_ID(data):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor()
    sql1 = """
    select S_Name from Student where S_ID = %s
    """
    sql2 = """
    select T_Name from Teacher where T_ID = %s
    """
    cursor.execute(sql1,data)
    ret1 = cursor.fetchone()
    cursor.execute(sql2,data)
    ret2 = cursor.fetchone()
    cursor.close()
    conn.close()
    if ret1 != None:
        return ret1[0]
    if ret2 != None:
        return ret2[0]

def Get_Paper_By_any(infodict,status=None):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor()
    conditionlist = []
    for i in infodict:
        conditionlist.append("Paper."+i+"="+"\""+infodict[i]+"\"")
    sql = """
    select Paper.P_Title,Paper.P_Author,Paper.P_ASequence,
    Paper.P_Size,Paper.P_Journal,Paper.P_Meeting,
    Paper.P_Mtime,Paper.P_Otime,Paper.P_Jtime,Paper.P_url from Paper 
    """ 
    time_position = [-2,-3,-4]
    if status != None:
        time_position = [-3,-4,-5]
        sql = """
        select Paper.P_Title,Paper.P_Author,Paper.P_ASequence,
        Paper.P_Size,Paper.P_Journal,Paper.P_Meeting,
        Paper.P_Mtime,Paper.P_Otime,Paper.P_Jtime,Paper.P_url,Paper_Status.status from Paper 
        inner join Paper_Status
        """ 
    if conditionlist != []:
        sql += ('where ' + ' and '.join(conditionlist))
    elif status != None:
        sql += 'where ' 
    if status != None:
        if conditionlist != []:
            sql += 'and '
        if status != 'all':
            sql += ( 'Paper.P_Title = Paper_Status.P_Title and Paper.P_Author = Paper_Status.P_Author and Paper_Status.Status = \'{}\''.format(status) )
        elif status == 'all':
            sql += ( 'Paper.P_Title = Paper_Status.P_Title and Paper.P_Author = Paper_Status.P_Author')
    print(sql)
    cursor.execute(sql)
    ret = cursor.fetchall()
    ret = list(ret)
    print(ret)
    for i in range(len(ret)):
        ret[i] = list(ret[i])
        for j in range(len(ret[i])):
            if ret[i][j] == None:
                ret[i][j] = ''
        for k in time_position:
            if ret[i][k] != '':
                print(ret[i][k])
                ret[i][k] = ret[i][k].strftime("%Y-%m-%d")
    cursor.close()
    conn.close()
    return ret

#录入学生信息
#参数为学生信息
#格式：[学号，姓名,年级，班级，学生类型]
#例：data = ['2017201984','朱子恒','大三','17级理科实验班','本科生']
def insert_into_Student(data):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor()
    sql = """
    insert into Student (S_ID,S_Name,S_Grade,S_Class,S_Level,S_Major) values (%s,%s,%s,%s,%s,%s)
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
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor()
    sql = """
    insert into Paper (P_Title,P_Author,P_ASequence,P_Size,P_Journal,P_Meeting,P_Mtime,P_Otime,P_Jtime,P_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
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

#新增论文状态设为待审核
def New_Paper(Title,Name):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor()
    sql='''
        insert into Paper_Status
        values(%s,%s,"待审核")
    '''
    data =[Title,Name]
    cursor.execute(sql,data)
    conn.commit()
    cursor.close()
    conn.close()
    
#论文信息审核
def Examine_Paper(Title,Name,Status):
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor()
    sql='''
        update Paper_Status
        set Status = %s
        where P_Title = %s and P_Author = %s
    '''
    data =[Status,Title,Name]
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
    pwd = request.json.get('password')
    usr = request.json.get('username')
    data=[usr,pwd]
    print(data)
    ret1 = Student_Login(data)
    print("ret:",ret1)
    ret2 = Get_Name_By_ID(usr)
    if not os.path.exists(app.config['UPLOAD_FOLDER']+usr):
        os.mkdir(app.config['UPLOAD_FOLDER']+usr)
    return jsonify({'islogin':ret1,'name':ret2})

@app.route('/revisepswd',methods=['POST'])
def revisepswd():
    uid = request.json.get('uid')
    old = request.json.get('oldpswd')
    new1 = request.json.get('newpswd1')
    new2 = request.json.get('newpswd2')
    if(new1 != new2):
        return jsonify({'status':2}) #两次密码不同
    ret1 = Student_Login([uid,old])
    if(ret1==1):
        conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
        cursor = conn.cursor()
        sql='''
            update Student_Login
            set Password = %s
            where S_ID = %s and Password = %s
        '''
        data =[new1,uid,old]
        cursor.execute(sql,data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status':0}) #修改成功
    elif(ret1==2):
        conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
        cursor = conn.cursor()
        sql='''
            update Teacher_Login
            set Password = %s
            where T_ID = %s and Password = %s
        '''
        data =[new1,uid,old]
        cursor.execute(sql,data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status':0}) #修改成功
    else:
        return jsonify({'status':1}) #旧密码错误
    
    

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
    value.append(request.json.get('url'))
    name = Get_Name_By_ID(request.json.get('sid'))
    value.insert(1,name)
    for i in range(len(value)):
        if value[i] == '':
            value[i] = None
    print(value)
    insert_into_Paper(value)
    New_Paper(request.json.get('title'),name)
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
    ret = Get_Paper_By_any({},status='all')
    print(ret)
    ret_value = []
    for x in ret:
        temp = {'title':x[0],'author':x[1],'sequence':x[2],'size':x[3],'journal':x[4],'meeting':x[5],'P_Mtime':x[6],'P_Otime':x[7],'P_Jtime':x[8],'url':x[9],'status':x[10]}
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
    value['status'] = Paper_Status(value['title'],value['author'])
    print(value['status'])
    #获取url
    url = "http://irms.ruc.edu.cn/download/"+ret_value[9]
    save = ret_value[9]
    save = save.split('/')[1][6:]
    return jsonify({"paper":value,'url':url,'save':save})

@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    print("upload_file")
    if request.method=='POST': 
        file=request.files.get('uploadfile')
        nowid = request.values.get('usr')
        if file and allowed_file(file.filename):
            print('是谁的文件',nowid)
#            nowtime = datetime.datetime.now()
            randomid = id_generator()
            file.save(app.config['UPLOAD_FOLDER'] + nowid+"/"+randomid+file.filename)
            print(app.config['UPLOAD_FOLDER'] + nowid+"/"+randomid+file.filename)
            return nowid+"/"+randomid+file.filename
    print("ERROR:",file.filename)
    return "fail upload file"

@app.route('/check_pass',methods=['POST'])
def check_pass():
    Examine_Paper(request.json.get('title'),request.json.get('author'),"审核通过")
    return jsonify({'issuccess':'Success'})

@app.route('/check_notpass',methods=['POST'])
def check_notpass():
    Examine_Paper(request.json.get('title'),request.json.get('author'),"审核不通过")
    return jsonify({'issuccess':'Success'})

@app.route('/fuzzyjournal',methods=['POST'])
def fuzzyjournal():
    string = request.json.get('string')
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = '''
    select J_Name from Journal 
    where J_Name like '%{}%'
    '''.format(string)
    cursor.execute(sql1)
    ret1 = cursor.fetchmany(10)
    #print(ret1)
    return jsonify(ret1)

@app.route('/fuzzymeeting',methods=['POST'])
def fuzzymeeting():
    string = request.json.get('string')
    conn = pymysql.connect(
            host = "202.112.113.26",
            port= 5412,
            user = "root",
            password = "j&ipH9yITl^3Sce8AvsO",
            database = "irmsdata",
            charset = "utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = '''
    select M_FName from Meeting 
    where M_FName like '%{}%'
    '''.format(string)
    cursor.execute(sql1)
    ret1 = cursor.fetchmany(10)
    #print(ret1)
    return jsonify(ret1)

@app.route('/filter_papers',methods=['POST'])
def filter_papers():
    author = request.json.get('author')
    journal = request.json.get('journal')
    meeting = request.json.get('meeting')
    sequence = request.json.get('sequence')
    size = request.json.get('size')
    status = request.json.get('status')
    if status == None:
        status = 'all'
    time = request.json.get('time')
    value = {}
    if author != None:
        value['P_Author'] = author
    if journal != None:
        value['P_Journal'] = journal
    if meeting != None:
        value['P_Meeting'] = meeting
    if sequence != None:
        value['P_ASequence'] = sequence
    if size != None:
        value['P_Size'] = size
    ret = Get_Paper_By_any(value,status)
    print(ret)
    ret_value = []
    for x in ret:
        temp = {'title':x[0],'author':x[1],'sequence':x[2],'size':x[3],'journal':x[4],'meeting':x[5],'P_Mtime':x[6],'P_Otime':x[7],'P_Jtime':x[8],'url':x[9],'status':x[10]}
        if time == None or temp['P_Mtime'][:4] == time or temp['P_Otime'][:4] == time or temp['P_Jtime'][:4] == time:
            ret_value.append(temp)
    return jsonify(ret_value)

if __name__ == '__main__':
    #app.run()
    app.run(host='202.112.113.26',port=5000)
