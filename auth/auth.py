#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/10/2514:42
# @NAME:flask/auth

import time, hashlib, datetime
from functools import partial
from flask import session, abort, current_app, redirect, url_for


DEFAULT_HASH_ALGORITHM = hashlib.sha1
DEFAULT_USER_TIMEOUT = 3600
SESSION_USER_KEY = 'auth_user'
SESSION_LOGIN_KEY = 'auth_login'


def _default_not_authorized(*args, **kwargs):
    return abort(401)  # 终止请求，产生http错误，提供一个带有基本描述的黑白页


def _redirect_to_login(login_url_name):
    return redirect(url_for(login_url_name))  # url_for()用于动态构建指定函数的URL  redirect()用于重定向到目标位置


class Auth(object):
    def __init__(self, app=None, login_url_name=None):
        if login_url_name is None:
            self.not_logged_in_callback = _default_not_authorized
        else:
            self.not_logged_in_callback = partial(_redirect_to_login, login_url_name)  # partial()对原始函数进行封装

        self.not_permitted_callback = _default_not_authorized
        self.hash_algorithm = DEFAULT_HASH_ALGORITHM
        self.user_timeout = DEFAULT_USER_TIMEOUT
        self.load_role = lambda _: None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.auth = self


class AuthUser(object):
    role = None

    def __init__(self, username=None, password=None, salt=None, role=None):
        self.username = username
        self.password = password
        self.salt = salt
        self.role = role

    def set_and_encrypt_password(self, password, salt=str(int(time.time()))):
        self.salt = salt
        self.password = encrypt(password, self.salt)

    def authenticate(self, password):
        """验证密码是否正确"""
        if self.password == encrypt(password, self.salt):
            login(self)
            return True
        return False

    def __eq__(self, other):
        return self.username == getattr(other, 'username', None)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getstate__(self):
        return self.__dict__

    @classmethod  # 类方法，不需要实例化就可以直接调用，cls参数表示自身类
    def load_current_user(cls, apply_timeout=True):
        """获取当前用户信息并加载"""
        data = get_current_user_data(apply_timeout)
        if not data:
            return None
        user = cls()
        user.__dict__ = data  # 对象的__dict__存放着init中的slef.xxx的值；类的__dict__存放着静态函数、类函数、普通函数、全局变量以及一些内置的属性
        return user

    def is_logged_in(self):
        user_data = get_current_user_data()
        return user_data is not None and user_data.get('username') == self.username


def encrypt(password, salt=None, hash_algorithm=None):
    """基于哈希算法加密密码"""
    to_encrypt = password
    if salt is not None:
        to_encrypt += salt
    if hash_algorithm is not None:
        return hash_algorithm(to_encrypt).hexdigest()
    return current_app.auth.hash_algorithm(to_encrypt).hexdigest()


def login(user):
    """用户登录，但不验证用户身份"""
    session[SESSION_USER_KEY] = user.__getstate__()  # 对象序列化
    session[SESSION_LOGIN_KEY] = datetime.datetime.now()  # 当前时间


def logout():
    """注销当前登录用户并返回用户数据"""
    session.pop(SESSION_LOGIN_KEY, None)
    return session.pop(SESSION_USER_KEY, None)


def get_current_user_data(apply_timeout=True):
    user_data = session.get(SESSION_USER_KEY, None)
    if user_data is None:
        return None
    if not apply_timeout:
        return user_data

    login_datetime = session[SESSION_LOGIN_KEY]
    now = datetime.datetime.now()
    user_timeout = current_app.auth.user_timeout
    if user_timeout > 0 and (now - login_datetime) > datetime.timedelta(seconds=user_timeout):
        logout()
        return None
    return user_data


def not_logged_in(callback, *args, **kwargs):
    """执行未登录的回调，非外用"""
    if callback is None:
        return current_app.auth.not_logged_in_callback(*args, **kwargs)
    else:
        return callback(*args, **kwargs)


def login_required(callback=None):
    """登录视图装饰器"""
    def wrap(func):
        def decorator(*args, **kwargs):
            if get_current_user_data() is None:
                return not_logged_in(callback, *args, **kwargs)
            return func(*args, **kwargs)

        return decorator
    return wrap
