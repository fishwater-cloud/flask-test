#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/10/2815:33
# @NAME:flask/闪现消息
import os

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)

app.secret_key = os.urandom(16)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'secret':
            error = "Invalid credentials"
        else:
            flash('You are successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run()
