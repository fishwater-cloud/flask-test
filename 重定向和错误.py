#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/10/2814:03
# @NAME:flask/重定向和错误


from flask import abort, redirect, url_for, Flask, render_template, make_response

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    abort(404)
    # this_is_never_executed()
    print("报错啦，后面不再执行了")

@app.errorhandler(404)
def page_not_found(error):
    # return render_template('page_not_found.html'), 404
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

if __name__ == '__main__':
    app.run()
