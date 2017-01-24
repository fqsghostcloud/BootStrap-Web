# coding=utf8
from . import main
from datetime import datetime
from flask import render_template, url_for, redirect, request, flash, current_app, session, abort
from flask.ext.login import login_user, login_required, current_user, logout_user
from .forms import LoginForm, RegisterForm, UserConfigForm, EditProfileAdminForm
from apps.models import User, SpiderData
from apps.views.decorators import admin_required, permission_required # 自定义修饰器
from apps.models.Role import Permission, Role
from apps.models import db




@main.before_app_request
def before_app_request():
    if current_user.is_authenticated:
        current_user.ping()
        '''
        if not current_user.confirmed \
        and request.endpoint[:5] != 'main'
        return redirect(url_for('main.unconfirmed'))
        '''







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
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.sex = form.sex.data
        db.session.add(current_user)
        return render_template('user.html', authenticated=True)
    form.username.data = current_user.username
    form.sex.data = current_user.sex
    if current_user.email is None:
        form.email.data = None
    else:
        form.email.data = current_user.email

    return render_template('user_config.html', title=u'个人信息', form=form, authenticated=True)







@main.route('/user/<username>', methods=['GET'])
def user(username):
    user = User.get_by_username(username)
    if user is None:
        abort(404)
    return render_template('user.html')




@main.route('/view')
def view():
    if current_user.is_authenticated and session.get('logged_in') is True:
        authenticated = True
    else:
        authenticated = False
    return render_template('view.html', authenticated=authenticated)


@main.route('/admin')
@login_required
@admin_required
def admin_config():
    return '<h1>Hello admin!</h1>'



@main.route('/admin/edit_user/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_user(id):
    user = User.User.query.get_or_404(id)
    form = EditProfileAdminForm(user, csrf_enabled=False)
    if form.validate_on_submit():
        if form.validate_username(form.username):
            user.username = form.username.data
        elif form.validate_email(form.email):
            if form.email.data is None:
                user.email = None
            else:
                user.email = form.email.data
        user.sex = form.sex.data
        user.role_id = form.role.data
        db.session.add(user)
        flash(u'用户信息修改成功!')
        return render_template('edit_user.html', form=form, authenticated=True)
    form.username.data = user.username
    form.email.data = user.email
    form.sex.data = user.sex
    form.role.data = user.role_id
    return render_template('edit_user.html',form=form, user=user,  authenticated=True)







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



