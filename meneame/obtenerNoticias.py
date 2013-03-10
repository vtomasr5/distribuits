# -*- coding: utf-8 -*-
from urllib2 import urlopen, URLError
import re
import httplib
from properties import MENEAME_URL

class ObtenerNoticias(object):
    
    def __init__(self):
        self._html = None
        
    def _obtener_contenido(self, pagina):
        try:
            doc = urlopen(MENEAME_URL+'/?page='+str(pagina))
            return doc.read()
        except:
            return None    

    def _obtener_contenido_url(self, url):
        try:
            html = urlopen(url).read()
            return html
        except:
            return None

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

    def _obtener_links_noticias(self, html):
        links = []
        while True:
            start = html.find('class="comments-counter"')
            if start == -1:
                break
            start_link = html.find('<a href="', start)
            end_link = html.find('"', start_link+9)
            link = html[start_link+9:end_link]
            links.append(MENEAME_URL+link+'/')
            html = html[start+1:]
        return links

    def _obtener_pagina_siguiente(self, html, pags):
        h = html
        start_link = h.find('title="ir a página "')
        if start_link == -1:
            return -1
        end_link = h.find('">', start_link+1)
        h = h[start_link+20:end_link]
        if h in pags:
            return -1
        else:
            return h

    def _obtener_comentarios(self):
        comentaris = [] # all comments from all reports
        comentari = [] # comments from one report
        pag_idas = [1]
        links = self._obtener_links_noticias(self._html)
        for link in links:
            # for i in range(1,6):
                # if self._existeix_url(link+str(i)):
            html_noticia = self._obtener_contenido_url(link)
            while True:
                start_link = html_noticia.find('id="cid-')
                if start_link == -1:
                    break
                end_link = html_noticia.find('</div>', start_link+1)
                html_comentari = html_noticia[start_link:end_link]

                start_link2 = html_comentari.find('</a>')
                end_link2 = html_comentari.find('</div>', start_link2+1)
                
                comentari.append(html_comentari[start_link2+16:end_link2])
                pag = self._obtener_pagina_siguiente(html_noticia, pag_idas)
                if pag == -1:
                    break # no more pages
                else:
                    pag_idas.append(int(pag))
                    link = link+'/'+pag_idas[-1]
                html_noticia = html_noticia[end_link+1:]
            comentaris.append(len(comentari))
        return comentaris

    def _make_noticias(self, contenido):
        l = []
        min=0
        max = len(contenido['descripciones'])
        
        if (max > 20):
            max=20
            contenido['descripciones'].pop(0)
        
        for i in range(min,max):
            l.append({ 'titulo': contenido['titulos'][i],
                 'link': contenido['links'][i],
                 'meneos': contenido['meneos'][i],
                 'descripcion': contenido['descripciones'][i],
                 'autor': contenido['autores'][i],
                 'link_noticia': contenido['links_noticias'][i],
                 'comentario': contenido['comentarios'][i]
                })
        
        return l

    def get(self, pagina=1):
        self._html = self._obtener_contenido(pagina)
        contenido = {}
        contenido['titulos'] = self._obtener_titulos()
        contenido['links'] = self._obtener_links()
        contenido['meneos'] = self._obtener_meneos()
        contenido['descripciones'] = self._obtener_descripciones()
        contenido['autores'] = self._obtener_autores()
        contenido['links_noticias'] = self._obtener_links_noticias(self._html)
        contenido['comentarios'] = self._obtener_comentarios()
        
        return self._make_noticias(contenido)
