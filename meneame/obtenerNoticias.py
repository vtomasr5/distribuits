# -*- coding: utf-8 -*-
from urllib2 import urlopen, URLError, HTTPError
import re
import httplib
from properties import MENEAME_BASE, MENEAME_DESTACADAS
from properties import MENEAME_PENDIENTES, MENEAME_POPULARES, MENEAME_MAS_VISITADAS
import datetime
from datetime import time, timedelta
import sys
import threading
from utils import retry

class ObtenerNoticias(object):
    
    def __init__(self):
        self._html = None
        self.estado = False
        
    def _obtener_contenido(self, url=MENEAME_BASE, pagina=None):
        try:
            uri = url
            if pagina:
                uri = uri +'?page='+str(pagina)
            html = urlopen(uri).read()
            if html.__len__() > 0:
                self.estado = True
            return html
        except:
            self.estado = False
            return None  

    def _obtener_contenido_url(self, url):
        try:
            html = urlopen(url).read()
            return html
        except:
            return None

    @retry(HTTPError, tries=4, delay=10, backoff=2)
    def _obtener_contenido_links(self, url, list):
        try:
            html = urlopen(url).read()
            list.append({'url':url,'contenido':html})
            return html
        except:
            return None

    def fetch_parallel(self, urls):
        list = []
        threads = [threading.Thread(target=self._obtener_contenido_links, args = (url,list)) for url in urls]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return list


    def _existeix_url(self, url):
        try:
            code = urlopen(url).code
            if code == 200:
                return True
        except:
            return False    
    
    def _obtener_items(self, regexpr1, regexpr2):
        l = []
        g = re.findall(regexpr1, self._html, re.I|re.S)
        if g:
            for m in g:
                p = re.search(regexpr2, m, re.I)
                if p:
                    n = p.groups()[0].strip()
                    l.append(n)
        return l
    
    def _obtener_links(self):
        regexpr1 = r'<h2> <a href=".*?" class'
        regexpr2 = '<h2> <a href="(.*?)" class'
         
        return self._obtener_items(regexpr1,regexpr2)
    
    def _obtener_titulos(self):
        regexpr1 = r'<h2> <a href=".*?>.*?</a>'
        regexpr2 = '<h2> <a href=".*?>(.*?)</a>'
         
        return self._obtener_items(regexpr1,regexpr2)
    
    def _obtener_meneos(self):
        regexpr1 = r'<div class="votes">.*?>.*?</a> meneos'
        regexpr2 = '<div class="votes">.*?>(.*?)</a> meneos'
         
        return self._obtener_items(regexpr1,regexpr2)
    def _obtener_descripciones(self):
        regexpr1 = r'  <p>.*?</p>'
        regexpr2 = '  <p>(.*?)</p>'
         
        return self._obtener_items(regexpr1,regexpr2)
    
    def _obtener_autores(self):
        regexpr1 = r'history">.*?</a>'
        regexpr2 = 'history">(.*?)</a>'
         
        return self._obtener_items(regexpr1,regexpr2)
        
    def _obtener_tag1(self):
        regexpr1 = r'title="meta: .*?">'
        regexpr2 = 'title="meta: (.*?)">'
        return self._obtener_items(regexpr1,regexpr2)
        

    def _obtener_tag2(self):
        regexpr1 = r'title="categoría:.*?">'
        regexpr2 = 'title="categoría:(.*?)">'
        return self._obtener_items(regexpr1,regexpr2)
        
    def _make_tags(self,tag1,tag2):
        l = []
        for i in range(0,len(tag1)):
            tags = []
            tags.append(tag1[i])
            tags.append(tag2[i])
            l.append(tags)
            
        return l

    def _obtener_fechas(self):

        regexpr1 = r'por  <a href="/user/.*?</a>.*?</div>'
        regexpr2 = 'por  <a href="/user/.*?</a>(.*?)</div>'
        return self._obtener_items(regexpr1,regexpr2)
        
        
    def _obtener_links_noticias(self, html):
        links = []
        while True:
            start = html.find('class="comments-counter"')
            if start == -1:
                break
            start_link = html.find('<a href="', start)
            end_link = html.find('"', start_link+9)
            link = html[start_link+9:end_link]
            links.append(MENEAME_BASE[:-1]+link+'/')
            html = html[start+1:]
        return links

    def _obtener_paginas(self, html):
        start = html.find('title="ir a página ')
        if start == -1:
            return -1
        end = html.find('">', start)
        a = int(html[start+20: end])+1
        return a

    def _obtener_autor_comentario(self, html):
        htm = html
        autors = []
        while True:
            start_link = htm.find('<div class="comment-info"')
            if start_link == -1:
                break
            end_link = htm.find('</div>', start_link+1)
            html_info = htm[start_link:end_link]
            start_link2 = html_info.find('<a href="/user/')
            end_link2 = html_info.find('"', start_link2+10)
            autor = html_info[start_link2+15:end_link2]
            # print autor
            autors.append(autor)
            htm = htm[end_link+1:]
        return autors

    # obté tots els autors de totes 
    def _obtener_autores_comentarios(self):
        autores_com = []
        links = self._obtener_links_noticias(self._html)
        for link in links: # para todas las noticias
            html_noticia = self._obtener_contenido_url(link)
            pags = self._obtener_paginas(html_noticia)
            if pags == -1:
                pags = 1
            for p in range(1, pags+1):
                html_noticia = self._obtener_contenido_url(link+str(p))
                autores = self._obtener_autor_comentario(html_noticia)
                autores_com.append(autores)
        return autores_com

    # obté els comentaris d'una sola notícia i d'una sola página d'una notícia
    def _obtener_comentario(self, html):
        h = html
        l = []
        while True:
            start_link = h.find('id="cid-')
            if start_link == -1:
                break
            end_link = h.find('</div>', start_link+1)
            html_comentari = h[start_link:end_link]

            start_link2 = html_comentari.find('</a>')
            end_link2 = html_comentari.find('</div>', start_link2+1)
            h = h[end_link+1:]
            l.append(html_comentari[start_link2+16:end_link2])
        l.append('$FI$')
        return l

    # obté tots els comentaris de totes les notícies (incuides amb més d'una pagina de comentaris també)
    def _obtener_comentarios(self):
        comentarios = []
        links = self._obtener_links_noticias(self._html)
        for link in links: # para todas las noticias
            # print "LINK >>> ", link
            html_noticia = self._obtener_contenido_url(link)
            pags = self._obtener_paginas(html_noticia)
            if pags == -1:
                pags = 1
            # print "PAGS >>> ", pags
            for p in range(1, pags+1):
                html_noticia = self._obtener_contenido_url(link+str(p))
                com = self._obtener_comentario(html_noticia)
                # print "LEN ", len(com)
                comentarios.append(com) 
        return comentarios # llista de subllistes que contenen els comentaris de cada noticia

    def _make_noticias(self, contenido):
        l = []
        min=0
        #max = len(contenido['descripciones'])
        max = len(contenido['fechas'])
        
        if (max > 20):
            max=20
            #contenido['descripciones'].pop(0)
        
        for i in range(min,max):
            f = self._tratar_fecha(contenido['fechas'][i])
            l.append({ 'titulo': contenido['titulos'][i],
                 'link': contenido['links'][i],
                 'meneos': contenido['meneos'][i],
                 'descripcion': contenido['descripciones'][i],
                 'autor': contenido['autores'][i],
                 'link_noticia': contenido['links_noticias'][i],
                 'comentario': contenido['comentarios'][i],
                 'tags': contenido['tags'][i],
                 'fechaEnvio': f[0],
                 'fechaPublicacion': f[1],
                 'autor_comentario': contenido['autores_comentarios'][i]
                })
        
        return l

    def _coger_fecha(self,fecha):
        a =""
        p = []
        num = "false"
        for i in range(0,len(fecha)):
            n = ord(fecha[i])
            if (n>47 and n<58):
                num = "true"
                a = a + fecha[i]
            elif (num=="true"):
                p.append(a)
                a = ""
                num = "false"
        if (len(p)==3):
            data = datetime.datetime.today() - timedelta(days=int(p[0]))
            data = data - timedelta(hours=int(p[1]))
            data = data - timedelta(minutes=int(p[2]))
        elif (len(p)==2):
            data = datetime.datetime.today() - timedelta(hours=int(p[0]))
            data = data - timedelta(minutes=int(p[1]))
        elif (len(p)==1):
            data = datetime.datetime.today() - timedelta(minutes=int(p[0]))
        else:
            #17-02-2013 21:35 
            data = datetime.datetime(int(p[2]),int(p[1]),int(p[0]),int(p[3]),int(p[4]))
        return data


    def _tratar_fecha(self,fechas):
        fechaEnvio = re.split("publicado ",fechas)
        fechaPublicado = fechaEnvio[1]
        fechaEnvio = fechaEnvio[0]
        return self._coger_fecha(fechaEnvio),self._coger_fecha(fechaPublicado)
        
        
    def get(self, pagina=1):
        self._html = self._obtener_contenido(MENEAME_BASE, pagina)
        contenido = {}
        contenido['titulos'] = self._obtener_titulos()
        contenido['links'] = self._obtener_links()
        contenido['meneos'] = self._obtener_meneos()
        contenido['descripciones'] = self._obtener_descripciones()
        contenido['autores'] = self._obtener_autores()
        contenido['links_noticias'] = self._obtener_links_noticias(self._html)
        contenido['comentarios'] = self._obtener_comentarios()
        contenido['tags'] = self._make_tags(self._obtener_tag1(), self._obtener_tag2()) 
        contenido['tags'] = self._make_tags(self._obtener_tag1(), self._obtener_tag2())
        contenido['fechas'] = self._obtener_fechas()
        contenido['autores_comentarios'] = self._obtener_autores_comentarios()

        for item in contenido['comentarios']:
            print len(item)
        sys.exit()
        return self._make_noticias(contenido)
