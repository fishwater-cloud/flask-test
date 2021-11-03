#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/11/110:09
# @NAME:flask/auth

import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# 创建名为auth的蓝图， __name__定义蓝图的地方， url_prefix的值会添加到所有与该蓝图关联的URL前面
bp = Blueprint("auth", __name__, url_prefix='/auth')


#  注册
@bp.route("/register", methods=('GET', 'POST'))  # URL：/auth/register
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute("Insert Into user(username, password) values (?,?)",
                           (username, generate_password_hash(password)),
                           )  # 使用？占位符抵御SQL注入攻击
                db.commit()
            except db.IntegrityError:  # 用户已存在
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('auth/register.html')


#  登录
@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'select * from user where username=?', (username,),
        ).fetchone()
        if user is None:
            error = 'Incorrent username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrent username'

        if error is None:
            session.clear()
            session.user_id = user['id']
            return redirect(url_for('blog.index'))
            # return redirect(url_for('auth.index'))
            # 调用的是视图函数名，所以必须有对应函数处理，否则报错werkzeug.routing.BuildError: Could not build url for endpoint

        flash(error)
    return render_template('auth/login.html')


@bp.route("/index", methods=('GET',))
def index():
    return render_template('auth/index.html')


# 如果用户已登录，在应用请求前载入用户信息，以供其他视图使用；
#  g.user持续时间比请求长
@bp.before_app_request
def load_login_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'select * from user where id = ?', (user_id,),
        ).fetchone()


# 注销
@bp.route("/logout")
def logout():
    session.clear()  # 将用户信息从session中移除
    # return redirect(url_for('auth.index'))
    return redirect(url_for('blog.index'))


#  在其他视图中验证用户是否登录的装饰器
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view()
