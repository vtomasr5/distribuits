from client import Client



class Master:
	def __init__(self):
		self.clients = []
		self._last_id = 1

	def _build_message(self, operation, parameter):
		return {'operation' : operation, 'parameter': parameter}

	def _messato_to_client(self, threadID, msg):
		"""
			Send Message to a Client
		"""
		client = self.get_client(threadID)
		client['thread'].set_message(msg)

	def add_client(self, url, sesionTime, consumptionTime):
		"""
			Create new Client Thread
		"""
		c = Client(self._last_id, url, sesionTime, consumptionTime)
		self.clients.append({'id': self._last_id, 'thread' : c })

		c.start()

		self._last_id = self._last_id + 1

	def get_client(self, threadID):
		"""
			Return a client Thread
		"""
		client = [client for client in self.clients if client['id'] == threadID]
		return client[0]

	def get_last_client(self):
		"""
			Return a last client thread
		"""
		if self._last_id > 1:
			return (self._last_id-1)
		else:
			return 0

	def remove_client(self, threadID):
		"""
			Terminate with Client Thread
		"""
		self._messato_to_client(threadID, self._build_message('shutdown', None))

	def wait_client(self, threadID, seconds):
		"""
			Client Thread wait x seconds
		"""
		self._messato_to_client(threadID, self._build_message('wait', seconds))

	def print_message(self, threadID, msg):
		"""
			Print a Message in console
		"""
		self._messato_to_client(threadID, self._build_message('print', msg))
