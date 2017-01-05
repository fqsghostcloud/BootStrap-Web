# coding=utf8
from . import main
from datetime import datetime
from flask import render_template, url_for, redirect, request, flash, current_app, session
from flask.ext.login import login_user, login_required, current_user, logout_user
from .forms import LoginForm, RegisterForm, UserConfigForm
from apps.models import User, SpiderData




@main.route('/')
@main.route('/index', methods='GET')
def index():
    if current_user.is_authenticated and session.get('logged_in') is True:
        authenticated = True
    else:
        session['logged_in'] = False
        authenticated = False
    movie_data = SpiderData.get_moviedata()
    # return render_template('index.html', list_data=movie_data, current_time=datetime.utcnow(), authenticated=authenticated)
    return render_template('index.html', list_data=None, current_time=datetime.utcnow(), authenticated=authenticated)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        password = user.verify_password(form.password.data)
        if user is None:
            flash(u'该用户名不存在!')
        elif password is not True:
            flash(u'您的密码错误!')
        else:
            login_user(user, remember=form.remember_me.data)
            session['username'] = request.form['username']
            session['logged_in'] = True
            flash(u'您登录成功!')
            return redirect(url_for('main.user_config'))
    return render_template('login.html', form=form, title=u'欢迎登录')


@main.route('/logout',methods=['GET'])
@login_required
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    logout_user()
    flash(u'您已经注销!')
    return redirect(url_for('main.index'))



@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        info = User.create_user(form)
        if info == 'OK':
            flash(u'您注册成功!')
            return redirect(url_for('main.login'))
        elif info == 'REPRAT':
            flash(u'您注册的用户名已经存在!')
        elif info == 'FAIL':
            flash(u'您注册失败!')
    return render_template('register.html', form=form, title=u'欢迎注册')




@main.route('/user_config', methods=['GET', 'POST'])
@login_required
def user_config():
    form = UserConfigForm(csrf_enabled=False)
    if current_user.is_authenticated and session.get('logged_in') is True:
        return render_template('user_config.html', title=u'个人信息', username=session.get('username'), form=form, authenticated=True)
    else: # 是否通过验证
        return current_app.login_manager.unauthorized()



@main.route('/view')
def view():
    if current_user.is_authenticated and session.get('logged_in') is True:
        authenticated = True
    else:
        authenticated = False
    return render_template('view.html', authenticated=authenticated)







# test------------------------------------------------------------------------------------
@main.route('/download/<path:filename>')

def download(filename):
    from flask import send_from_directory
    import os.path



    dirpath = os.path.join(main.root_path, 'upload')
    return send_from_directory(dirpath, filename, as_attachment=True)


@main.route('/send')
def send_email():
    from apps import mail, Message # must import mail after Blurprint init success!!
    msg = Message('Hello',sender='1178996513@qq.com',recipients=['376141249@qq.com'])
    msg.body = 'testind body'
    msg.html = '<b>HTML</b> body'
    mail.send(msg)
    return '<h1>send email success!</h1>'



