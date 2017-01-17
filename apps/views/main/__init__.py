# coding=utf8
from flask import Blueprint
from apps.models.Role import Permission

main = Blueprint('main', __name__)  # add Flask-Blueprint


@main.app_context_processor # app_context处理器，添加Permission到上下文。
def inject_permissions():
    return dict(permission=Permission)


from . import views, forms, error