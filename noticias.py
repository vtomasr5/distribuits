# -*- coding: utf-8 -*-
from meneame.obtenerNoticias import ObtenerNoticias

o = ObtenerNoticias()
for i in range(1,5):
    res = o.get(i)
    #falta pasar de unicode a utf-8
    print "------------------------------------------------------------------------------------------------------------->"+ str(i)
    for index,item in enumerate(res):
        print "------------------------------------------------------------------"
        print "#"+ str(index)
        print item
        print "------------------------------------------------------------------"
        
    print "<-------------------------------------------------------------------------------------------------------------" 