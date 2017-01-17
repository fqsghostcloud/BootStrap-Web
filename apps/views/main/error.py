# coding=utf8
from . import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found(e): # 错误页面显示
    return render_template('error/404.html', title=u'页面不存在'), 404

@main.app_errorhandler(403)
def page_forbid_visit(e): # 禁止访问
    return render_template('error/403.html', title=u'页面禁止访问'), 403