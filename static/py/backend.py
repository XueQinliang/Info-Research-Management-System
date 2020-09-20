from flask import Flask, render_template, session, redirect, url_for, request, jsonify, make_response, send_file, \
    send_from_directory
from flask_cors import CORS
import os
import datetime
import time
import string
import random
import json
import pymysql
import pandas as pd

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'T8mT#DS!NVjrR8*ATUUR'
UPLOAD_FOLDER = r'../usrupload/'
ALLOWED_EXTENSIONS = set(
    ['xlsx', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'pptx', 'ppt', 'zip', 'tar', 'rar', '7z'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dbinfo = {
    'host': "202.112.113.26",
    'port': 5412,
    'user': "root",
    'password': "j&ipH9yITl^3Sce8AvsO",
    'database': "irmsdata",
    'charset': "utf8"
}

information = {'1234': '薛钦亮'}


# 生成随机字符串
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# 论文审核状态查询
def Paper_Status(Title, Name):
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = '''
            select Status from Paper_Status
            where P_Title = %s and P_Author = %s
        '''
    data = [Title, Name]
    cursor.execute(sql, data)
    ret = cursor.fetchmany(1)
    return ret[0]['Status']


# 判断后缀名
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 由学号得到学生信息
# 输入一个八位学号，返回一个字符串
def Get_Name_By_ID(data):
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor()
    sql1 = """
    select S_Name from Student where S_ID = %s
    """
    sql2 = """
    select T_Name from Teacher where T_ID = %s
    """
    cursor.execute(sql1, data)
    ret1 = cursor.fetchone()
    cursor.execute(sql2, data)
    ret2 = cursor.fetchone()
    cursor.close()
    conn.close()
    if ret1 != None:
        return ret1[0]
    if ret2 != None:
        return ret2[0]


def Get_Paper_By_any(infodict, status=None):
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor()
    conditionlist = []
    for i in infodict:
        conditionlist.append("Paper." + i + "=" + "\"" + infodict[i] + "\"")
    sql = """
    select Paper.P_Title,Paper.P_Author,Paper.P_ASequence,
    Paper.P_Size,Paper.P_Journal,Paper.P_Meeting,
    Paper.P_Mtime,Paper.P_Otime,Paper.P_Jtime,Paper.P_url from Paper 
    """
    time_position = [-2, -3, -4]
    if status != None:
        time_position = [-3, -4, -5]
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
            sql += (
                'Paper.P_Title = Paper_Status.P_Title and Paper.P_Author = Paper_Status.P_Author and Paper_Status.Status = \'{}\''.format(
                    status))
        elif status == 'all':
            sql += ('Paper.P_Title = Paper_Status.P_Title and Paper.P_Author = Paper_Status.P_Author')
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


# 录入学生信息
# 参数为学生信息
# 格式：[学号，姓名,年级，班级，学生类型]
# 例：data = ['2017201984','朱子恒','大三','17级理科实验班','本科生']
def insert_into_Student(data):
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor()
    sql = """
    insert into Student (S_ID,S_Name,S_Grade,S_Class,S_Level,S_Major) values (%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()


# 录入论文信息
# 参数为论文信息
# 格式：[论文标题，论文作者，作者排序，论文篇幅，发表期刊，发表会议，会议时间，线上时间，期刊时间]
# 例：data = ['论文A','陶云浩','一作','长文','test_J','test_M','2018-10-30','2019-01-01','2019-12-25']
def insert_into_Paper(data):
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor()
    sql = """
    insert into Paper (P_Title,P_Author,P_ASequence,P_Size,P_Journal,P_Meeting,P_Mtime,P_Otime,P_Jtime,P_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()


# 学生登录检测
# 参数为学生用户名和密码，检测是否在数据库中有记录，有记录返回1，否则返回0
# 格式:[用户名，密码]
# 例：data = ['2017201985','123456']
def Student_Login(data):
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = '''
    select * from Student_Login 
    where S_ID = %s and Password = %s
    '''
    cursor.execute(sql1, data)
    ret1 = cursor.fetchmany(1)
    sql2 = '''
    select * from Teacher_Login 
    where T_ID = %s and Password = %s
    '''
    cursor.execute(sql2, data)
    ret2 = cursor.fetchmany(1)
    cursor.close()
    conn.close()
    if ret1 == () and ret2 == ():
        return 0
    elif ret1 != ():
        return 1
    else:
        return 2


# 新增论文状态设为待审核
def New_Paper(Title, Name):
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor()
    sql = '''
        insert into Paper_Status
        values(%s,%s,"待审核")
    '''
    data = [Title, Name]
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()


# 论文信息审核
def Examine_Paper(Title, Name, Status):
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor()
    sql = '''
        update Paper_Status
        set Status = %s
        where P_Title = %s and P_Author = %s
    '''
    data = [Status, Title, Name]
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/', methods=['POST'])
def hello_world():
    temp = json.loads(request.get_data().decode())
    return jsonify(temp)


@app.route('/login', methods=['POST'])
def dologin():
    pwd = request.json.get('password')
    usr = request.json.get('username')
    data = [usr, pwd]
    print(data)
    ret1 = Student_Login(data)
    print("ret:", ret1)
    ret2 = Get_Name_By_ID(usr)
    if not os.path.exists(app.config['UPLOAD_FOLDER'] + usr):
        os.mkdir(app.config['UPLOAD_FOLDER'] + usr)
    return jsonify({'islogin': ret1, 'name': ret2})


@app.route('/revisepswd', methods=['POST'])
def revisepswd():
    uid = request.json.get('uid')
    old = request.json.get('oldpswd')
    new1 = request.json.get('newpswd1')
    new2 = request.json.get('newpswd2')
    if (new1 != new2):
        return jsonify({'status': 2})  # 两次密码不同
    ret1 = Student_Login([uid, old])
    if (ret1 == 1):
        conn = pymysql.connect(
            host="202.112.113.26",
            port=5412,
            user="root",
            password="j&ipH9yITl^3Sce8AvsO",
            database="irmsdata",
            charset="utf8")
        cursor = conn.cursor()
        sql = '''
            update Student_Login
            set Password = %s
            where S_ID = %s and Password = %s
        '''
        data = [new1, uid, old]
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 0})  # 修改成功
    elif (ret1 == 2):
        conn = pymysql.connect(
            host="202.112.113.26",
            port=5412,
            user="root",
            password="j&ipH9yITl^3Sce8AvsO",
            database="irmsdata",
            charset="utf8")
        cursor = conn.cursor()
        sql = '''
            update Teacher_Login
            set Password = %s
            where T_ID = %s and Password = %s
        '''
        data = [new1, uid, old]
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 0})  # 修改成功
    else:
        return jsonify({'status': 1})  # 旧密码错误


@app.route('/islogin', methods=['GET'])
def index():
    # 如果用户名和密码都存在，则跳转到index页面，登录成功
    print("ISLOGIN:", session)
    if 'username' in session and 'password' in session:
        print("pwd:", session['password'], " usr:", session['username'])
        return jsonify({'LOGINSTATUS': 'OK'})
    # 否则，跳转到login页面
    return jsonify({'LOGINSTATUS': 'NOT'})


@app.route('/get_info', methods=['POST'])
def get_info():
    print("Getinfo")
    sid = request.json.get('id')
    print(sid)
    name = Get_Name_By_ID(request.json.get('id'))
    print(sid, name)
    return jsonify({'sid': sid, 'name': name})


@app.route('/upload', methods=['POST'])
def upload():
    """
    提交用户在前端写的论文信息进入数据库（分为第一次提交与被驳回后第n次提交两种情况）
    :param pub_data:json格式的论文信息
    :return:成功返回1，失败返回-1
    """
    # 生成主键并在数据库内部搜索，
    # 1.若找到相同主键，则确认先前存在的论文是否处于被驳回的状态
    # 若是处于被驳回的状态，则执行update函数，并且将该条目的审核状态设置成待审核。在对journal与meeting表插入的过程中若出现重复条目则不插入，若出现新条目则新建
    # 若不是则返回错误，因为 “只有被驳回后才需要用户重新修改”。（注意：此功能设计待完善，因为有可能用户在待审核期间仍旧希望更改申请信息）。
    # 2.若没有找到相同主键，则执行insert函数，并且将该条目的审核状态设置成待审核。在对journal与meeting，student表插入的过程中若出现重复条目则不插入，若出现新条目则新建
    # 在函数的具体实现中没有判断是否处于驳回状态。。。

    # 获取从前端传来的申报信息
    # p.P_Title,p.P_Author,p.P_ASequence,p.P_Size, p.P_Otime,p.P_Journal,p.P_Jtime,j.J_Level,j.J_SName,p.P_Meeting,p.P_Mtime,m.M_Level,m.M_SName,p.P_url
    title = None if request.json.get("title").strip() =="" else request.json.get("title").strip()
    author = None if request.json.get("author").strip() =="" else request.json.get("author").strip()
    sequence = None if request.json.get("sequence").strip() =="" else request.json.get("sequence").strip()
    size = None if request.json.get("size").strip() =="" else request.json.get("size").strip()
    otime = None if request.json.get("otime").strip() =="" else request.json.get("otime").strip()
    journal = None if request.json.get("journal").strip() =="" else request.json.get("journal").strip()
    jtime = None if request.json.get("jtime").strip() =="" else request.json.get("jtime").strip()
    jlevel = None if request.json.get("jlevel").strip() =="" else request.json.get("jlevel").strip()
    jsname = None if request.json.get("jsname").strip() =="" else request.json.get("jsname").strip()
    meeting = None if request.json.get("meeting").strip() =="" else request.json.get("meeting").strip()
    mtime = None if request.json.get("mtime").strip() =="" else request.json.get("mtime").strip()
    mlevel = None if request.json.get("mlevel").strip() =="" else request.json.get("mlevel").strip()
    msname = None if request.json.get("msname").strip() =="" else request.json.get("msname").strip()
    purl = None if request.json.get("purl").strip() =="" else request.json.get("purl").strip()

    # 连接数据库
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    # 创建游标
    cur = conn.cursor()
    # 在paper表中搜索主键
    search_sql_paper = """
            select * from Paper as p 
            where p.P_Title= %s and p.P_Author= %s;
        """
    search_sql_paperstatus = """
            select * from Paper_Status as ps
            where ps.P_Title= %s and ps.P_Author= %s;
        """
    re0 = cur.execute(search_sql_paper, [title, author])
    re1 = cur.execute(search_sql_paperstatus, [title, author])
    if re0 != re1:  # paper与status两个表格内容不一致
        print("出现故障，Paper与Paper_Status表格内容不一致，论文主键为：" + title + " " + author)
        return -1
    else:
        if re0 == 1:  # 已经出现过这篇论文，需要执行update操作
            try:
                # 更新paper表
                # p.P_Title, p.P_Author, p.P_ASequence, p.P_Size, p.P_Otime, p.P_Journal, p.P_Jtime, j.J_Level, j.J_SName, p.P_Meeting, p.P_Mtime, m.M_Level, m.M_SName, p.P_url
                sql_uppaper = """
                        update Paper as p
                        set p.P_ASequence = %s, p.P_Size = %s, 
                        p.P_Journal = %s, p.P_Jtime = %s, p.P_Meeting = %s, p.P_Mtime = %s, p.P_Otime = %s,
                        p.P_url = %s
                        where p.P_Title = %s and p.P_Author = %s ;
                    """
                re_update = cur.execute(sql_uppaper,
                                        [sequence, size, journal, jtime, meeting, mtime, otime, purl, title, author])
                # 更新journal表,meeting表
                # 在杂志表中寻找该杂志是否已经存在
                if journal:
                    sql_fjournal = """
                            select * 
                            from Journal as j
                            where
                            j.J_Name= %s;
                        """
                    re_fjournal = cur.execute(sql_fjournal, [journal])
                    if re_fjournal == 0:  # 没有找到该journal
                        sql_ijournal = """
                                insert into Journal
                                values
                                (%s , %s , %s);
                            """
                        cur.execute(sql_ijournal, [journal, jlevel, jsname])
                    else:
                        pass  # 找到了就不插了
                if meeting:
                    sql_fmeeting = """
                            select * 
                            from Meeting as m
                            where
                            m.M_FName= %s;
                        """
                    re_fmeeting = cur.execute(sql_fmeeting, [meeting])
                    if re_fmeeting == 0:  # 没有找到该meeting
                        sql_imeeting = """
                                insert into Meeting
                                values
                                (%s , %s , %s);
                            """
                        cur.execute(sql_imeeting, [meeting, msname, mlevel])
                    else:
                        pass  # 找到了就不插了

                # 更新paper status表
                sql_uppaperstatus = """
                        update Paper_Status as ps
                        set ps.Status= %s
                        where ps.P_Title =%s and ps.P_Author=%s;
                    """
                cur.execute(sql_uppaperstatus, ["待审核", title, author])

                conn.commit()
                return jsonify({'status': 1, 'content': "执行成功"})
            except Exception as e:
                conn.rollback()
                print("执行sql语句发生错误 update")
                print(e)
                return -1
        if re0 == 0:  # 没找到这篇论文，需要执行插入操作
            try:
                # 插入paper表
                sql_ipaper = """
                        insert into Paper
                        values
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                    """
                cur.execute(sql_ipaper, [title, author, sequence, size, journal, meeting, mtime, otime, jtime, purl])
                # 更新journal表，meeting表
                # 在杂志表中寻找该杂志是否已经存在
                if journal:
                    sql_fjournal = """
                            select * 
                            from Journal as j
                            where
                            j.J_Name= %s;
                        """
                    re_fjournal = cur.execute(sql_fjournal, [journal])
                    if re_fjournal == 0:  # 没有找到该journal
                        sql_ijournal = """
                                insert into Journal
                                values
                                (%s , %s , %s);
                            """
                        cur.execute(sql_ijournal, [journal, jlevel, jsname])
                    else:
                        pass  # 找到了就不插了
                if meeting:
                    sql_fmeeting = """
                            select * 
                            from Meeting as m
                            where
                            m.M_FName= %s;
                        """
                    re_fmeeting = cur.execute(sql_fmeeting, [meeting])
                    if re_fmeeting == 0:  # 没有找到该meeting
                        sql_imeeting = """
                                insert into Meeting
                                values
                                (%s , %s , %s);
                            """
                        cur.execute(sql_imeeting, [meeting, msname, mlevel])
                    else:
                        pass  # 找到了就不插了

                # 插入paper status表
                sql_ipaperstatus = """
                        insert into Paper_Status
                        values
                        (%s,%s,%s);
                    """
                cur.execute(sql_ipaperstatus, [title, author, "待审核"])
                conn.commit()
                return jsonify({'status': 1, 'content': "执行成功"})
            except Exception as e:
                conn.rollback()
                print("执行sql语句发生错误 insert")
                print(e)
                return -1


@app.route('/check_papers', methods=['POST'])
def check_papers():
    value = {}
    name = Get_Name_By_ID(request.json.get('id'))
    value['P_Author'] = name
    ret = Get_Paper_By_any(value)
    print(ret)
    ret_value = []
    for x in ret:
        temp = {'title': x[0], 'author': x[1], 'sequence': x[2]}
        ret_value.append(temp)
    return jsonify(ret_value)


@app.route('/all_papers', methods=['GET'])
def get_all():
    ret = Get_Paper_By_any({}, status='all')
    print(ret)
    ret_value = []
    for x in ret:
        temp = {'title': x[0], 'author': x[1], 'sequence': x[2], 'size': x[3], 'journal': x[4], 'meeting': x[5],
                'P_Mtime': x[6], 'P_Otime': x[7], 'P_Jtime': x[8], 'url': x[9], 'status': x[10]}
        ret_value.append(temp)
    return jsonify(ret_value)


@app.route('/get_detail', methods=['POST'])
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
    value['status'] = Paper_Status(value['title'], value['author'])
    print(value['status'])
    # 获取url
    url = "http://irms.ruc.edu.cn/download/" + ret_value[9]
    save = ret_value[9]
    save = save.split('/')[1][6:]
    return jsonify({"paper": value, 'url': url, 'save': save})


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    print("upload_file")
    if request.method == 'POST':
        file = request.files.get('uploadfile')
        nowid = request.values.get('usr')
        if file and allowed_file(file.filename):
            print('是谁的文件', nowid)
            #            nowtime = datetime.datetime.now()
            randomid = id_generator()
            file.save(app.config['UPLOAD_FOLDER'] + nowid + "/" + randomid + file.filename)
            print(app.config['UPLOAD_FOLDER'] + nowid + "/" + randomid + file.filename)
            return nowid + "/" + randomid + file.filename
    print("ERROR:", file.filename)
    return "fail upload file"


@app.route('/check_pass', methods=['POST'])
def check_pass():
    Examine_Paper(request.json.get('title'), request.json.get('author'), "审核通过")
    return jsonify({'issuccess': 'Success'})


@app.route('/check_notpass', methods=['POST'])
def check_notpass():
    Examine_Paper(request.json.get('title'), request.json.get('author'), "审核不通过")
    return jsonify({'issuccess': 'Success'})


@app.route('/fuzzyjournal', methods=['POST'])
def fuzzyjournal():
    string = request.json.get('string')
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = '''
    select J_Name from Journal 
    where J_Name like '%{}%'
    '''.format(string)
    cursor.execute(sql1)
    ret1 = cursor.fetchmany(10)
    # print(ret1)
    return jsonify(ret1)


@app.route('/fuzzymeeting', methods=['POST'])
def fuzzymeeting():
    string = request.json.get('string')
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = '''
    select M_FName from Meeting 
    where M_FName like '%{}%'
    '''.format(string)
    cursor.execute(sql1)
    ret1 = cursor.fetchmany(10)
    # print(ret1)
    return jsonify(ret1)


@app.route('/filter_papers', methods=['POST'])
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
    ret = Get_Paper_By_any(value, status)
    print(ret)
    ret_value = []
    for x in ret:
        temp = {'title': x[0], 'author': x[1], 'sequence': x[2], 'size': x[3], 'journal': x[4], 'meeting': x[5],
                'P_Mtime': x[6], 'P_Otime': x[7], 'P_Jtime': x[8], 'url': x[9], 'status': x[10]}
        if time == None or temp['P_Mtime'][:4] == time or temp['P_Otime'][:4] == time or temp['P_Jtime'][:4] == time:
            ret_value.append(temp)
    return jsonify(ret_value)


@app.route('/csvdownload', methods=['GET', 'POST'])
def csvdownload():
    """
    根据前端传回的论文的主键搜集论文的所有信息，汇总成一个csv文件
    :return: 返回csv文件的存储路径,若失败返回-1（暂定）
    """
    # 获取主键信息列表(标题+作者名称)
    titles = request.json.get('title')
    authors = request.json.get('author')
    if len(titles) != len(authors):  # 若titlelist与作者list长度不同，则意味着出大问题了
        print("主键出现异常，title列表长度：" + str(len(titles)) + " author列表长度：" + str(len(authors)))
        return -1
    # 连接数据库
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    # 创建游标
    cur = conn.cursor()
    # 根据pubkeys中的论文主键搜索所有的论文信息，存入list中
    pub_datas = []
    # 将所有的字段名放在list中
    col_names = []
    col_ch_names = ["论文标题","论文作者","作者序","论文篇幅","在线发表日期","期刊名称","期刊发表日期","期刊等级","期刊缩写","会议名称","会议发表日期","会议等级","会议缩写"]
    flag = 1
    for i in range(len(titles)):  # 遍历每一个主键
        # 从数据库中筛选需要的条目
        sqls = """
            SELECT 
            p.P_Title,p.P_Author,p.P_ASequence,p.P_Size,
            p.P_Otime,p.P_Journal,p.P_Jtime,j.J_Level,j.J_SName,p.P_Meeting,p.P_Mtime,m.M_Level,m.M_SName
            FROM 
            ( SELECT * FROM Paper WHERE Paper.P_Title = %s AND Paper.P_Author = %s ) p
            LEFT JOIN Journal AS j ON p.P_Journal = j.J_Name
            LEFT JOIN Meeting AS m ON p.P_Meeting = m.M_FName
            LEFT JOIN Paper_Status AS ps ON ps.P_Title = p.P_Title AND ps.P_Author = p.P_Author
            LEFT JOIN Student AS s ON p.P_Author = s.S_Name;
            """
        try:
            re = cur.execute(sqls, [titles[i], authors[i]])
            if re == 0:  # 没有找到该主键对应的论文
                print("找不到该论文，主键：" + titles[i] + " " + authors[i])
                continue  # 跳过该论文
            if re > 1:  # 找到了主键重复的论文
                print("出现论文主键重复，主键：" + titles[i] + " " + authors[i])
                continue  # 跳过改论文
            pub_datas.append(list(cur.fetchone()))
            if flag == 1:  # 只需要提取字段信息一次
                cols_info = cur.description
                for col in cols_info:  # 遍历每一行的信息元组
                    col_names.append(col[0])
                flag = 0
        except Exception as e:
            print("执行sql语句发生错误：" + sqls)
            print(e)
            return -1
    # 将获取的论文信息与字段名称转换成dataframe，再输出成excel文件
    df = pd.DataFrame(pub_datas, columns=col_ch_names)
    out_path = "download/信院学生论文信息汇总.csv"
    df.to_csv("../usrupload/信院学生论文信息汇总.csv", sep=",", index=False, header=True)  # tocsv函数会将重名文件覆盖
    return out_path  # 返回文件路径


@app.route('/getdetailedinfo', methods=['GET', 'POST'])
def getdetailedinfo():
    """
    前端输入论文的主键，返回该论文所有的信息，以帮助用户在修改填报信息时避免重复的填写内容
    :return: json数据，存放所有细节信息，若失败返回-1（暂定）
    """
    # 获取主键信息列表(标题+作者名称)
    title = request.json.get('title')
    author = request.json.get('author')
    if type(title) != type("a") or type(author) != type("a"):  # 若传入的主键类型不是str
        print("主键类型错误，为：" + type(title) + " " + type(author))
        return -1
    # 连接数据库
    conn = pymysql.connect(
        host="202.112.113.26",
        port=5412,
        user="root",
        password="j&ipH9yITl^3Sce8AvsO",
        database="irmsdata",
        charset="utf8")
    # 创建游标
    cur = conn.cursor()
    # 根据主键搜索所有的论文信息，存入list中
    sqls = """
        SELECT 
        p.P_Title,p.P_Author,p.P_ASequence,p.P_Size,
        p.P_Otime,p.P_Journal,p.P_Jtime,j.J_Level,j.J_SName,p.P_Meeting,p.P_Mtime,m.M_Level,m.M_SName,p.P_url
        FROM 
        ( SELECT * FROM paper WHERE paper.P_Title = %s AND paper.P_Author = %s ) p
        LEFT JOIN journal AS j ON p.P_Journal = j.J_Name
        LEFT JOIN meeting AS m ON p.P_Meeting = m.M_FName
        LEFT JOIN paper_status AS ps ON ps.P_Title = p.P_Title AND ps.P_Author = p.P_Author
        LEFT JOIN student AS s ON p.P_Author = s.S_Name;
            """
    try:
        re = cur.execute(sqls, [title, author])
        if re == 0:  # 没有找到到这篇论文
            print("找不到该论文，主键：" + title + " " + author)
            return -1
        if re > 1:  # 找到了多篇主键重复的论文
            print("出现论文主键重复，主键：" + title + " " + author)
            return -1
        pub_data = cur.fetchone().tolist()
        # 将list转成字典再将其json化返回
        # p.P_Title,p.P_Author,p.P_ASequence,p.P_Size,
        # p.P_Otime,p.P_Journal,p.P_Jtime,j.J_Level,j.J_SName,p.P_Meeting,p.P_Mtime,m.M_Level,m.M_SName,p.P_url
        ret_dic = {
            "title": pub_data[0], "author": pub_data[1], "sequence": pub_data[2], "size": pub_data[3],
            "otime": pub_data[4],
            "journal": pub_data[5], "jtime": pub_data[6], "jlevel": pub_data[7], "jsname": pub_data[8],
            "meeting": pub_data[9], "mtime": pub_data[10], "mlevel": pub_data[11], "msname": pub_data[12],
            "url": pub_data[13]
        }
        return jsonify(ret_dic)
    except Exception as e:
        print("执行sql语句发生错误：" + sqls)
        print(e)
        return -1


if __name__ == '__main__':
    # app.run()
    app.run(host='202.112.113.26', port=5000)
