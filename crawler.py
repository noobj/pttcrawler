#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib2
import time

class Crawler():
    def parser(self, code, keyword="python"):
        for i in code.find_all(class_='r-ent'):
            if keyword in i.a.getText():
                print i.a.getText()

    def start(self):
        for i in xrange(1, 319):
            try:
                page = BeautifulSoup(urllib2.urlopen("https://www.ptt.cc/bbs/CodeJob/index{0}.html".format(i)).read())
            except urllib2.HTTPError, e:
                print "fuck u bitch" + str(e.reason)
                time.sleep(3)
                page = BeautifulSoup(urllib2.urlopen("https://www.ptt.cc/bbs/CodeJob/index{0}.html".format(i)).read())

            self.parser(page, "python") 

if __name__ == '__main__':
    fucker = Crawler()
    fucker.start()
