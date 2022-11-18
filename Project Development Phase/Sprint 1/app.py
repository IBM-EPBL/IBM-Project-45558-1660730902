from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import ibm_db
try:
  conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pxj01049;PWD=gHDRlsYaudgJIF2y",'','')
  print("Successfully connected with db2")
except:
  print("Sorry.. Unable to connect with Database: ", ibm_db.conn_errormsg())

app = Flask(__name__)


# Home page open aagum
@app.route('/')
def home():
  return render_template('login.html')

  
@app.route("/index")
def index():
  return render_template('home.html')
@app.route("/upload")
def upload():
  return render_template('upload.html')

# @app.route('/login')
# def login():
#   return render_template('login.html')

# @app.route('/register')
# def register():
#   return render_template('login.html')
  
# register oda submit action
@app.route('/register',methods = ['POST','GET'])
def register():
  if request.method == 'POST':
    print("--------------------------------")
    name = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['confirmpassword']

    sql = "SELECT * FROM user WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print("********************")
    print(account)
    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO user VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.execute(prep_stmt)
      print("Data Stored")
      sql = "SELECT * FROM user WHERE name = ?"
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt, 1, name)
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      print("$$$$$$$Fetched$$$$$$$$$")
      print(account)
      return render_template('login.html', msg="user Data saved successfuly..")


@app.route('/signin', methods=['POST','GET'])
def signin():
  if request.method == 'POST': 
    name = request.form.get("fullname")
    password = request.form.get("password")

    print("Trying to Login in")
    sql = "SELECT * FROM user WHERE name = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print("$$$$$$$$$$$$$$$$$")
    print(account)
    if not account: 
      return render_template('login.html', msg="You not yet registered")
    else:
      if(password == account['PASSWORD']):
        print("Password Matched")
        return redirect(url_for('index'))
      else:
        return render_template('login.html', msg = "Password Incorrect")

if '__name__' == '__main__' :
  app.run(debug=True)