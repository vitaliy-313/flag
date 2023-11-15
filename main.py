import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import flask
from flask import Flask, render_template, request, session, redirect
import os
import hashlib, random
import function
from function import *

app = Flask(__name__, template_folder='templates', static_folder='templates/static')
app.secret_key = os.urandom(30).hex()
app.config['JWT_SECRET_KEY'] = 'super-secret'
connect = sqlite3.connect('dbase.db', check_same_thread=False)
cursor = connect.cursor()

@app.route('/', methods =['GET', 'POST'])
def index():
    print(session["auth"])
    if request.method == 'POST':
        err = ''
        url = request.form.get('url')
        access = request.form.get('access')
        short_url = request.form.get('short_url')
        if url != None:
            if 'user_id' in session:
                userUrl =  searchUserUrl(url, session['user_id'])
                print(searchUserUrl(url, session['user_id']))
                if len(userUrl) == 0:
                    if short_url:
                        upUrl(url,  short_url, access, session['user_id'])
                    else:
                        err = 'Ссылка уже используется'
                else:
                    userShortUrl = ''
                    userShortUrl = hashlib.mb5(url.encode()).hexdigest()[:random.randint]
                    upUrl(url,  userShortUrl, access, session['user_id'])
            else:
                err = 'Эта ссылка сокращалась вами'
        else:
            err = 'Войдите, чтоб сокраить ссылку'
    return render_template("index.html")

@app.route('/login', methods =['GET', 'POST'])
def log():
    err=""
    if request.method == 'POST':
        loginUser = request.form.get('login')
        passw = request.form.get('password')
        user = findUser(loginUser)
        if user != None:
            if check_password_hash(user[2], passw):
                session['user_id'] = user[0]
                session['auth'] = True
                return redirect('profile')
            else:
                err = 'Пароль не верный'
        else:
            err = 'Пользователь не найден'
    return render_template("login.html", err=err)

@app.route('/reg', methods =['GET', 'POST'])
def reg():
    session['user_id'] = None
    if request.method == 'POST':
        login = request.form.get('login')
        passw = request.form.get('password')
        function.reg(login, passw)
    return render_template("reg.html")
@app.route('/profile', methods =['GET', 'POST'])
def profile():
    userUrl = getUserUrl(session['user_id'])
    return render_template("profile.html", userUrl=userUrl)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['user_id'] = None
    session['all'] = None
    return redirect("/")


if __name__ == '__main__':
    app.run()
