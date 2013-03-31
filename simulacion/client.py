import threading
import httplib 
import Queue
from time import sleep

class Client(threading.Thread):
	def __init__(self, threadID, url, sesionTime, consumptionTime):  
		threading.Thread.__init__(self)
		#Threads Variables
		self._threadID 		 = threadID
		self.url 			 = url
		self._connection	 = None
		self.exitFlag 		 = False
		#Events Queue Messages
		self._mailbox 		 = Queue.Queue()
		#Simulation Variables
		self.sesionTime 	 = sesionTime
		self.consumptionTime = consumptionTime
		#Permited Operation
		self.operation 		 = {'shutdown': self._shutdown,
					 	  		'wait': self._wait,
					 	  		'print': self._print
					 	 	   }


	def run(self):
		while not self.exitFlag:
			msg = self._mailbox.get()
			operation = msg['operation']
			param = msg['parameter']
			self.operation[operation](param)

	def _open_connection(self):
		self._connection = httplib.HTTPConnection(self.url)
		self._connection.request("GET","/")

		return self._connection.getresponse()

	def _close_connection(self):
		self._connection.close()

	def set_message(self, msg):
		self._mailbox.put(msg)

	"""
		Threads Operations
	"""
	def _print(self, msg=''):
		print "#"+str(self._threadID) + " Msg: " + msg

	def _shutdown(self, info=None):
		"""
			Exit Thread
		"""
		self._print('shutdown')
		self.exitFlag = True

	def _wait(self, seconds=0):
		"""
			Thread Wait a x seconds
		"""
		self._print("Sleeping "+ str(seconds) + " seconds")
		print 
		sleep(seconds)

