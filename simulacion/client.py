import threading
import httplib 
import Queue

class Client(threading.Thread):
	def __init__(self, threadID, url, sesionTime, consumptionTime):  
			threading.Thread.__init__(self)
			#Threads Variables
			self._threadID 		 = threadID
			self.url 			 = url
			self._connection		 = None
			#Events Queue Messages
			self._mailbox 		 = Queue.Queue()
			#Simulation Variables
			self.sesionTime 	 = sesionTime
			self.consumptionTime = consumptionTime

	def run(self):
		while True:
			msg = self._mailbox.get()
			print "#" + str(self._threadID)
			print "Msg: " + str(msg)

			if msg == 'shutdown':
				return

	def _open_connection(self):
		self._connection = httplib.HTTPConnection(self.url)
		self._connection.request("GET","/")

		return self._connection.getresponse()

	def _close_connection(self):
		self._connection.close()

	def set_message(self, msg):
		self._mailbox.put(msg)
