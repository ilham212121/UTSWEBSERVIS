# 19090064 Muhamad Ilham Maulana F S
# 19090141 Abbror Sholakhudin 
# 19090121 Moh Farid Nurul Ikhsani
# 18090037 Solehudin Allah Rezi
from pickle import TRUE
from flask import Flask,request,jsonify
import random, os, string
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import check_password_hash
from sqlalchemy import DATETIME, TIMESTAMP,String

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "uts1.db"))
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class logs(db.Model):
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now ,unique=False,nullable=False, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False, primary_key=False)
    event_name = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    log_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    log_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
class events(db.Model):
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now)
    event_creator = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_name = db.Column(db.String(20), unique=False,nullable=False, primary_key=True)
    event_start_time = db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    event_start_lat= db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_start_lng =db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_end_time = db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    event_finish_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
class users(db.Model):
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now)
    token = db.Column(db.String(20), unique=False,nullable=True, primary_key=False)
    username = db.Column(db.String(20), unique=True,nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
@app.route('/api/v1/users/create/', methods=['POST'])
def register():
    password = request.json['password']
    username = request.json['username']
    user = users(username=username,password=password,token= '')
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg" : "registrasi sukses"}), 200
@app.route('/api/v1/users/login/', methods=['POST'])
def login():
    password = request.json['password']
    username = request.json['username']
    user= users.query.filter_by(username=username).first()
    n=13
    if not user or not check_password_hash(user.password, password):
           tkn = ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))
           user.token= tkn
           db.session.commit()
    return jsonify({"msg": "login sukses","token": tkn,}), 200
@app.route('/api/v1/events/create', methods=['POST'])
def create_event():
    tkn =  request.json['token']
    usr=users.query.filter_by(token=tkn).first()
    event_name = request.json['event_name']
    stime = request.json['event_start_time']
    stimeobj = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S.%f')
    etime = request.json['event_end_time']
    etimeobj = datetime.datetime.strptime(etime, '%Y-%m-%d %H:%M:%S.%f')
    slat = request.json['event_start_lat']
    slng = request.json['event_start_lng']
    flat = request.json['event_finish_lat']
    flng = request.json['event_finish_lng']
    epen = events(event_creator = usr.username,
                    event_name = event_name,
                    event_start_time = stimeobj,
                    event_end_time = etimeobj,
                    event_start_lat = slat,
                    event_start_lng = slng,
                    event_finish_lat = flat,
                    event_finish_lng = flng)
    db.session.add(epen)
    db.session.commit()
    return jsonify({"msg": "membuat event sukses"}), 200

@app.route('/api/v1/logs', methods=['POST'])
def create_logs():
    tkn = request.json['token']
    usr=users.query.filter_by(token=tkn).first()
    log = logs(username = usr.username, event_name = request.json['event_name'],log_lat = request.json['log_lat'], log_lng = request.json['log_lng'])
    db.session.add(log)
    db.session.commit()
    return jsonify({"msg": "Log berhasil dibuat"}), 200

@app.route('/api/v1/users/logs/<token>/<event_name>', methods=['GET'])
def view_logs(token,event_name):
    v= logs.query.filter_by(event_name=event_name).all()
    
    l = []

    for i in v:
        d = {}
        d.update({"username": i.username,"log_lat": i.log_lat, "log_lng": i.log_lng, "create_at": i.created_at})
        l.append(d)
    return jsonify(l), 200
if __name__ == '__main__':
  app.run(debug = True, port=5000)
    
