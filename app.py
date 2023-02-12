from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)
import hashlib
import datetime
# 설치
import jwt

from bson import ObjectId

app = Flask(__name__)

## certifi 맥OS 환경설정을 위한 패키지 설치입니다.
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient("mongodb+srv://test:sparta@cluster0.exrmfp9.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.team6

@app.route('/')
def home():
    return render_template('index.html')