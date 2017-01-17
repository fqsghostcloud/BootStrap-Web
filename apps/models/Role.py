# coding=utf8
import traceback
from . import db
from flask import current_app



class Permission:
    COMMENT = 0x01
    HELP_ADMIN = 0x02
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %s>' % self.name



    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.COMMENT, True),
            'Moderator':(Permission.COMMENT|Permission.HELP_ADMIN, False),
            'Administer':(Permission.ADMINISTER, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


















