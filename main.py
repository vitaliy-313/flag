import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import flask
from flask import Flask, render_template, request, session, redirect
import os
import hashlib, random
from random import randint, choice
import function
from function import *

app = Flask(__name__, template_folder='templates', static_folder='templates/static')
app.secret_key = os.urandom(30).hex()
app.config['JWT_SECRET_KEY'] = 'super-secret'
connect = sqlite3.connect('dbase.db', check_same_thread=False)
cursor = connect.cursor()

@app.route('/', methods =['GET', 'POST'])
def index():
    err = ''
    accesses = getAccess()
    if request.method == 'POST':
        url = request.form.get('url')
        access = request.form.get('access')
        short_url = request.form.get('short_url')
        if url != None:
            if 'user_id' in session:
                userUrl = searchUserUrl(url, session['user_id'])
                print(searchUserUrl(url, session['user_id']))
                if userUrl == None:
                    if short_url:
                        upUrl(url,  short_url, access, session['user_id'])
                    else:
                        userShortUrl = ''
                        userShortUrl = hashlib.mb5(url.encode()).hexdigest()[:random.randint]
                        upUrl(url,  userShortUrl, access, session['user_id'])
                else:
                    err = 'Эта ссылка сокращалась вами'
            else:
                err = 'Войдите, чтоб сокраить ссылку'
    return render_template("index.html", err = err, accesses = accesses)

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
    session['err'] = ''
    if request.method == 'POST':
        login = request.form.get('login')
        passw = request.form.get('password')
        user = function.reg(login, passw)
        if user != False:
            session['auth'] = True
            session["user_id"] = user[0]
            return redirect("/profile")
    return render_template("reg.html")
@app.route('/profile', methods =['GET', 'POST'])
def profile():
    accesses = getAccess()
    links = getUserUrl(session['user_id'])
    hosthref = request.host_url
    print(hosthref)
    return render_template("profile.html", userUrl=links, accesses=accesses,hosthref=hosthref)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect("/")
@app.route('/edit_access', methods=['POST', 'GET'])
def edit_access():
    if request.method == 'POST':
        url_id = request.form['id']
        type_id = request.form["type"]
        editAccessUrl(type_id, url_id)
        return redirect('/profile')

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        url_id = request.form['id']
        print(url_id)
        editDelete(url_id)
        return redirect('/profile')
@app.route('/edit_short_name', methods=['POST', 'GET'])
def edit_short_name():
    err = ''
    if request.method == 'POST':
        link_id = request.form.get('id')
        short = request.form.get("short_name")
        if short == '':
            host_url = request.host_url
            short_link = host_url + "link/" + ''.join(
                choice(string.ascii_letters + string.digits) for _ in range(randint(8, 12)))
            editShortUrl(short_link, link_id)

            err = "Заполните псевдоним"
        else:
            new_link = request.host_url + "link/" + short
            if getShortUrl(new_link) != None:
                err = "Псевдоним для ссылки занят"
            else:
                editShortUrl(new_link, link_id)
        return redirect('/profile', err = err)


if __name__ == '__main__':
    app.run()
