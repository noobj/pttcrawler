#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib2
import time
from functools import wraps
import re
import sys


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry



class Crawler():
    def __init__(self, keyword="python"):
        self.key = keyword

    def parser(self, code, keyword="python"):
        for i in code.find_all(class_='r-ent'):
            if i.a and keyword in i.a.getText():
                print i.a.getText()

    @retry((urllib2.HTTPError, urllib2.URLError), tries=2, delay=2, backoff=1)
    def get_page(self, url):
        return BeautifulSoup(urllib2.urlopen(url).read())

    def get_max_page(self, url):
	result = self.get_page(url)
	href = result.find_all(class_='btn wide')[1].get('href')
	num = re.findall(re.compile(r"\d+"), href)[0]
	return int(num) + 1

    def start(self):
	url = "https://www.ptt.cc/bbs/CodeJob/index.html"
	maxPage = self.get_max_page(url)

        for i in xrange(1, maxPage):
            url = "https://www.ptt.cc/bbs/CodeJob/index{0}.html".format(i)
            page = self.get_page(url)
            self.parser(page, self.key)

if __name__ == '__main__':
    keyword = sys.argv[1]
    fucker = Crawler(keyword)
    fucker.start()
