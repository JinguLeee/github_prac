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
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return render_template('index.html')
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            print(payload)
            return render_template('index.html', user_name=payload["user_name"], user_id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

SECRET_KEY = 'SPARTA'
@app.route('/login', methods=["POST"])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    if id_receive == "":
        return jsonify({'result': 'fail', 'msg': '아이디를 입력해주세요.', 'cur':'id'})
    elif pw_receive == "":
        return jsonify({'result': 'fail', 'msg': '비밀번호를 입력해주세요.', 'cur':'pw'})

    user_name = db.users.find_one({"user_id": id_receive})['user_name']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'user_id': id_receive, 'user_pw': pw_hash})
    print(result)

    if result is not None:
        payload = {
            'user_id': id_receive,
            'user_name': user_name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=500)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
