# coding = utf8
from flask import Flask
from apps.config import databaseconfig
from apps.models import User
from apps.models import db

if __name__ == "__main__":

    app = Flask(__name__)
    app.config.from_object(databaseconfig['videodata'])
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User.User(u'admin')
        user.password = 'admin'
        user.id = '52695269'
        user.save()
