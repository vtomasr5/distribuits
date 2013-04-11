

class evento():
	def __init__(self,tipoEvento,tiempo,numCliente):  
		self.tipoEvento = tipoEvento
		self.tiempo = tiempo 
		self.numCliente = numCliente

import threading 
import httplib 
  
class Session(threading.Thread):  
      def __init__(self, direccion,tiempoSesion,tiempoConsumido):  
			threading.Thread.__init__(self)  
			self.connection = httplib.HTTPConnection(direccion)
			self.connection.request("GET","/")
			self.tiempoSesion = tiempoSesion
			self.tiempoConsumido = tiempoConsumido
			self.esperar =False
  
      def run(self):  
			while(True):
				if not(self.esperar):
					response = self.connection.getresponse()
					data = response.read()
					self.connection.close()
					self.esperar=True
				else:
					a=1

def calculaTiempoLlegada():
	return 1;

def calculaDireccionPopularidad():
	return ""

def calculaTiempoSesion():
	return 10;

def calculaTiempoEntrePeticion():
	return 4;
	
import Queue
import time


#Def. de variables de la simulacion
tactual = time.time()
texec = 60+tactual
cola = Queue.PriorityQueue(0)
numCliente = 0
dominio = "www.google.es"

#Inicializacion Simulacion
#Calculo de todas las llegadas
while tactual < texec :
	
	tiempoLlegada = calculaTiempoLlegada() #Funcion estadistica de t.llegada
	tactual = tiempoLlegada + tactual
	evento1 = evento("LlegadaCliente",tactual,numCliente) 
	cola.put((tactual,evento1))
	numCliente = numCliente + 1


#Inicio Simulacion
sessiones = {}
while not(cola.empty()):
	p = cola.get()[1] #Coge el evento
	while tactual < p.tiempo:
		tactual = time.time()
		pass
	tactual = p.tiempo
	if p.tipoEvento == "LlegadaCliente":
		print "T:"+str(tactual)+" El cliente : "+str(p.numCliente) + " ha llegado en el tiempo " + str(p.tiempo)
		ts = calculaTiempoSesion()
		tep = calculaTiempoEntrePeticion()
		if tep < ts:
			evento1 = evento("SalidaCliente",tactual+tep,p.numCliente)
			cola.put((tactual+tep,evento1))
			nuevaSesion = Session(dominio+calculaDireccionPopularidad(),ts,tep)
			nuevaSesion.start()  
			#nuevaSesion.join() 
			sessiones[str(p.numCliente)] = nuevaSesion
		else:
			evento1 = evento("SalidaCliente",tactual+ts,p.numCliente)
			cola.put((tactual+ts,evento1))
			nuevaSesion = Session(dominio+calculaDireccionPopularidad(),ts,tep)
			nuevaSesion.start()  
			#nuevaSesion.join() 
			sessiones[str(p.numCliente)] = nuevaSesion
	elif p.tipoEvento == "SalidaCliente":
		print "T:"+str(tactual)+" El cliente : "+str(p.numCliente) + " vuelve a entrar en el tiempo " + str(tactual)
		#aqui mediante mensajes le diria al cliente que vaya a otro sitio, no se como se hace aun y restaria el tiempo de consumo
		tep = calculaTiempoEntrePeticion()
		sessionActual = sessiones[str(p.numCliente)]
		if sessionActual.tiempoConsumido + tep < sessionActual.tiempoSesion:
			evento1 = evento("SalidaCliente",tactual+tep,p.numCliente)
			cola.put((tactual+tep,evento1))
			sessionActual.tiempoConsumido = sessionActual.tiempoConsumido + tep
		else:
			tr = sessionActual.tiempoSesion-sessionActual.tiempoConsumido
			evento1 = evento("SalidaClienteTotal",tactual + tr,p.numCliente)
			cola.put((tactual+tr,evento1))
			sessionActual.tiempoConsumido = tr
		sessiones[str(p.numCliente)] = sessionActual
	else:
		print "T:"+str(tactual)+" El cliente : "+str(p.numCliente) + " ha salido "
			










