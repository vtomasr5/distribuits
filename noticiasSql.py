# python noticiasSql.py <pag_inicial> <pag_final> published
# -*- coding: utf-8 -*-
import sys
import re
import os
from meneame.obtenerNoticias import ObtenerNoticias
from meneame.utils import limpia, limpia1
from meneame.properties import MENEAME_BASE, MENEAME_PENDIENTES, DIROUT
from meneame.utils import get_path

if len(sys.argv) != 4:
    print 'python noticiasSql.py <pag_inicial> <pag_final> <published|pending>'
    sys.exit(1)

o = ObtenerNoticias()
p = get_path()
d = os.listdir(p)
if DIROUT not in d:
    os.mkdir(DIROUT)

path = p+'/'+DIROUT+'/'

init = int(sys.argv[1])
max = int(sys.argv[2])
status = sys.argv[3]

url_news = ''

all_news = []

if not status in ('published', 'pending'):
    print 'python noticiasSql.py <pag_inicial> <pag_final> <published|pending>'
    sys.exit()
elif status == 'published':
    url_news = MENEAME_BASE
else:
    status = 'queued'
    url_news = MENEAME_PENDIENTES

f1 = open(path + 'all_page_' + status + '.sql', 'w')
for i in reversed(range(init-1, max)):
    k = str(i)
    f = open(path + 'page' + str(i) + '_' + status + '.sql', 'w')
    res = o.get(i, url_news)
    b = ""
    c = ""
    #falta pasar de unicode a utf-8
    i = 1
    comment_id = 0
    if status == 'queued':
        res.reverse()
    for index, item in (enumerate(res)):
        if not item['titulo'] in all_news:
            all_news.append(item['titulo'])
            b = b + "insert into users (user_id,user_login,user_pass) values (NULL,'" + item['autor'] + "', '0000');\n\n"
            b = b + "insert into links (link_id,link_content,link_title,link_url,link_votes,link_author,"
            b = b + "link_category,link_status,link_sent_date"
            if status == 'published':
                b = b + ",link_date"
            # b = b + ") values ("+str(i)+", '"
            b = b + ") values (NULL, '"
            b = b + limpia(item['descripcion']) + "',"
            b = b + "'" + limpia(item['titulo']) + "',"
            b = b + "'" + item['link'] + "',"
            b = b + item['meneos'] + ","
            b = b + "(Select user_id from users where user_login ='" + item['autor'] + "'),"
            # falten es tags, es pos un xk sinos no va be
            b = b + "(SELECT category_id FROM categories WHERE category_name='"+item['tags'][1]+"'),"
            # print str(item['fechaEnvio'])
            k = re.split(".", str(item['fechaEnvio']))
            # print k
            k1 = re.split(".", str(item['fechaPublicacion']))
            b = b + "'" + status + "','" + str(item['fechaEnvio'])
            if status == 'published':
                b = b + "','" + str(item['fechaPublicacion'])
            b = b + "');" "\n\n"
            f.write(b)
            f1.write(b)
            comment_id = 0
            b = "SET @id_link = (select max(link_id) from links);\n\n"
            f.write(b)
            f1.write(b)
            for comment in (enumerate(item['comentario'])):
                if comment_id < len(item['fecha_comentario']):  # Esto está asi para que no pete
                    comentario_fecha = item['fecha_comentario'][comment_id]
                if comment_id < len(item['autor_comentario']):
                    comentario_autor = item['autor_comentario'][comment_id]
                c = c + "insert into users (user_id,user_login,user_pass) values (NULL,'" + comentario_autor + "', '0000');\n\n"
                c = c + "insert into comments (comment_id,comment_type,comment_link_id,comment_content,"
                c = c + "comment_user_id,comment_date)values (NULL,'normal',@id_link,'"+limpia1(str(comment))+"',"
                c = c + "(Select user_id from users where user_login ='" + comentario_autor + "'),'" + str(comentario_fecha) + "');\n\n"
                c = c + "SET @nombre_var = @nombre_var + 1; \n\n"
                f.write(c)
                f1.write(c)
                c = ""
                comment_id = comment_id + 1
            b = "update links set link_comments="+str(len(item['comentario']))+" where link_id=@id_link;"+"\n\n"
            f.write(b)
            f1.write(b)
            b = ""
            i = i + 1
    f.close()
f1.close()
