# -*- coding: utf-8 -*-
from obtenerNoticias import ObtenerNoticias
import sys

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

max = int(sys.argv[1])

status = sys.argv[2]

f1 = open('all-comments.sql','w')
status = 'published'
for i in reversed(range(1,max+1)):
	k = str(i)
	f = open('page'+str(i)+'.sql','w')
	res = o.get(i)
	b = ""
    #falta pasar de unicode a utf-8
	for index,item in (enumerate(res)):
		b = b + "insert into comments values ('"+ item['autor'] +"');\n\n"
		b = b + "insert into links (link_id,link_content,link_title,link_url,link_votes,link_author,"
		b = b + "link_tags,link_status) values (NULL, '" 
		b = b + limpia(item['descripcion']) + "',"
		b = b + "'" + limpia(item['titulo']) + "',"
		b = b + "'" + item['link'] + "',"
		b = b + item['meneos'] + ","
		b = b + "(Select user_id from users where user_login ='"+ item['autor'] +"'),"
		#falten es tags, es pos un xk sinos no va be
		b = b + "'" + limpia(item['tags'][0]) + "-" +  limpia(item['tags'][1]) + "',"
		b = b + "'" + status +"'"
		b = b + ");" "\n\n"

	f.write(b)
	f.close()
	f1.write(b)


# CREATE TABLE `comments` (
#   `comment_id` int(20) NOT NULL AUTO_INCREMENT,
#   `comment_type` enum('normal','admin','private') COLLATE utf8_spanish_ci NOT NULL DEFAULT 'normal',
#   `comment_randkey` int(11) NOT NULL DEFAULT '0',
#   `comment_parent` int(20) DEFAULT '0',
#   `comment_link_id` int(20) NOT NULL DEFAULT '0',
#   `comment_user_id` int(20) NOT NULL DEFAULT '0',
#   `comment_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   `comment_modified` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
#   `comment_ip` char(24) COLLATE utf8_spanish_ci DEFAULT NULL,
#   `comment_order` smallint(6) NOT NULL DEFAULT '0',
#   `comment_votes` smallint(4) NOT NULL DEFAULT '0',
#   `comment_karma` smallint(6) NOT NULL DEFAULT '0',
#   `comment_content` text COLLATE utf8_spanish_ci NOT NULL,
#   PRIMARY KEY (`comment_id`),
#   KEY `comment_link_id_2` (`comment_link_id`,`comment_date`),
#   KEY `comment_date` (`comment_date`),
#   KEY `comment_user_id` (`comment_user_id`,`comment_date`),
#   KEY `comment_link_id` (`comment_link_id`,`comment_order`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;