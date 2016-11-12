# coding=utf8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys
sys.path.append('D:\\BootStrap-code\\BootStrap-Web')
sys.path.append('D:\\BootStrap-code\\BootStrap-Web\\apps')
from apps import config
from apps.models import SpiderData
from apps.models import db

app = Flask(__name__)
app.config.from_object(config.databaseconfig['videodata'])
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    title = SpiderData.SpiderHtml(u'新建数据库')
    title.id = 1
    title.img_url = 'asdfjlksad'
    title.movie_url = ''
    title.save()
    print 'sucess'