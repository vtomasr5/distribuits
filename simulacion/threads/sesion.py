 # -*- coding: utf-8 -*-
import mechanize
import cookielib
import random
import string
from chomsky import chomsky
import re

class Sesion:
	def __init__(self, user , password):
		self.user 		= user
		self.password 	= password
		self._host 		= '130.206.134.123'
		self._path 		= 'meneame'
		self._cookie 	= None
		self._br 		= None

		self._init_mechanize()
		self._make_login()

	def _get_meneame_url(self):
		return 'http://'+self._host+'/'+self._path+'/'

	def _init_mechanize(self):
		self._cookie 		= cookielib.LWPCookieJar()
		self._br 			= mechanize.Browser(factory=mechanize.RobustFactory())
		self._br.addheaders = [
								(
								 'User-agent', 
								 'Mozilla/5.0 (Windows; U; Windows NT6.0; en-US; rv:1.9.0.6'
								)
							  ]
		
		self._br.set_cookiejar(self._cookie)
		self._br.set_handle_equiv(True)
		self._br.set_handle_redirect(True)
		self._br.set_handle_referer(True)
		self._br.set_handle_robots(False)
		self._br.set_debug_responses(True)
		self._br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		self._br.set_handle_redirect(mechanize.HTTPRedirectHandler)


	def _make_login(self):
		url = self._get_meneame_url()+'login.php'

		self._br.open(url)
		self._br.select_form(nr=1)
		self._br['username'] = self.user
		self._br['password'] = self.password
		self._br.submit()

	def _random_tag(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))

	def _generate_content(self, title, tags, bodytext, category):
		d = {
			'title'	   : title,
			'tags' 	   : tags,
			'bodytext' : bodytext,
			'category' : category
		}
		if len(title) 	 == 0:
			d['title'] = chomsky(1, 72)[0:120]
		if len(tags) 	 == 0:
			d['tags']  = self._random_tag()
		if len(bodytext) == 0:
			d['bodytext'] = chomsky(4, 72)[0:500]

		categories = [17, 25, 7, 18, 20, 44, 24, 38, 64, 41, 22, 
			62, 36, 61, 29, 60, 15, 16, 9, 45, 6, 35, 27, 12, 32, 
			28, 5, 10, 13, 40, 8, 4, 23, 39, 43, 42, 37, 11, 1]
		rand = random.randrange(len(categories)-1)
		if category == -1:
			d['category'] = str(categories[rand]) #Hay 60 categorías

		return d

	def make_a_comment(self, story, msg=''):
		url = self._get_meneame_url()+'story.php?id='+str(story)
		if len(msg) == 0:
			msg = chomsky(4, 72)[0:500]
		self._br.open(url)
		self._br.select_form(nr=1)
		self._br['comment_content'] = msg
		self._br.submit()

	def make_a_new(self, url_of_new, title='', tags='', bodytext='', category=-1):
		url = self._get_meneame_url()+'submit.php'

		self._br.open(url)
		#Paso 1 de 3
		self._br.select_form(nr=1)
		self._br['url'] = url_of_new

		response = self._br.submit()
		#Paso 2 de 3
		html = response.get_data()
		regex = re.compile("<p class=\"error\">(.+?)</p>")
		l = regex.findall(html)

		if not len(l):
			self._br.select_form(nr=1)
			infoPaso2 = self._generate_content(title, tags, bodytext, category)

			self._br['title'] 	 = infoPaso2['title']
			self._br['tags'] 	 = infoPaso2['tags']
			self._br['bodytext'] = infoPaso2['bodytext']
			self._br['category'] = [infoPaso2['category']]
			self._br['type'] 	 = ['text']
			
			response = self._br.submit()
			#Paso 3 de 3
			self._br.select_form(nr=1)
			#print self._br.form
			self._br.submit()
			#print response.get_data()
		else:
			print 'Se ha producido el siguiente error: ' + l[0]

