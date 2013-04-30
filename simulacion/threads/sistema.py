import threading
from time import sleep


class Sistema(threading.Thread):
	def __init__(self, resolution, path):
		threading.Thread.__init__(self)

		self.exitFlag   	= False
		self.numeroClientes = 0
		self.path 			= path
		self.resolution		= resolution

	def run(self):
		self.file = open(self.path+'usuarios_sistema.txt','w')
		while not self.exitFlag:
			try:
				while not self.exitFlag:
					self.file.write(str(self.numeroClientes)+"\n")
					sleep(self.resolution)
			except KeyError:  # Operation not in self.operation
				self._print(self.rol+" monitor no permitido")
				self.file.close()
				return
			except KeyboardInterrupt:  # CTRL+C interrupt
				self.file.close()
				return

	def shutdown(self, info=None):
		self.exitFlag = True
		self.file.close()