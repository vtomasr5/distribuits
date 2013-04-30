from time import time
import Queue
from client import Client
from estadisticas.estadistica import Estadistica
from evento import Evento
import numpy as np
from sistema import Sistema
import urllib2

class Master(object):
    def __init__(self, texec, numUsuario, url, password_metricas):
        self._clients           = []
        self._last_id           = 1
        self._tactual           = time()
        self._texec             = self._tactual+(60*texec)
        self._domain            = url
        self._cola              = Queue.PriorityQueue(0)
        self._lastKill          = 1
        self._estadistica       = Estadistica(numUsuario)
        self._responseTime      = 0
        self._npeticions        = 0
        self._infoTimeClient    = []
        self._alive_clients     = []
        self.password_metricas  = password_metricas
        self._sistema           = Sistema(1, self._estadistica._obtain_path())
        #Variables de la traza
        self.mediaSesion     = 0
        self.mediaPeticion   = 0
        self.mediaLlegadas   = 0
        #Variables muestrales
        self.muestraMediaSesion   = []
        self.muestraMediaPeticion = []
        self.muestraMediaLlegadas = []

    def _build_message(self, operation, parameter):
        return {'operation': operation, 'parameter': parameter}

    def _message_to_client(self, threadID, msg):
        """
            Send Message to a Client
        """
        client = self.get_client(threadID)
        client['thread'].set_message(msg)

    def _obtain_client_response_time(self, threadID):
        client = self.get_client(threadID)
        return client['thread'].responseTime

    def add_client(self, threadID, url, sesionTime, consumptionTime):
        """
            Create new Client Thread
        """
        self._alive_clients.append(threadID)
        c = Client(threadID, url, sesionTime, consumptionTime)
        self._clients.append({'id': threadID, 'thread': c})

        c.start()

    def get_client(self, threadID):
        """
            Return a client Thread
        """
        client = [client for client in self._clients if client['id'] == threadID]
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
        self._message_to_client(threadID, self._build_message('shutdown', None))

    def wait_client(self, threadID, seconds):
        """
            Client Thread wait x seconds
        """
        self._message_to_client(threadID, self._build_message('wait', seconds))

    def open_path_client(self, threadID, path):
        """
            Client Thread wait x seconds
        """
        peticion = self._estadistica.obtenerPeticionEsc()
        d = {'thread': threadID,
             'url':path,
             'action':peticion[:-1], #Quitamos \n
             'time': 0
            }
        self._infoTimeClient.append(d)
        self._message_to_client(threadID, self._build_message('openPath', self._infoTimeClient[-1]))

    def print_message(self, threadID, msg):
        """
            Print a Message in console
        """
        self._message_to_client(threadID, self._build_message('print', msg))

    def setConsumptionTime_client(self, threadID, consumptionTime):
        """
            Set Consumption Time for a one Client
        """
        self._message_to_client(threadID, self._build_message('setConsumptionTime', consumptionTime))

    def rutina_inicializacion(self):
        """
            Init Simulation
        """
        # Inicializamos todos los eventos
        tactual = self._tactual
        # while tactual < self._texec:
        tiempoLlegada = self._estadistica.obtenerLlegada()  # Funcion estadistica de t.llegada
        self.muestraMediaLlegadas.append(tiempoLlegada)
        tactual = tiempoLlegada + tactual
        evento1 = Evento("LlegadaCliente", tactual, self._last_id)
        self._cola.put((tactual, evento1))
        self._last_id = self._last_id + 1

    def rutina_llegadas(self, evento):
        """
            Routine arrivals
        """
        print "El cliente : "+str(evento.numCliente) + " ha llegado en el tiempo " + str(evento.tiempo)
        self._sistema.numeroClientes = self._sistema.numeroClientes + 1
        ts = self._estadistica.obtenerSesion()
        self.muestraMediaSesion.append(ts)
        tep = self._estadistica.obtenerPeticion()
        self.muestraMediaPeticion.append(tep)
        tactual = evento.tiempo

        tiempoLlegada = self._estadistica.obtenerLlegada()  # Funcion estadistica de t.llegada
        self.muestraMediaLlegadas.append(tiempoLlegada)
        tactual = tiempoLlegada + tactual
        evento1 = Evento("LlegadaCliente", tactual, self._last_id)
        self._cola.put((tactual, evento1))
        self._last_id = self._last_id + 1

        # Anyade un evento de salida
        if tep < ts:
            evento1 = Evento("SalidaCliente", tactual + tep, evento.numCliente)
            temps = tactual+tep
        else:
            evento1 = Evento("SalidaCliente", tactual + ts, evento.numCliente)
            temps = tactual+ts

        self._cola.put((temps, evento1))
        domini = self._domain
        path = self._estadistica.obtenerPopularidad()
        self.add_client(evento1.numCliente, domini, ts, tep)
        self.open_path_client(evento1.numCliente,  path)

    def rutina_salida(self, evento):
        """
            exit routine
        """
        print "El cliente : "+str(evento.numCliente) + " vuelve a entrar en el tiempo " + str(evento.tiempo)
        
        tep = self._estadistica.obtenerPeticion()
        self.muestraMediaPeticion.append(tep)
        client = self.get_client(evento.numCliente)
        clientActual = client['thread']
        tactual = evento.tiempo
        #sessionActual = sessiones[str(p.numCliente)]
        path = self._estadistica.obtenerPopularidad()
        if clientActual.consumptionTime + tep < clientActual.sesionTime:
            evento1 = Evento("SalidaCliente", tactual + tep, evento.numCliente)
            temps = tactual+tep
            self.open_path_client(evento1.numCliente,  path)
            newComsuptionTime = clientActual.consumptionTime+tep
        else:
            tr = clientActual.sesionTime - clientActual.consumptionTime
            temps = tactual+tr
            evento1 = Evento("SalidaClienteTotal", temps, evento.numCliente)
            newComsuptionTime = tr
        self._npeticions = self._npeticions + 1
        self._responseTime = self._responseTime + self._obtain_client_response_time(evento.numCliente)
        self._cola.put((temps, evento1))
        self.setConsumptionTime_client(evento.numCliente, newComsuptionTime)

    def rutina_salida_sistema(self, evento):
        """
            routine system exit
        """
        print "El cliente : "+str(evento.numCliente) + " ha salido del sistema"
        self._sistema.numeroClientes = self._sistema.numeroClientes - 1
        self._npeticions = self._npeticions + 1
        self._responseTime = self._responseTime + self._obtain_client_response_time(evento.numCliente)
        self.remove_client(evento.numCliente)
        self._alive_clients.remove(evento.numCliente)
        self._lastKill = evento.numCliente

    def kill_threads(self):
        for thread in self._alive_clients:
            print "Killing thread "+str(thread)
            self.remove_client(thread)

    def _start_metricas(self):
        urllib2.urlopen('http://130.206.134.123/exec_metrica.php?pw='+self.password_metricas).read()
        self._sistema.start()

    def _end_metricas(self):
        urllib2.urlopen('http://130.206.134.123/exec_metrica.php?pw='+self.password_metricas+'&stop=1').read()
        self._sistema.shutdown()

    def simular(self):
        """
            Main method for run the simulation
        """
        self._start_metricas()
        error   = False
        tactual = self._tactual
        self.rutina_inicializacion()
        self.mediaSesion,self.mediaPeticion,self.mediaLlegadas = self._estadistica.obtenerMedias()
        try:
            while not(self._cola.empty()) and tactual < self._texec:
                evento = self._cola.get()[1]  # Coge el evento
                while tactual < evento.tiempo:
                    tactual = time()

                tactual = evento.tiempo
                if evento.tipoEvento == "LlegadaCliente":
                    self.rutina_llegadas(evento)
                elif evento.tipoEvento == "SalidaCliente":
                    self.rutina_salida(evento)
                else:
                    self.rutina_salida_sistema(evento)
        except KeyboardInterrupt:
            self.kill_threads()
            error = True

        if not error:
            self.kill_threads()
        self._end_metricas()

        meanLlegadas   = np.mean(self.muestraMediaLlegadas)
        meanPeticiones = np.mean(self.muestraMediaPeticion)
        meanSesion     = np.mean(self.muestraMediaSesion)

        stdLlegadas = np.std(self.muestraMediaLlegadas)
        stdPeticion = np.std(self.muestraMediaPeticion)
        stdLlegadas = np.std(self.muestraMediaSesion)


        print ''
        print "NUM PETICIONES PROCESADAS: " + str(self._npeticions)
        print ''
        print "TIEMPO ENTRE LLEGADA: "
        print "     Media Traza " + str(self.mediaLlegadas)
        print "     Media Muestral "+ str(meanLlegadas) + " segundos"
        print "     Desviacion Estandar Muestral " + str(stdLlegadas)
        print "TIEMPO ENTRE PETICIONES:  "
        print "     Media Traza " + str(self.mediaSesion)
        print "     Media Muestral "+ str(meanPeticiones) + " segundos"
        print "     Desviacion Estandar Muestral " + str(stdPeticion)
        print "TIEMPO DURACION SESION:"
        print "     Media Traza " + str(self.mediaPeticion)
        print "     Media Muestral "+ str(meanSesion) + " segundos"
        print "     Desviacion Estandar Muestral " + str(stdLlegadas)
        print ""
        print "TRESP: "+ str(self._responseTime / self._npeticions) + " segundos"
