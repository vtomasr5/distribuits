import sys
import os
import numpy
import random


class Estadistica(object):

    def initPopularidad(self):
        self.numNoticias = 200
        self.noticias = []
        self.probabilidades = []
        mu = -0.10
        sigma = 2.43
        acumulacion = 0
        for i in range(0,self.numNoticias):
        	self.noticias.append(random.randint(0,self.numNoticias))	
        	aux = numpy.random.lognormal(mu,sigma)
        	acumulacion = acumulacion + aux
        	self.probabilidades.append(acumulacion)
        for i in range(0,self.numNoticias):
            self.probabilidades[i] = self.probabilidades[i]/acumulacion
		
        self.probabilidades.sort()
        return self.probabilidades,self.noticias,self.numNoticias	

    def __init__(self, max):
        self.llegadas = ""
        self.popularidad = ""
        self.sesion = ""
        self.peticion = ""
        self.max = max
        self.probabilidades,self.noticias,self.numNoticias = self.initPopularidad()
		

    def _obtain_path(self):
        return os.path.realpath(os.path.dirname(sys.argv[0]))+'/estadisticas/'

    def generaFicheroLlegadas(self):
        path = self._obtain_path() + 'llegadas.txt'
        self.llegadas = open(path, 'w')
        for i in range(0, self.max):
            self.llegadas.write(str(self.calculaTiempoLlegada())+"\n")
        self.llegadas.close()
        self.llegadas = ""

    def generaFicheroPopularidad(self):
        path = self._obtain_path() + 'popularidad.txt'
        self.popularidad = open(path, 'w')
        for i in range(0, self.max):
            self.popularidad.write(str(self.calculaDireccionPopularidad())+"\n")
        self.popularidad.close()
        self.popularidad = ""

    def generaFicheroSesion(self):
        path = self._obtain_path() + 'sesion.txt'
        self.sesion = open(path, 'w')
        for i in range(0, self.max):
            self.sesion.write(str(self.calculaTiempoSesion())+"\n")
        self.sesion.close()
        self.sesion = ""

    def generaFicheroPeticion(self):
        path = self._obtain_path() + 'peticion.txt'
        self.peticion = open(path, 'w')
        for i in range(0, self.max):
            self.peticion.write(str(self.calculaTiempoEntrePeticion())+"\n")
        self.peticion.close()
        self.peticion = ""

    def obtenerLlegada(self):
        path = self._obtain_path() + 'llegadas.txt'
        if self.llegadas == "":
            self.llegadas = open(path, 'r')
        return float(self.llegadas.readline())

    def obtenerPopularidad(self):
        path = self._obtain_path() + 'popularidad.txt'
        if self.popularidad == "":
            self.popularidad = open(path, 'r')
        return self.popularidad.readline()

    def obtenerSesion(self):
        path = self._obtain_path() + 'sesion.txt'
        if self.sesion == "":
            self.sesion = open(path, 'r')
        return float(self.sesion.readline())

    def obtenerPeticion(self):
        path = self._obtain_path() + 'peticion.txt'
        if self.peticion == "":
            self.peticion = open(path, 'r')
        return float(self.peticion.readline())

    def calculaTiempoLlegada(self):
        """
            Tiempo entre peticiones diferentes
        """
        mu = 1.789
        sigma = 2.366
        return rand.lognormal(mu, sigma)
		  
	
    def calculaDireccionPopularidad(self):
        noticia = random.random()
        i = 0
        while i < self.numNoticias and not(self.probabilidades[i] > noticia):
        	i =  i + 1
        return "/numnoticia"+str(i)

    def calculaTiempoSesion(self):
        return 10

    def calculaTiempoEntrePeticion(self):
        mu = 2.245
        sigma = 1.133
        return rand.lognormal(mu, sigma)

    def puedoEscribir(self):
        r = rand.random_sample()
        if r <= 0.992:
            return False
        else:
            return True

if __name__ == "__main__" and __package__ is None:
    __package__ = "estadisticas.estadistica"
