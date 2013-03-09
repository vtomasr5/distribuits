# -*- coding: utf-8 -*-
from urllib2 import urlopen, URLError, HTTPError
from urlparse import urlparse, urlsplit, urljoin
import re, os, sys
from properties import MENEAME_URL

class ObtenerNoticias:
    
    def __init__(self):
        self._html = None
        
    def _obtener_contenido(self, pagina):
        try:
            doc = urlopen(MENEAME_URL+'/?page='+str(pagina))
            return doc.read()
        except:
            return None    
    
    def _obtener_items(self, regexpr1, regexpr2):
        list = []
        g = re.findall(regexpr1, self._html, re.I|re.S)
        if g:
            for m in g:
                p = re.search(regexpr2, m, re.I)
                if p:
                    l = p.groups()[0].strip()
                    list.append(l)
        
        return list
    
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

    def _make_noticias(self, contenido ):
        list = []
        min=0
        max = len(contenido['descripciones'])
        
        if (max > 20):
            max=20
            contenido['descripciones'].pop(0)
        
        for i in range(min,max):
            list.append({ 'titulo': contenido['titulos'][i],
                 'link': contenido['links'][i],
                 'meneos': contenido['meneos'][i],
                 'descripcion': contenido['descripciones'][i],
                 'autor': contenido['autores'][i],
                })
        
        return list

    def get(self, pagina=1):
        self._html = self._obtener_contenido(pagina)
        contenido = {}
        contenido['titulos'] = self._obtener_titulos()
        contenido['links'] = self._obtener_links()
        contenido['meneos'] = self._obtener_meneos()
        contenido['descripciones'] = self._obtener_descripciones()
        contenido['autores'] = self._obtener_autores()
        
        return self._make_noticias(contenido)
