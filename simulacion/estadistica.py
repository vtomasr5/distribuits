import random
class Estadistica:
	
	def __init__(self,max):
		self.llegadas = ""
		self.popularidad = ""
		self.sesion = ""
		self.peticion = ""
		self.max = max

	def generaFicheroLlegadas(self):
		self.llegadas = open('llegadas.txt', 'w')
		for i in range(0,self.max):
			self.llegadas.write(str(self.calculaTiempoLlegada())+"\n")
		self.llegadas.close()
		self.llegadas = ""

	def generaFicheroPopularidad(self):
		self.popularidad = open('popularidad.txt', 'w')
		for i in range(0,self.max):
			self.popularidad.write(str(self.calculaDireccionPopularidad())+"\n")
		self.popularidad.close()
		self.popularidad = ""

	def generaFicheroSesion(self):
		self.sesion = open('sesion.txt', 'w')
		for i in range(0,self.max):
			self.sesion.write(str(self.calculaTiempoSesion())+"\n")
		self.sesion.close()
		self.sesion = ""

	def generaFicheroPeticion(self):
		self.peticion = open('peticion.txt', 'w')
		for i in range(0,self.max):
			self.peticion.write(str(self.calculaTiempoEntrePeticion())+"\n")
		self.peticion.close()
		self.peticion = ""

	def obtenerLlegada(self):
		if self.llegadas =="":
			self.llegadas = open('llegadas.txt','r')
		return float(self.llegadas.readline())
	def obtenerPopularidad(self):
		if self.popularidad =="":
			self.popularidad = open('popularidad.txt','r')
		return self.popularidad.readline()
	def obtenerSesion(self):
		if self.sesion =="":
			self.sesion = open('sesion.txt','r')
		return float(self.sesion.readline())
	def obtenerPeticion(self):
		if self.peticion =="":
			self.peticion = open('peticion.txt','r')
		return float(self.peticion.readline())
		

	def calculaTiempoLlegada(self):
		return 1

	def calculaDireccionPopularidad(self):
		return "/"

	def calculaTiempoSesion(self):
		return 10

	def calculaTiempoEntrePeticion(self):
		return 4
