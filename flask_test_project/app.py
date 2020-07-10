import json

from flask import Flask, render_template, request, Response, redirect, url_for

import settings

app = Flask(__name__)

# Flask是一个类，可以查看源码，发现__init__中没有默认值的参数为import_name，这个就是传入的__name__

# print(__name__) ==> __main__

# 首页


@app.route('/', endpoint='index')  # 路由：访问路径
def index():  # 视图函数 MTV：view
    return render_template('index.html')


# 路由的另一种实现方式：add_url_rule()


def index1():
    return 'This is Index'


app.add_url_rule('/index1', view_func=index1)

# 路由的变量规则
data = {'a': '北京', 'b': '上海', 'c': '深圳'}


@app.route('/getcity/<key>')  # key是变量名,默认是字符串类型的
def get_city(key):
    return data.get(key)

# **********************************************************
users = []


# 通过render_template()去直接调用templates文件夹中的HTML界面
@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.method)
    if request.method == 'POST':
        username = request.form.get('username')
        passwords = request.form.get('passwords')
        repasswords = request.form.get('repasswords')
        # 用户名密码一致性验证
        if passwords == repasswords:
            # 保存用户：当前保存到列表中，实际要保存到数据库中
            user = {'username':username, 'passwords':passwords}
            users.append(user)
            return redirect('/')  # 有两次响应：1.给浏览器返回302状态码+location 2.返回location请求地址内容
        else:
            return '两次密码不一致'
    return render_template('register.html')


# 显示已经注册成功的用户名和密码
@app.route('/show')
def show():
    # user[] ----> str json字符串
    j_str = json.dumps(users)
    return j_str


# 进入/register界面输入用户名密码后提交，跳转到/index2,同时获取提交的内容
@app.route('/index2', methods=['GET', 'POST'])
def index2():
    print(request.args)  # 只能获取get请求
    print(request.form)  # 获取post请求
    return 'I LOVE YOU!'
# **********************************************************
# 启动配置
# print(app.config)
# app.config['ENV'] = 'development'  这样写会造成程序冗余，最好是解耦单独写到settings.py文件中
# 通过app.config.form_object()导入配置文件

@app.route('/test')
def test():
    url = url_for('index')
    return 'test'
app.config.from_object(settings)

if __name__ == '__main__':
    print(app.url_map)
    app.run()
