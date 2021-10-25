from flask import Flask
from flask import render_template, request
import qr_code

# Flask实例化
app = Flask(__name__)


@app.route('/')
@app.route('/login')
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    if not all(username, password):
        return "用户名或密码不能为空"





@app.route('/hello')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/qrcode')
def qrcode():
    return render_template('qrcode.html')


@app.route('/make', methods=['GET', 'POST'])
def make_qrcode():
    if request.method == 'GET':
        return 'make'
    # 提取请求内容数据，post请求使用request.form，get请求使用request.args
    http_url = request.form.get('text')  # get函数的key是HTML文件中input标签的name属性值
    img_path = qr_code.make_qrcode(http_url)
    print(img_path)
    return render_template('qrcode_display.html', img_path=img_path)




# 本文将作为执行文件时执行函数，在被其他文件引用时不执行函数
if __name__ == '__main__':
    # app.run()
    app.run(debug=True)  # 打开调试
