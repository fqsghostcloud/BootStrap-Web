# coding=utf-8
import requests

urls = 'http://www.renren66.com/'

filename = 'spiderhtml.txt'

class SpiderHtml:
    def __init__(self, urls, filename):
        try:
            res = requests.get(urls)
            res.raise_for_status()  # Errors trigger

            if res.status_code == requests.codes.ok:
                print '****************************'
                print 'The url %s ---response is OK!' % urls
                print '****************************'
            else:
                print 'response Number is Not 200!'

                # *******save download html file************
            saveFile = open(filename, 'wb')

            for chunk in res.iter_content(100000):
                saveFile.write(chunk)
            saveFile.close()
            print 'Save HTML Success'
        except Exception as conerro:
            print 'xxxxxxxxxxxxxxxxxxx--ERROR--xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            print 'The url %s --------is Faild! The faild reason is: %s' % (urls, conerro)

spider = SpiderHtml(urls, filename)