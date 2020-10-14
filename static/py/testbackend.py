from flask import Flask, render_template, session, redirect, url_for, request, jsonify, make_response, send_file, send_from_directory
from flask_cors import CORS
import os
import datetime
import time
import string
import random
import json
import pymysql
import requests
from backend import Get_Paper_By_any
r = requests.post(url="http://202.112.113.26:5000/importsid",json={'students':[{'sid':'202020','name':'xql2'}]},headers={'Content-Type': 'application/json;charset=UTF-8'})
print(r)
print(r.json())
# print(Get_Paper_By_any({},status='all'))