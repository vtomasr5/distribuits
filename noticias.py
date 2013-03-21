# -*- coding: utf-8 -*-
from meneame.obtenerNoticias import ObtenerNoticias
from meneame.properties import MENEAME_BASE, MENEAME_PENDIENTES
o = ObtenerNoticias()
res = o.get(1, MENEAME_PENDIENTES) #1 = num de pagina
#falta pasar de unicode a utf-8
for index,item in enumerate(res):
    print "------------------------------------------------------------------"
    print "#"+ str(index)
    print item
    print "------------------------------------------------------------------"