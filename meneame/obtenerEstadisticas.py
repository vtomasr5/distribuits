import feedparser
import sys
import configparser
import datetime
import time

class obtenerEstadisticas(object):
	def __init__(self, path, url):
		self._feed = feedparser.parse(url)
		name = self._feed['channel']['title'].split(' ')[-1]
		self._output_file = path+'/output/'+name+'.ini'

	def getFeeds(self):
		return self._feed

	def __fileExists(self):
		try:
		   with open(self._output_file): return True
		except IOError:
		   return False

	def __readfile(self):
		config = configparser.ConfigParser()
		config.read(self._output_file)
		config.sections()

		return config

	def __buildtemplate(self, num = 0, last_new = 0):
		if last_new == 0:
			last_new = datetime.datetime.strptime('01-01-2000 00:00:00', "%d-%m-%Y %H:%M:%S")
		config = configparser.RawConfigParser()
		config.add_section('master')
		config.set('master', 'num', num)
		config.set('master', 'last_new', last_new)

		with open(self._output_file, 'w') as configfile: config.write(configfile)

	def __to_datetime(self, s):
		return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

	def _get_date(self, s):
		try:
			date = s.split(' ')
			month = self._get_month(date[2])
			convert_date = date[1] + '-' + month + '-' + date[3] + ' ' + date[4]
			return datetime.datetime.strptime(convert_date, "%d-%m-%Y %H:%M:%S")
		except (ValueError, IndexError):
			return datetime.datetime.strptime('01-01-2000 00:00:00', "%d-%m-%Y %H:%M:%S")

	def _get_month(self, month):
		d = {'Ene': '01',
			 'Feb': '02',
			 'Mar': '03',
			 'Apr': '04',
			 'May': '05',
			 'Jun': '06',
			 'Jul': '07',
			 'Aug': '08',
			 'Sep': '09',
			 'Oct': '10',
			 'Nov': '11',
			 'Dic': '12'}

		return d[month]

	def getStats(self):
		fileexists = self.__fileExists()
		if not fileexists:
			self.__buildtemplate()
		
		config = self.__readfile()
		last_item = self.__to_datetime(config['master']['last_new'])
		num_items = int(config['master']['num'])

		date_max = last_item

		for index, feed in enumerate(self._feed['items']):
			feed_date = self._get_date(feed['published'])
			if index == 0:
				date_max = feed_date
			if last_item > feed_date:
				break
			num_items = num_items + 1

		self.__buildtemplate(num_items, date_max)
		t = time.asctime( time.localtime(time.time()))
		print '#'+str(t)+': Stats Guardadas (' + self._output_file +')'

	