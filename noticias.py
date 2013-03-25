# -*- coding: utf-8 -*-
from meneame.obtenerNoticias import ObtenerNoticias
from meneame.properties import MENEAME_BASE, MENEAME_PENDIENTES

o = ObtenerNoticias()
res = o.get(1, MENEAME_PENDIENTES) #1 = num de pagina

for index,item in (enumerate(res)):
    print "Noticia"+str(index)
    print "Comentarios: "+str(len(item['comentario']))
    print "Fechas de comentarios: "+str(len(item['fecha_comentario']))
    print "Fechas de autores: "+str(len(item['autor_comentario']))
    print item['tags']