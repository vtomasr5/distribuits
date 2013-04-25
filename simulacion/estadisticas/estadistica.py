import sys
import os
import numpy.random as rand
import random

class Estadistica(object):

    def __init__(self, max, numNoticiaInicial, totalNoticias):
        self.llegadas = ""
        self.popularidad = ""
        self.sesion = ""
        self.peticion = ""
        self.max = max
        self.numNoticiaInicial = numNoticiaInicial
        self.numNoticias = totalNoticias
        self.probabilidades,self.noticias = self.initPopularidad(numNoticiaInicial, numNoticiaInicial+totalNoticias)

    def initPopularidad(self, numNoticiaInicio, numNoticiaFinal):
        self.noticias = []
        self.probabilidades = []
        mu = -0.10
        sigma = 2.43
        acumulacion = 0
        for i in range(0, numNoticiaFinal-numNoticiaInicio):
        	self.noticias.append(random.randint(numNoticiaInicio,numNoticiaFinal))	
        	aux = rand.lognormal(mu,sigma)
        	acumulacion = acumulacion + aux
        	self.probabilidades.append(acumulacion)
        for i in range(0, numNoticiaFinal-numNoticiaInicio):
            self.probabilidades[i] = self.probabilidades[i]/acumulacion
		
        self.probabilidades.sort()
        return self.probabilidades,self.noticias
		

    def _obtain_path(self):
        return os.path.realpath(os.path.dirname(sys.argv[0])) + '/estadisticas/'

    def generaFicheroLlegadas(self):
        path = self._obtain_path() + 'llegadas.txt'
        self.llegadas = open(path,'w')
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
        noticia = rand.random_sample()
        i = 0
        while i < self.numNoticias and not(self.probabilidades[i] > noticia):
        	i =  i + 1
        return str(i+self.numNoticiaInicial)

    def calculaTiempoSesion(self):
		  rho = 2
		  a = rand.zipf(rho)
		  return a
    def calculaTiempoEntrePeticion(self):
        mu = 2.245
        sigma = 1.133
        return rand.lognormal(mu, sigma)

    def peticionEscritura(self):
        r = rand.random_sample()
        if r <= 0.898:
            return 'Comentario'
        else:
            return 'Noticia'

    def puedoEscribir(self):
        r = rand.random_sample()
        if r <= 0.992:
            return 'No'
        else:
            return self.peticionEscritura()

if __name__ == "__main__" and __package__ is None:
    __package__ = "estadisticas.estadistica"
