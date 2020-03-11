# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 20:39:02 2020

@author: pc
"""
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, make_response, send_file, send_from_directory
from flask_cors import CORS
import os
import time
import string
import json
import pymysql
import django


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '123456'
def Student_Login(data):
    if data[0]=='dzc@ruc.edu.cn' and data[1]=='123456':
        return 2
    else:
        return 0

def Get_Name_By_ID(data):
    return '杜忠朝'

def Get_Group_By_ID(email):
    print('test')
    return [['2017级信息学院本科生',['张腾甘','陈明骏','陶俊屹','朱子恒']],['2018级信息学院本科生',
            ['刘仲杰','张汝洹','张浩琛']],['信息学院党支部',['文继荣','王晓彤','陈红']]]

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


if __name__ == '__main__':
    app.run()