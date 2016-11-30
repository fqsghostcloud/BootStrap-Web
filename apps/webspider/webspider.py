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
import re


size = 100000
app = Flask(__name__)
app.config.from_object(config.databaseconfig['videodata'])
db.init_app(app)
elemtsdata = {'title': '', 'img_url': '', 'movie_url': '' }
urls = 'http://www.renren66.com'

# get home page html info
class SpiderHtml(object):

    index_url = 'http://www.renren66.com'

    def __init__(self, url):
        self.url = url

    # remove blank line
    def reblank(self, tag_list):
        new_list = []

        for content in tag_list.contents:
            if content != '\n':
                new_list.append(content)

        return new_list

    # get movie play url from script
    def script_to_url(self, strings):

        reg_strings = '(?<=\|id\|).+(?=\|com\|)'
        play_url = 'http://www.renren66.com/ckplayer/ckplayer.php?id='
        searchobj = re.search(reg_strings, strings, re.M|re.I)
        id = searchobj.group()
        return play_url + id

    # get tr info convert to string type
    def get_tr_string(self, tr_tag):
        strings = ''
        for tr in tr_tag.contents[3].children:
            strings = strings + tr.string

        return strings




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



    # get other html comments return response
    def get_other_html(self, url):

        try:
            res = requests.get(url)
            res.raise_for_status() # trigger Error
            if res.status_code == requests.codes.ok:
                print '****************************'
                print 'The url %s ---response is OK!' % url
                print '****************************'
                return res # html contents
            else:
                print 'response Number is Not 200!'
                return None
        except Exception as HtmlError:
            print 'xxxxxxxxxxxxxxxxxxx--Get-Your-Input-Urls-ERROR--xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            print 'Get url %s --------is Faild! The faild reason is: %s' % (url, HtmlError)





    # get movie_item_tag form html return movie item list type(Tag)
    def get_movie_item(self, contents_response):
        movie_item_list = []

        for chunk in contents_response.iter_content(size):
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


    def get_movie_info(self, movie_item_tag):
        moviedata = {}
        play_url_list = []
        if movie_item_tag:
            moviedata['title'] = movie_item_tag.contents[1].contents[1]['title']
            moviedata['img_url'] = movie_item_tag.contents[1]. contents[1]['src']
            moviedata['movie_url'] = movie_item_tag.contents[1]['href']

            # from movie_url to get detail movie info

            url = 'http://www.renren66.com' + moviedata['movie_url']
            get_detail_info = SpiderHtml(url)
            try:
                res = get_detail_info.get_html()
                if res:
                    # get fast play url
                    previous_play_list = get_detail_info.get__previous_play_urls(res)
                    if previous_play_list:
                        for previous_play in previous_play_list:
                            play_page_res = self.get_other_html(previous_play)
                            play_url = self.get_play_url(play_page_res)
                            play_url_list.append(play_url)

                        moviedata['play_url'] = play_url_list

                        for chunk in res.iter_content(size):
                            # get movie year
                            moviedata['year'] = get_detail_info.get_movie_year(chunk)

                            # get movie tbody info
                            moviedata['tbody_info_dic'] = get_detail_info.get_tbody_info(chunk)

                            # get movie summery
                            moviedata['summary'] = get_detail_info.get_summary_info(chunk)

                            # get movie sreenshot url
                            moviedata['screenshot_url'] = get_detail_info.get_screenshot(chunk)


                        return moviedata
                    else:
                        print u'该电影不支持播放!'

                else:
                    print 'response of get movie other info is None!'
            except Exception as Error:
                print 'get movie detail info Error:%s' % Error



        else:
            print 'movie_item is None'




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




    # get movie info from tbody
    def get_tbody_info(self, chunk):
        moviedata = {}
        try:
            soup = BeautifulSoup(chunk, 'lxml')
            tbody_class = soup.find_all("tbody")
            tbody_tag = tbody_class[0]
            tbody_tag = self.reblank(tbody_tag) # remove blank line in tr list
            # get movie perfor data
            for tr_tag in tbody_tag:
                if tr_tag.contents[1].string == u'主演':
                    #print tr_tag.contents[1].string
                    moviedata['performer'] = self.get_tr_string(tr_tag)
                    #print moviedata['performer']

                elif tr_tag.contents[1].string == u'类型':
                    #print tr_tag.contents[1].string
                    moviedata['type'] = self.get_tr_string(tr_tag)
                    #print moviedata['type']

                elif tr_tag.contents[1].string == u'制片国家':
                    #print tr_tag.contents[1].string
                    moviedata['state'] = self.get_tr_string(tr_tag)
                    #print moviedata['state']

                elif tr_tag.contents[1].string == u'语言':
                    #print tr_tag.contents[1].string
                    moviedata['language'] = self.get_tr_string(tr_tag)
                    #print moviedata['language']

                elif tr_tag.contents[1].string == u'上映时间':
                    #print tr_tag.contents[1].string
                    moviedata['release_time'] = self.get_tr_string(tr_tag)
                    #print moviedata['release_time']

                elif tr_tag.contents[1].string == u'片长':
                    #print tr_tag.contents[1].string
                    moviedata['time_length'] = self.get_tr_string(tr_tag)
                    #print moviedata['time_length']

                elif tr_tag.contents[1].string == u'又名':
                    #print tr_tag.contents[1].string
                    moviedata['another_name'] = self.get_tr_string(tr_tag)
                    #print moviedata['another_name']

                elif tr_tag.contents[1].string == u'评分':
                    #print tr_tag.contents[1].string
                    moviedata['score'] = tr_tag.contents[3].contents[1].contents[0]
                    #print moviedata['score']

                elif tr_tag.contents[1].string == u'imdb':
                    #print tr_tag.contents[1].string
                    moviedata['imdb'] = tr_tag.contents[2].contents[0].string
                    #print moviedata['imdb']

            return moviedata

        except Exception as Error:
            print 'get tbody info Error:%s' % Error

    # get movie summary
    def get_summary_info(self, chunk):
        moviedata = {}
        try:
            soup = BeautifulSoup(chunk, 'lxml')
            tag_class = soup.find_all(class_='summary')
            summary_tag = tag_class[0]
            moviedata['summary'] = summary_tag.string
            return moviedata

        except Exception as Error:
            print 'get movie summary Error:%s' % Error


    # get movie screenshot url
    def get_screenshot(self, chunk):
        moviedata = {}
        screenshot_urls = []
        try:
            soup = BeautifulSoup(chunk, 'lxml')
            screenshot_class = soup.find_all("h4")

            screenshot_previous_tag = screenshot_class[0]

            if screenshot_previous_tag.next_sibling.name == 'img':

                for screenshot_tag in screenshot_previous_tag.next_siblings:
                    screenshot_urls.append(screenshot_tag['src'])
                    moviedata['screenshot'] = screenshot_urls
                return moviedata # use it like moviedata['screenshot'][0]

            else:
                moviedata['screenshot'] = None
                return moviedata





        except Exception as Error:
            print 'get screenshot Error:%s' % Error

    # get movie paly ulrs
    def get__previous_play_urls(self, request):
        previous_url_list = []
        for chunk in request.iter_content(size):
            try:
                soup = BeautifulSoup(chunk, 'lxml')
                previous_url_class = soup.find_all("li",class_='list-group-item')
                if previous_url_class:
                    previous_url_tag = previous_url_class[0]
                    previous_url_list.append(self.index_url + previous_url_tag.contents[0]['href'])
                    previous_url_list.append(self.index_url + previous_url_tag.contents[1]['href'])
                    return previous_url_list
                else:
                    print u'该电影无法播放'

            except Exception as Error:
                print 'get__previous_play_urls Error: %s' % Error








    def get_play_url(self, request):
        try:
            for chunk in request.iter_content(size):
                soup = BeautifulSoup(chunk, 'lxml')
                div_tag = soup.find_all(class_='container-fluid')[0]

                for script in div_tag.contents[3].contents[1].stripped_strings:
                    play_url = self.script_to_url(script)

            return play_url


        except Exception as Error:
            print 'get play url Error:%s' % Error




















'''
test = SpiderHtml('http://www.renren66.com/movie/id_1781.html')
res = test.get_html()
for chunk in res.iter_content(size):
    test.get_screenshot(chunk)
'''




start = SpiderHtml(urls)
res = start.get_html()
movie_tag_list = start.get_movie_item(res)
movie_data = {}

#movie_data = start.get_movie_info(movie_tag_list[4])




for i in movie_tag_list:
    movie_data = start.get_movie_info(i)
    if movie_data:

        print movie_data['title']

        print movie_data['play_url']

        #print movie_data['summary']['summary']

        print movie_data['tbody_info_dic']['performer']
        print movie_data['tbody_info_dic']['language']
        print movie_data['tbody_info_dic']['time_length']
        print movie_data['tbody_info_dic']['state']
        print movie_data['tbody_info_dic']['score']
        print movie_data['tbody_info_dic']['imdb']


        print movie_data['year']

        print movie_data['screenshot_url']['screenshot']

        print movie_data['img_url']
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    else:
        print u'无法播放此电影！'






