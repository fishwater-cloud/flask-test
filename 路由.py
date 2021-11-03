#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/10/289:24
# @NAME:flask/路由

from flask import Flask, url_for

app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    return "Index"


@app.route("/login")
def login():
    return "Login"


@app.route("/user/<username>")
def profile(username):
    return f"{username}`s profile"


with app.test_request_context():
    print(url_for("index"))
    print(url_for("login"))
    print(url_for("login", next="/", next2="//"))
    print(url_for("profile", username="alaix"))

if __name__ == '__main__':
    app.run()
