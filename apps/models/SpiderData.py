# coding=utf-8
import traceback
from flask import current_app
from . import db


class SpiderHtml(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.Unicode(128), index=True)
    img_url = db.Column(db.String(128))
    year = db.Column(db.Integer)
    performer = db.Column(db.String(64))
    type = db.Column(db.String(32))
    state = db.Column(db.String(32))
    language = db.Column(db.String(32))
    release_time = db.Column(db.String(32))
    time_length = db.Column(db.String(32))
    another_name = db.Column(db.String(32))
    score = db.Column(db.Float)
    imdb = db.Column(db.String(64))
    summary = db.Column(db.Text)
    screenshot_url = db.Column(db.String(128))
    play_url = db.Column(db.String(128))
    play_url2 = db.Column(db.String(128))
    pan_url = db.Column(db.String(128))
    pan_url2 = db.Column(db.String(128))
    bt_url = db.Column(db.String(128))
    bt_url2 = db.Column(db.String(128))
    movie_comment = db.Column(db.Text)




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
    if SpiderHtml.query.filter(SpiderHtml.title == title).first():
        return True

def get_count():
    return SpiderHtml.query.count()

def get_by_id(id):
    return SpiderHtml.query.get(id)



# add movie_info by Spider to database
def add_spiderdata(moviedata):
    try:
        has_data = get_by_title(moviedata['title'])
        if has_data:
            return 'The data :%s is existence!' % has_data
        else:
            spiderhtml = SpiderHtml(moviedata['title'])
            spiderhtml.img_url = moviedata['img_url']
            spiderhtml.year = moviedata['year']
            spiderhtml.save()
            print 'add Html-Info Sucess!'

    except Exception as Error:
        print 'The DB_Error is : %s' % Error




 # get movie_info by list to html
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