# coding=utf8
from apps import app
from datetime import datetime
from flask import render_template, url_for, redirect, request, flash, current_app, session
from flask.ext.login import login_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from apps.models import User, SpiderData


@app.route('/')
@app.route('/index', methods='GET')
def index():
    movie_data = SpiderData.get_moviedata()

    return render_template('index.html', list_data=movie_data, current_time=datetime.utcnow())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        password = User.check_password(form.password.data)
        if user is None:
            flash(u'该用户名不存在!')
        elif password is not True:
            flash(u'您的密码错误!')
        else:
            login_user(user, remember=form.remember_me.data) # 验证之前需要加入？
            session['name'] = form.username.data
            return redirect(url_for('user_config'))
    return render_template('login.html', form=form, title=u'欢迎登录')




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        info = User.create_user(form)
        if info == 'OK':
            return redirect(url_for('login'))
            flash(u'您注册成功!')
        elif info == 'REPRAT':
            flash(u'您注册的用户名已经存在!')
        elif info == 'FAIL':
            flash(u'您注册失败!')
    return render_template('register.html', form=form, title=u'欢迎注册')




@app.route('/user_config', methods=['GET', 'POST'])
def user_config():
    if not current_user.is_authenticated: # 是否通过验证
        return current_app.login_manager.unauthorized()
    else:
        return render_template('user_config.html', title=u'个人信息', username=session.get('name'))


@app.errorhandler(404)
def page_not_found(e): # 错误页面显示
    return render_template('404.html',title=u'页面不存在'), 404

@app.route('/view')
def view():
    return render_template('view.html')







# test------------------------------------------------------------------------------------
@app.route('/download/<path:filename>')

def download(filename):
    from flask import send_from_directory
    import os.path



    dirpath = os.path.join(app.root_path, 'upload')
    return send_from_directory(dirpath, filename, as_attachment=True)














