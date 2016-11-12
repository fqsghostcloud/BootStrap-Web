# coding=utf-8
import traceback
from flask import current_app
from . import db


class SpiderHtml(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False, unique=True, index=True)
    movie_url = db.Column(db.String(128), nullable=False)
    img_url = db.Column(db.String(128), nullable=False)


    def __init__(self, title):
        self.title = title


    def __repr__(self):
        return 'The SpiderDatabbase info is %s' % (self.title)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()


def get_by_title(title):
    return SpiderHtml.query.filter(SpiderHtml.title == title).first()

def get_count():
    return SpiderHtml.query.count()

def add_spiderdata(elemtsdata):
    try:
        has_data = get_by_title(elemtsdata['title'])
        if has_data:
            return 'The data :%s is existence!' % has_data
        else:
            spiderhtml = SpiderHtml(elemtsdata['title'])
            spiderhtml.img_url = elemtsdata['img_url']
            spiderhtml.movie_url = elemtsdata['movie_url']
            spiderhtml.save()
            return 'add Html-Info Sucess!'

    except Exception as Error:
        print 'The DB_Error is : %s' % Error