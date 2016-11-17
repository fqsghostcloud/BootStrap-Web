# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import traceback
import requests
sys.path.append('D:\\BootStrap-code\\BootStrap-Web')
sys.path.append('D:\\BootStrap-code\\BootStrap-Web\\apps')
from bs4 import BeautifulSoup
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from apps.models import SpiderData, db
from apps import config



app = Flask(__name__)
app.config.from_object(config.databaseconfig['videodata'])
db.init_app(app)
elemtsdata = {'title': '', 'img_url': '', 'movie_url': '' }
urls = 'http://www.renren66.com'

# get home page html info
class SpiderHtml(object):

    def __init__(self, url):
        self.url = url

    # get html comments return response
    def get_html(self):

        try:
            res = requests.get(self.url)
            res.raise_for_status() # trigger Error
            if res.status_code == requests.codes.ok:
                print '****************************'
                print 'The url %s ---response is OK!' % self.url
                print '****************************'
                return res # html contents
            else:
                print 'response Number is Not 200!'
                return None
        except Exception as HtmlError:
            print 'xxxxxxxxxxxxxxxxxxx--Get-Urls-ERROR--xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            print 'Get url %s --------is Faild! The faild reason is: %s' % (self.url, HtmlError)


    # get movie_item form html return movie item list
    def get_movie_item(self, contents_response):
        movie_item_list = []

        for chunk in contents_response.iter_content(100000):
            try:
                soup = BeautifulSoup(chunk, 'lxml')
                if soup:
                    movie_item_class = soup.find_all(class_='movie-item') # get movie_item Tag

                    for movie_item in movie_item_class:
                        movie_item_list.append(movie_item)
                else:
                    print 'soup of BeautifulSoup is None!'
            except Exception as Error:
                print 'get movie item error: %s' % Error
        return movie_item_list


    def get_movie_year(self, chunk):
        try:
            soup = BeautifulSoup(chunk, 'lxml')
            movie_year_tag_class = soup.find_all(class_='movie-year')

            for year in movie_year_tag_class:
                year_string = year.string # the movie year like '(2016)'

            movie_year = ''
            for i in year_string:
                if i != '(' and i != ')':
                    movie_year = movie_year + i
            return int(movie_year)
        except Exception as Error:
            print 'BeautifulSoup Error: %s when get movie year' % Error




# get movie info by movie_item
    def get_movie_info(self, movie_item_tag):
        moviedata = {}
        if movie_item_tag:
            for elemt in movie_item_tag:
                moviedata['title'] = elemt.contents[1].contents[1]['title']
                moviedata['img_url'] = elemt.contents[1]. contents[1]['src']
                moviedata['movie_url'] = elemt.contents[1]['href']

            # from movie_url get other movie info
                url = 'http://www.renren66.com' + moviedata['movie_url']
                get_movie_info = SpiderHtml(url)
                try:
                    res = get_movie_info.get_html()
                    if res:
                        for chunk in res.iter_content(100000):
                            moviedata['year'] = get_movie_info.get_movie_year(chunk)

                        with app.app_context():
                            SpiderData.add_spiderdata(moviedata)



                    else:
                        print 'response of get movie other info is None!'
                except Exception as Error:
                    print 'get movie other info Error:%s' % Error

        else:
            print 'movie_item is None'
























start_HtmlSpider = SpiderHtml(urls)
res = start_HtmlSpider.get_html() # res is content of HTML
movie_item_list = start_HtmlSpider.get_movie_item(res)
start_HtmlSpider.get_movie_info(movie_item_list)
