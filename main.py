from flask import Flask, render_template, request, session, redirect

import function
# from flask_jwt_extended import create_access_token, JWTManger, get_jwt_identity, jwt_required
# import sqlite3, uuid, hashlib, random
from werkzeug.security import generate_password_hash, check_password_hash

from function import *

app = Flask(__name__, template_folder='templates', static_folder='templates/static')

connect = sqlite3.connect('dbase.db', check_same_thread=False)
cursor = connect.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        passw = request.form.get('password')
        user = function.login(login, passw)
    return render_template("login.html")

@app.route('/reg', methods =['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form.get('login')
        passw = request.form.get('password')
        print(login, passw)
        function.reg(login,passw)
    else:
        print('незарегистрирован')

    return render_template("reg.html")
if __name__ == '__main__':
    app.run()
