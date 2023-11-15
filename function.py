import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import flask
from flask import Flask, render_template, request, session, redirect
import os
app = Flask(__name__, template_folder='templates', static_folder='templates/static')
app.secret_key = os.urandom(30).hex()
app.config['JWT_SECRET_KEY'] = 'super-secret'
connect = sqlite3.connect('dbase.db', check_same_thread=False)
cursor = connect.cursor()

# resull = cursor.execute('''
# CREATE TABLE IF NOT EXISTS
# "users"
# ("id" INTEGER NOT NULL,
# "login" INTEGER NOT NULL,
# "password" INTEGER NOT NULL,
# primary key("id" AUTOINCREMENT))''')
#
# resull = cursor.execute('''
# CREATE TABLE IF NOT EXISTS
# "links"
# ("id" INTEGER NOT NULL,
# "long" TEXT NOT NULL,
# "short" TEXT,
# "access_id" INTEGER NOT NULL,
# "count" TEXT NOT NULL,
# "owner" INTEGER NOT NULL,
# primary key("id" AUTOINCREMENT),
# FOREIGN KEY("owner") REFERENCES "users"("id"),
# FOREIGN KEY("access_id") REFERENCES "accesses"("id"))''')
#
# resull = cursor.execute('''
# CREATE TABLE IF NOT EXISTS
# "accesses"
# ("id" INTEGER NOT NULL,
# "level" INTEGER NOT NULL,
# primary key("id" AUTOINCREMENT))''')
# connect.commit()
#
# links_types = [(1, 'public'), (2, 'all'), (3, 'privat')]
# acc = cursor.execute(''' SELECT * FROM accesses'''). fetchall()
#
# if (acc == []):
#     for i in links_types:
#         cursor.execute(''' INSERT INTO accesses('level') VALUES (?)''', (i[1], ))
#         connect.commit()

def searchUserUrl(url, owner_id):
    return cursor.execute('''
    SELECT long
    FROM links
    WHERE long = ? AND owner_id = ?''',(url, owner_id)).fetchall()
def findUser(login):
    return cursor.execute("SELECT * FROM users where login = ? ", (login,)).fetchone()


def login (login, password):
    cursor.execute('''SELECT login, password
    FROM users WHERE login = ? AND password =?''', (login,password)).fetchone()

def reg (login, password):
    user_id = login
    cursor.execute('''SELECT * FROM users WHERE login = ?''', (user_id,)).fetchone()
    user_n = cursor.fetchone()

    if (login == '' or password == ''):
        flask.flash('для регистрации заполните все поля')
        return redirect('/reg', code=302)
    else:
        if user_n != None:
            flask.flash('выбранное имя занято')
            return redirect('/reg', code=302)
        else:
            hash = generate_password_hash(password)
            cursor.execute('''INSERT INTO users('login', password) VALUES(?, ?)''', (login,hash))
            connect.commit()
            user = cursor.execute('''SELECT * FROM 'users' WHERE login = ?''', (login,)).fetchone()
            session['user_id'] = user[0]
            return redirect('/profile', code=302)


def upUrl(url, short_url, access_id, owner_id, count = 0):
    cursor.execute('''INSERT INTO
        links (long, short, access_id, count, owner_id)
        VALUES (?,?,?,?,?)'''),(url, short_url, access_id, count, owner_id)
    connect.commit()

def getUserUrl(owner):
    cursor.execute('''
    SELECT long, short, count
    FROM links
    WHERE owner = ?
    ''',(owner,)).fetchall()