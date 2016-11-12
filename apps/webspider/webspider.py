# coding=utf-8
import sys
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
urls = 'http://www.renren66.com/'

class SpiderHtml(object):
    def __init__(self, urls):
        self.urls = urls

        try:
            res = requests.get(urls)
            res.raise_for_status() # trigger Error
            if res.status_code == requests.codes.ok:
                print '****************************'
                print 'The url %s ---response is OK!' % urls
                print '****************************'
            else:
                print 'response Number is Not 200!'

            for chunk in res.iter_content(100000):
                try:
                    soup = BeautifulSoup(chunk, 'lxml')
                    if soup is not None:
                        elems = soup.find_all(class_='movie-item')  # get movie info
                        with app.app_context():
                            for elem in elems:
                                elemtsdata = {'title': '', 'img_url': '', 'movie_url': '' }
                                elemtsdata['title'] = elem.contents[1].contents[1]['title'].encode('gbk')
                                elemtsdata['img_url'] = elem.contents[1].contents[1]['src']
                                elemtsdata['movie_url'] = ''
                                SpiderData.add_spiderdata(elemtsdata)
                            print 'Add info Success!'


                    else:
                        print 'The BeautifulSoup is None!'



                except Exception as AnalysisError:
                    print 'AnalysisHtml Error:%s' % AnalysisError


        except Exception as geturlError:
            print 'xxxxxxxxxxxxxxxxxxx--Get-Urls-ERROR--xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            print 'Get url %s --------is Faild! The faild reason is: %s' % (urls, geturlError)




star = SpiderHtml(urls)



