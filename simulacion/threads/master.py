from time import time
import Queue
from client import Client
from estadisticas.estadistica import Estadistica
from evento import Evento

class Master(object):
    def __init__(self, texec, nconexions, url):
        self._clients = []
        self._last_id = 1
        self._tactual = time()
        self._texec = self._tactual+(60*texec)
        self._domain = url
        self._numberOfConnections = nconexions
        self._cola = Queue.PriorityQueue(0)
        self._lastKill = 1
        self._estadistica = Estadistica(1000)
        self._responseTime = 0
        self._npeticions = 0
        self._infoTimeClient = []
        self._alive_clients = []

    def _build_message(self, operation, parameter):
        return {'operation': operation, 'parameter': parameter}

    def _messato_to_client(self, threadID, msg):
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
        self._messato_to_client(threadID, self._build_message('shutdown', None))

    def wait_client(self, threadID, seconds):
        """
            Client Thread wait x seconds
        """
        self._messato_to_client(threadID, self._build_message('wait', seconds))

    def open_path_client(self, threadID, path):
        """
            Client Thread wait x seconds
        """
        d = {'thread': threadID,
             'url':path, 
             'action':self._estadistica.puedoEscribir(), 
             'time': 0
            }
        self._infoTimeClient.append(d)
        self._messato_to_client(threadID, self._build_message('openPath', self._infoTimeClient[-1]))

    def print_message(self, threadID, msg):
        """
            Print a Message in console
        """
        self._messato_to_client(threadID, self._build_message('print', msg))

    def setConsumptionTime_client(self, threadID, consumptionTime):
        """
            Set Consumption Time for a one Client
        """
        self._messato_to_client(threadID, self._build_message('setConsumptionTime', consumptionTime))

    def rutina_inicializacion(self):
        """
            Init Simulation
        """
        # Inicializamos todos los eventos
        tactual = self._tactual
        # while tactual < self._texec:
        tiempoLlegada = self._estadistica.obtenerLlegada()  # Funcion estadistica de t.llegada
        tactual = tiempoLlegada + tactual
        evento1 = Evento("LlegadaCliente", tactual, self._last_id)
        self._cola.put((tactual, evento1))
        self._last_id = self._last_id + 1

    def rutina_llegadas(self, evento):
        """
            Routine arrivals
        """
        print "El cliente : "+str(evento.numCliente) + " ha llegado en el tiempo " + str(evento.tiempo)
        ts = self._estadistica.obtenerSesion()
        tep = self._estadistica.obtenerPeticion()
        tactual = evento.tiempo

        tiempoLlegada = self._estadistica.obtenerLlegada()  # Funcion estadistica de t.llegada
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
        #aqui mediante mensajes le diria al cliente que vaya a otro sitio, no se como se hace aun y restaria el tiempo de consumo
        tep = self._estadistica.obtenerPeticion()
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
        print "El cliente : "+str(evento.numCliente) + " ha salido "
        self._npeticions = self._npeticions + 1
        self._responseTime = self._responseTime + self._obtain_client_response_time(evento.numCliente)
        self.remove_client(evento.numCliente)
        self._alive_clients.remove(evento.numCliente)
        self._lastKill = evento.numCliente

    def kill_threads(self):
        for thread in self._alive_clients:
            print "Killing thread "+str(thread)
            self.remove_client(thread)

    def simular(self):
        """
            Main method for run the simulation
        """
        tactual = self._tactual
        self.rutina_inicializacion()
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
        self.kill_threads()
        
        print ''
        print ''
        print ''
        print "TRESP: "+ str(self._responseTime / self._npeticions) + " segundos"
        print "NUM PETICIONES PROCESADAS: " + str(self._npeticions)
