#!/usr/bin/env python
# coding: utf8

from urllib2 import urlopen, URLError
import sys

# class Parser(object):
#     def __init__(self):
#         pass

#     def get_url(self, url):

URL = 'http://www.meneame.net/'

try:
    html = urlopen(URL).read()
except URLError, e:
    print "ERROR", e

links = []
while True:
    start = html.find('class="comments-counter"')
    if start == -1:
        break
    start_link = html.find('<a href="', start)
    end_link = html.find('"', start_link+9)
    link = html[start_link+9:end_link]
    links.append('http://www.meneame.net'+link)
    html = html[start+1:]
    print 'http://www.meneame.net'+link



def parse_noticia(l):
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


def parse_autors(l):
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

parse_noticia(links)
parse_autors(authors)







