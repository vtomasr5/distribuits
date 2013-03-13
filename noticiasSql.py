# -*- coding: utf-8 -*-
from obtenerNoticias import ObtenerNoticias
import sys
import re

def limpia(antigua):
  	antigua = antigua.replace('á','a');
	antigua = antigua.replace('é','e');
	antigua = antigua.replace('í','i');
	antigua = antigua.replace('ó','o');
	antigua = antigua.replace('ú','u');
	antigua = antigua.replace('ñ','n');
	antigua = antigua.replace("'",'*');
	return antigua

o = ObtenerNoticias()
#'discard','queued','published'

init = int(sys.argv[1])
max = int(sys.argv[2])

status = sys.argv[3]

f1 = open('all_page.sql','w')
for i in reversed(range(init-1,max)):
	k = str(i)
	print 'page'+str(i+1)
	f = open('page'+str(i)+'.sql','w')
	res = o.get(i)
	b = ""
    #falta pasar de unicode a utf-8
	for index,item in (enumerate(res)):
		b = b + "insert into users (user_id,user_login) values (NULL,'"+ item['autor'] +"');\n\n"
		b = b + "insert into links (link_id,link_content,link_title,link_url,link_votes,link_author,"
		b = b + "link_tags,link_status,link_sent_date,link_published_date) values (NULL, '" 
		b = b + limpia(item['descripcion']) + "',"
		b = b + "'" + limpia(item['titulo']) + "',"
		b = b + "'" + item['link'] + "',"
		b = b + item['meneos'] + ","
		b = b + "(Select user_id from users where user_login ='"+ item['autor'] +"'),"
		#falten es tags, es pos un xk sinos no va be
		b = b + "'" + limpia(item['tags'][0]) + "-" +  limpia(item['tags'][1]) + "',"
		print str(item['fechaEnvio'])
		k = re.split(".",str(item['fechaEnvio']))
		print k
		k1 = re.split(".",str(item['fechaPublicacion']))
		b = b + "'" + status +"',"+k[0]+","+k1[0]
		b = b + ");" "\n\n"

	f.write(b)
	f.close()
	f1.write(b)
