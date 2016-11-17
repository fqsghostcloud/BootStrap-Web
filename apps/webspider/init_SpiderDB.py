# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
sys.path.append('D:\\BootStrap-code\\BootStrap-Web')
sys.path.append('D:\\BootStrap-code\\BootStrap-Web\\apps')
from apps import config
from apps.models import SpiderData, User
from apps.models import db

app = Flask(__name__)
app.config.from_object(config.databaseconfig['videodata'])
db.init_app(app)
with app.app_context():
    print SpiderData.get_by_title(u'吸血鬼日记 第八季')