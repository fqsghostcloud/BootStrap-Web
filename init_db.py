# coding=utf8
from flask import Flask
from apps.config import databaseconfig
from apps.models import User, Role, Comment
from apps.models.Role import Permission
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

        # init Role inser_roles()
        Role.Role.insert_roles() # init rloe database

        user = User.User(u'admin')
        user.password = 'admin'
        user.user_id = '52695269'
        user.role_id = Role.Role.query.filter(Role.Role.permissions == 0xff).first().id
        #user.confirmed = True
        user.save()
        print 'init db success!'



        '''
        User.User.__table__.create(db.session.bind, checkfirst=True)
        print 'succsess!'
        '''
