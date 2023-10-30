from flask import Flask, render_template, request, session, redirect
import os
import function
# from flask_jwt_extended import create_access_token, JWTManger, get_jwt_identity, jwt_required
# import sqlite3, uuid, hashlib, random
from werkzeug.security import generate_password_hash, check_password_hash

from function import *

app = Flask(__name__, template_folder='templates', static_folder='templates/static')
app.secret_key = os.urandom(30).hex()
app.config['JWT_SECRET_KEY'] = 'super-secret'
connect = sqlite3.connect('dbase.db', check_same_thread=False)
cursor = connect.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods =['GET', 'POST'])
def login():

    if request.method == 'POST':
        login = request.form.get('login')
        passw = request.form.get('password')
        function.login(login, passw)
        
    return render_template("login.html")

@app.route('/reg', methods =['GET', 'POST'])
def reg():
    session['user_id'] = ""
    if request.method == 'POST':
        login = request.form.get('login')
        passw = request.form.get('password')
        print(login, passw)
        function.reg(login, passw)
        print(session['user_id'])
    else:
        print('незарегистрирован')
    return render_template("reg.html")

if __name__ == '__main__':
    app.run()
