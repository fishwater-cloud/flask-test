#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/10/2810:25
# @NAME:flask/请求
import os

from flask import Flask, request, flash, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './files/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER   # 文件上传目录
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000   # 限制上传文件尺寸16M


"""实现文件上传功能"""
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash("没有选择文件")
            return redirect(request.url)
        if f and allowed_file(f.filename):
            server_filename = secure_filename(f.filename)
            # f.save(f"./files/uploads/{secure_filename(server_filename)}")
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], server_filename))
            return render_template("upload_file.html", file_names=server_filename)
    return render_template("upload_file.html")


@app.route("/download/<file_name>", methods=['POST'])
def download_file(file_name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], file_name)

if __name__ == '__main__':
    app.run()
