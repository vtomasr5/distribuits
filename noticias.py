# -*- coding: utf-8 -*-
from meneame.obtenerNoticias import ObtenerNoticias
from meneame.properties import PAGINA

<<<<<<< HEAD
PAGINA = 1

o = ObtenerNoticias()
res = o.get(PAGINA)
#falta pasar de unicode a utf-8
for index,item in enumerate(res):
    print "#"+ str(index)
    print item
    print "------------------------------------------------------------------" 
=======
if __name__ == '__main__':
    o = ObtenerNoticias()
    res = o.get(PAGINA)
    #falta pasar de unicode a utf-8
    for index,item in enumerate(res):
        print "------------------------------------------------------------------"
        print "#"+ str(index)
        print item
        print "------------------------------------------------------------------" 
>>>>>>> c24ce09086e0098556db9f28a805dadf47e9e7a4
