from client import Client



class Master:
	def __init__(self):
		self.clients = []
		self._last_id = 1

	def messato_to_client(self, threadID, msg):
		client = self.get_client(threadID)
		client['thread'].set_message(msg)

	def add_client(self, url, sesionTime, consumptionTime):
		c = Client(self._last_id, url, sesionTime, consumptionTime)
		self.clients.append({'id': self._last_id, 'thread' : c })

		c.start()

		self._last_id = self._last_id + 1

	def remove_client(self, threadID):
		self.messato_to_client(threadID, 'shutdown')

	def get_client(self, threadID):
		client = [client for client in self.clients if client['id'] == threadID]
		return client[0]

	def get_last_client(self):
		if self._last_id > 1:
			return (self._last_id-1)
		else:
			return 0