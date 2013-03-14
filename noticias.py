# -*- coding: utf-8 -*-
from meneame.obtenerNoticias import ObtenerNoticias


o = ObtenerNoticias()
res = o.get(1) #1 = num de pagina
#falta pasar de unicode a utf-8
for index,item in enumerate(res):
    print "------------------------------------------------------------------"
    print "#"+ str(index)
    print item
    print "------------------------------------------------------------------"