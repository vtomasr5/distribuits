# python noticiasSql.py <pag_inicial> <pag_final> published
# -*- coding: utf-8 -*-
from meneame.obtenerNoticias import ObtenerNoticias
from meneame.utils import limpia, limpia1
import sys
import re

o = ObtenerNoticias()
#'discard','queued','published'

init = int(sys.argv[1])
max = int(sys.argv[2])

status = sys.argv[3]

f1 = open('all_page.sql','w')
for i in reversed(range(init-1,max)):
	k = str(i)
	f = open('page'+str(i)+'.sql','w')
	res = o.get(i)
	b = ""
	c = ""
    #falta pasar de unicode a utf-8
	i = 1
	comment_id = 0
	for index,item in (enumerate(res)):
		b = b + "insert into users (user_id,user_login) values (NULL,'"+ item['autor'] +"');\n\n"
		b = b + "insert into links (link_id,link_content,link_title,link_url,link_votes,link_author,"
		b = b + "link_tags,link_status,link_sent_date,link_date) values ("+str(i)+", '" 
		b = b + limpia(item['descripcion']) + "',"
		b = b + "'" + limpia(item['titulo']) + "',"
		b = b + "'" + item['link'] + "',"
		b = b + item['meneos'] + ","
		b = b + "(Select user_id from users where user_login ='"+ item['autor'] +"'),"
		#falten es tags, es pos un xk sinos no va be
		b = b + "'" + limpia(item['tags'][0]) + "-" +  limpia(item['tags'][1]) + "',"
		#print str(item['fechaEnvio'])
		k = re.split(".",str(item['fechaEnvio']))
		#print k
		k1 = re.split(".",str(item['fechaPublicacion']))
		b = b + "'" + status +"','"+str(item['fechaEnvio'])+"','"+str(item['fechaPublicacion'])
		b = b + "');" "\n\n"
		f.write(b)
		f1.write(b)
		b =""
		comment_id = 0
		print "Noticia"+str(i)
		print "Comentarios: "+str(len(item['comentario']))
		print "Fechas de comentarios: "+str(len(item['fecha_comentario']))
		print "Fechas de autores: "+str(len(item['autor_comentario']))
		for comment in (enumerate(item['comentario'])):
			if comment_id < len(item['fecha_comentario']):#Esto está asi para que no pete
				comentario_fecha = item['fecha_comentario'][comment_id]
			if comment_id < len(item['autor_comentario']):
				comentario_autor = item['autor_comentario'][comment_id]
			c = c + "insert into comments (comment_id,comment_type,comment_link_id,comment_content,"
			c = c + "comment_user_id,comment_date)values (NULL,'normal',"+str(i)+",'"+limpia1(str(comment))+"',"
			c = c + "(Select user_id from users where user_login ='"+ comentario_autor +"'),'"+str(comentario_fecha)+"');\n\n"
			f.write(c)
			f1.write(c)
			c =""
			comment_id = comment_id + 1
		i = i + 1
	f.close()
f1.close()
