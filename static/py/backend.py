from flask import Flask, render_template, session, redirect, url_for, request, jsonify, make_response, send_file, send_from_directory
from flask_cors import CORS
import os
import time
import string
import json


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '123456'

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

if __name__ == '__main__':
    app.run()