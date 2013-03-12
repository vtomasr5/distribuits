# coding: utf8
from urllib2 import urlopen, URLError

class Crawler():
    def __init(self, url):
        self.url = url
        self.html = self._open_url(url)
    def _open_url(self, url):
        try:
            return urlopen(url).read()
        except URLError, e:
            print "ERROR", e

    def _parse_noticia(l):
        for link in l:
            try:
                noticia = urlopen(link).read()
            except URLError, e:
                print "ERROR", e
            while True:
                start_link = noticia.find('id="cid-')
                if start_link == -1:
                    break
                end_link = noticia.find('</div>', start_link+1)
                print noticia[start_link:end_link]
                noticia = noticia[end_link+1:]
                print "--------------------------------"


    def obtain_news(self,page=1):
        return self._parse_noticia()
