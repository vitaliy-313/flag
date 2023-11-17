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
# "rus" INTEGER NOT NULL,
# primary key("id" AUTOINCREMENT))''')
# connect.commit()
#
# links_types = [(1, 'public', 'Публичный'), (2, 'all', 'Общий'), (3, 'privat', 'Приватный')]
# acc = cursor.execute(''' SELECT * FROM accesses'''). fetchall()
#
# if (acc == []):
#     for i in links_types:
#
#         cursor.execute(''' INSERT INTO accesses('level', 'rus') VALUES (?,?)''', (i[1],i[2] ))
#         connect.commit()

def getAccess():
    return cursor.execute('''SELECT id, level, rus FROM accesses ''').fetchall()
def searchUserUrl(url, owner_id):
    return cursor.execute('''
    SELECT long
    FROM links
        WHERE long = ? AND owner = ?
    ''',(url, owner_id)).fetchone()
def findUser(login):
    return cursor.execute("SELECT * FROM users where login = ? ", (login,)).fetchone()


def login (login, password):
    cursor.execute('''SELECT login, password
    FROM users WHERE login = ? AND password =?''', (login,password)).fetchone()

def reg (login, password):
    if findUser(login) != None:
        session['err']='выбранное имя занято'
        return False
    else:
        hash = generate_password_hash(password)
        cursor.execute('''INSERT INTO users('login', password) VALUES(?, ?)''', (login,hash))
        connect.commit()
        return cursor.execute('''SELECT * FROM 'users' WHERE login = ?''', (login,)).fetchone()


def upUrl(url, short_url, access_id, owner_id, count = 0):
    cursor.execute('''INSERT INTO
        links(long, short, access_id, count, owner)
        VALUES (?,?,?,?,?)''',(url, short_url, access_id, count, owner_id))
    connect.commit()

def getUserUrl(owner):
    return cursor.execute('''
    SELECT links.id, long, short, count, accesses.rus as type, access_id 
    FROM links INNER JOIN accesses ON access_id = accesses.id WHERE owner = ?
    ''',(owner,)).fetchall()
def editShortUrl(short, url_id):
    cursor.execute('''
    UPDATE links SET short = ?
    WHERE id = ?''',(short, url_id))
    connect.commit()
def getShortUrl(short):
    return cursor.execute('''
    SELECT * FROM links
    WHERE short = ?
    ''',(short,)).fetchall()
def editAccessUrl(type_id, url_id):
    cursor.execute('''
    UPDATE links
    SET access_id = ?
    WHERE id = ?''',(type_id, url_id))
    connect.commit()

def editDelete(url_id):
    cursor.execute('''
    DELETE FROM links
    WHERE id = ?;''',(url_id,))
    connect.commit()