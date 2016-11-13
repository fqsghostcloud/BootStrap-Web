# coding=utf-8
import traceback
from flask import current_app
from . import db


class SpiderHtml(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.Unicode(128), nullable=False, unique=True, index=True)
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

def get_by_id(id):
    return SpiderHtml.query.get(id)



# add movie_info by Spider
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

# get movie_info by list
def get_moviedata():
    count = 13
    movie_info = []
    try:
        check_data = get_count()
        if check_data:
            for id in range(1, count):
                movie_tmp = []
                img_url = get_by_id(id).img_url
                title = get_by_id(id).title
                movie_tmp = [title, img_url]
                movie_info.append(movie_tmp)
            return movie_info
        else:
            return 'movie-info from DB is None!'

    except Exception as Error:
        print 'get movie-info from DB error: %s' % Error