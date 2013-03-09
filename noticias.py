# -*- coding: utf-8 -*-
from meneame.obtenerNoticias import ObtenerNoticias

PAGINA = 1

o = ObtenerNoticias()
res = o.get(PAGINA)
#falta pasar de unicode a utf-8
for index,item in enumerate(res):
    print "------------------------------------------------------------------"
    print "#"+ str(index)
    print item
    print "------------------------------------------------------------------" 