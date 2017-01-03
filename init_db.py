# coding=utf8
from flask import Flask
from apps.config import databaseconfig
from apps.models import User, SpiderData
from apps.models import db

# debug database must set default encoding as utf8 when you want to read movie_title
'''import sys
reload(sys)
sys.setdefaultencoding('utf-8')'''

if __name__ == "__main__":

    app = Flask(__name__)
    app.config.from_object(databaseconfig['videodata'])
    db.init_app(app)

    with app.app_context():

        db.drop_all()
        db.create_all()
        user = User.User(u'admin')
        user.password = 'admin'
        user.id = '1'
        user.save()
        print 'init db success!'
        '''
        User.User.__table__.create(db.session.bind, checkfirst=True)
        print 'succsess!'
        '''
