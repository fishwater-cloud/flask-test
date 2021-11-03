#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/11/110:09
# @NAME:flask/__init__

import os
from flask import Flask


#  定义应用工厂函数
def create_app():
    #  __name__等于python模块名
    #  instance_relative_config告诉应用配置文件存在于实例文件夹的相对路径
    app = Flask(__name__, instance_relative_config=True)

    # E:\python\flask\instance
    # print("app.instance_path:%s" % app.instance_path)

    #  设置一个应用的缺省配置
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # if test_config is None:
    #     #  使用config.py中的值来重载缺省配置
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     app.config.from_mapping(test_config)

    # 确定实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # hello实例
    @app.route("/hello")
    def hello():
        return "Hello World!"

    #  初始化数据库
    from . import db
    db.init_app(app)

    #  在工厂函数中导入和注册认证蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    # 在工厂函数中导入和注册博客蓝图
    from . import blog
    app.register_blueprint(blog.bp)  # index视图的端点会被定义为blog.index，但是验证视图指向的是普通的index端点
    app.add_url_rule('/', endpoint='index')  # 关联端点名称index和/URL，使得url_for('index')或url_for('blog.index')都有效，生成同样的/URL

    return app
