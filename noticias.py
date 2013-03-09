# -*- coding: utf-8 -*-
from meneame.obtenerNoticias import ObtenerNoticias
from meneame.properties import PAGINA

if __name__ == '__main__':
    o = ObtenerNoticias()
    res = o.get(PAGINA)
    #falta pasar de unicode a utf-8
    for index,item in enumerate(res):
        print "------------------------------------------------------------------"
        print "#"+ str(index)
        print item
        print "------------------------------------------------------------------" 