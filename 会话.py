#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/10/2814:46
# @NAME:flask/会话
import os
from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)
# app.secret_key = b'12123123-3rdevv_23dvfv#$'
app.secret_key = os.urandom(16)

@app.route("/")
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
    <form method="post">
        <p><input type=text name=username>
        <p><input type=submit value=Login>
    </form>
    '''

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
