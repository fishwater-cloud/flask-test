#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/11/114:37
# @NAME:flask/db

import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:  # g是一个特殊对象，独立于每一个请求
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  # current_app是一个特殊对象，指向处理请求的Flask应用
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # 告诉连接，返回类似字典的行
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


#  初始化数据库，执行sql文件用于创建表
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:  # open_resource()打开一个文件，路径相对于flaskr包
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')  # 定义一个名为“init-db“的命令行，调用Init_db()，并显示成功消息
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


# 要使用close_db()和init_db_command()函数，需要在应用实例中注册，但因使用工厂函数__init__.py，导致写函数时无法使用应用实例
# 故做以下函数定义，把应用作为参数，在函数中注册，然后在工厂函数中导入该函数
def init_app(app):
    app.teardown_appcontext(close_db)  # 告诉flask在返回响应后进行清理的时候调用close_db()
    app.cli.add_command(init_db_command)  # 添加一个新的可与flask一起工作的命令

# 初始化数据库执行命令
#  $env:FLASK_APP = "flaskr"
#  $env:FLASK_ENV = "development"
#  flask init-db
