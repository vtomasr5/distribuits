import threading
from time import sleep


class Sistema(threading.Thread):
	def __init__(self, resolution, path, sufijo):
		threading.Thread.__init__(self)

		self.exitFlag   	= False
		self.numeroClientes = 0
		self.mediaClientes	= 0
		self.iteracion		= 1
		self.path 			= path
		self.resolution		= resolution
		self.sufijo			= sufijo

	def run(self):
		self.file = open(self.path+'usuarios_sistema_'+self.sufijo+'.txt','w')
		while not self.exitFlag:
			try:
				while not self.exitFlag:
					self.mediaClientes = (self.mediaClientes + self.numeroClientes)
					self.file.write(str(self.mediaClientes/self.iteracion)+"\n")
					self.iteracion 	   = self.iteracion + 1
					sleep(self.resolution)
			except KeyboardInterrupt:  # CTRL+C interrupt
				self.file.close()
				return

	def shutdown(self, info=None):
		self.exitFlag = True
		self.file.close()
