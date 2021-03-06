from time import time
import Queue
from client import Client
from estadisticas.estadistica import Estadistica
from evento import Evento
import numpy as np
from sistema import Sistema
import urllib2
from time import sleep

class Master(object):
    def __init__(self, texec, numUsuario, url, password_metricas, transitorio, sufijo, path_estadisticas):
        self.path_estadisticas   = path_estadisticas
        self._clients            = []
        self._last_id            = 1
        self._tactual            = time()
        self._texec              = self._tactual+(60*texec)
        self._domain             = url
        self._cola               = Queue.PriorityQueue(0)
        self._lastKill           = 1
        self._estadistica        = Estadistica(numUsuario)
        self._responseTime       = 0
        self._npeticions         = 0
        self._infoTimeClient     = []
        self._alive_clients      = []
        self.password_metricas   = password_metricas
        self._sistema            = Sistema(1, self._estadistica._obtain_path(), sufijo)
        self.nclients            = 0
        self.clientsAc           = 0
        self.timeLastEvent       = 0
        self.timeStart           = 0
        self.ficheroClientes     = open(path_estadisticas+'num_clientes_acumulado_'+sufijo+'.txt', 'w')
        self.transitorio         = transitorio
        self.regimenEstacionario = False
        self.sufijoMetricas      = sufijo
        #Variables de la traza
        self.mediaSesion         = 0
        self.mediaPeticion       = 0
        self.mediaLlegadas       = 0
        self.lastAcumulateClient = 0
        #Variables muestrales
        self.muestraMediaSesion   = []
        self.muestraMediaPeticion = []
        self.muestraMediaLlegadas = []
        self.muestraTRespuesta    = []
        #Cluster de tiempo de respuesta para
        self.mediaTRcentroides    = [0.45, 8.7, 16.4, 32.2]
        self.clusterTRespuesta    = [[], [], [], []]
        self.ficheroTRRespuesta   = open(path_estadisticas+'tr_paginas_'+sufijo+'.csv', 'w')

    def _escribirClientAc(self,ac):
        self.lastAcumulateClient = ac
        self.ficheroClientes.write(str(ac) + "\n")

    def _escribirTr(self, tr, pagina, operacion):
        self.ficheroTRRespuesta.write(str(tr)+','+str(pagina[:-1])+','+str(operacion)+'\n')

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
        self._escribirTr(client['thread'].responseTime,
                         client['thread'].lastPage,
                         client['thread'].lastOperation)
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

    def rutina_inicializacion(self,sufix=""):
        """
            Init Simulation
        """
        # Inicializamos todos los eventos
        tactual       = self._tactual
        tiempoLlegada = self._estadistica.obtenerLlegada(sufix)  # Funcion estadistica de t.llegada

        self.muestraMediaLlegadas.append(tiempoLlegada)

        tactual       = tiempoLlegada + tactual
        evento1       = Evento("LlegadaCliente", tactual, self._last_id)

        self._cola.put((tactual, evento1))

        self._last_id = self._last_id + 1

    def insert_tRespuesta(self, tr):
        last = 0
        index = len(self.mediaTRcentroides)-1
        for i,centroide in enumerate(self.mediaTRcentroides):
            if tr >= last  and tr < centroide:
                index = i
                break

        self.clusterTRespuesta[index].append(tr)

    def rutina_llegadas(self, evento,sufix=""):
        """
            Routine arrivals
        """
        print "El cliente : "+str(evento.numCliente) + " ha llegado en el tiempo " + str((evento.tiempo-self.timeStart)/60)
        self._sistema.numeroClientes = self._sistema.numeroClientes + 1
        ts = self._estadistica.obtenerSesion()
        self.muestraMediaSesion.append(ts)
        tep = self._estadistica.obtenerPeticion()
        self.muestraMediaPeticion.append(tep)
        tactual = evento.tiempo
        self.clientsAc = self.clientsAc + self.nclients*(evento.tiempo - self.timeLastEvent)
        self.nclients = self.nclients + 1
        if evento.tiempo-self.timeStart > 0:
            self.timeLastEvent = evento.tiempo

        print "Nclientes: " + str(self.nclients) + " Nacumulat: " + str(self.clientsAc/(evento.tiempo-self.timeStart))
        self._escribirClientAc(self.clientsAc/(evento.tiempo-self.timeStart))

        tiempoLlegada = self._estadistica.obtenerLlegada(sufix)  # Funcion estadistica de t.llegada
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
        print "El cliente : "+str(evento.numCliente) + " vuelve a entrar en el tiempo " + str((evento.tiempo-self.timeStart)/60)
        self.clientsAc = self.clientsAc + self.nclients*(evento.tiempo - self.timeLastEvent)

        print "Nclientes: " + str(self.nclients) + " Nacumulat: " + str(self.clientsAc/(evento.tiempo-self.timeStart))
        self._escribirClientAc(self.clientsAc/(evento.tiempo-self.timeStart))

        if evento.tiempo-self.timeStart > 0:
            self.timeLastEvent = evento.tiempo
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
            if tr < 0:
                temps = tactual + 1
            else:
                temps = tactual+tr
            evento1 = Evento("SalidaClienteTotal", temps, evento.numCliente)
            newComsuptionTime = tr

        if self.regimenEstacionario:
            self._npeticions = self._npeticions + 1
            responseTime = self._obtain_client_response_time(evento.numCliente)
            self.muestraTRespuesta.append(responseTime)
            self.insert_tRespuesta(responseTime)
            self._responseTime = self._responseTime + responseTime
        self._cola.put((temps, evento1))
        self.setConsumptionTime_client(evento.numCliente, newComsuptionTime)

    def rutina_salida_sistema(self, evento):
        """
            routine system exit
        """
        print "El cliente : "+str(evento.numCliente) + " ha salido del sistema en el tiempo " + str((evento.tiempo-self.timeStart)/60)


        self.clientsAc = self.clientsAc + self.nclients*(evento.tiempo - self.timeLastEvent)
        self.nclients = self.nclients - 1

        print "Nclientes: " + str(self.nclients) + " Nacumulat: " + str(self.clientsAc/(evento.tiempo-self.timeStart))
        self._escribirClientAc(self.clientsAc/(evento.tiempo-self.timeStart))

        if evento.tiempo-self.timeStart > 0:
            self.timeLastEvent = evento.tiempo

        self._sistema.numeroClientes = self._sistema.numeroClientes - 1

        if self.regimenEstacionario:
            self._npeticions   = self._npeticions + 1
            responseTime = self._obtain_client_response_time(evento.numCliente)
            self.muestraTRespuesta.append(responseTime)
            self.insert_tRespuesta(responseTime)
            self._responseTime = self._responseTime + responseTime

        self.remove_client(evento.numCliente)
        self._alive_clients.remove(evento.numCliente)
        self._lastKill = evento.numCliente

    def kill_threads(self):
        for thread in self._alive_clients:
            print "Killing thread "+str(thread)
            self.remove_client(thread)

    def _start_metricas(self):
        urllib2.urlopen('http://130.206.134.123/exec_metrica.php?pw='+self.password_metricas+'&nom='+self.sufijoMetricas).read()
        self._sistema.start()

    def _end_metricas(self):
        close_metricas = False
        while not close_metricas:
            try:
                urllib2.urlopen('http://130.206.134.123/exec_metrica.php?pw='+self.password_metricas+'&stop=1').read()
                close_metricas  = True
            except urllib2.URLError:
                print "Servidor Colapsado. Esperando 30 segundos para finalizar las metricas"
                sleep(0.5) #Esperamos 1 minuto a realizar la operacion ya que el servidor esta saturado
                close_metricas = False
            except:
                close_metricas  = True
        self._sistema.shutdown()

    def _write_t_respuesta(self):
        trespFichero = ""
        trespFichero = open(self.path_estadisticas+'tRespuesta_'+self.sufijoMetricas+'.csv', 'w')
        trespFichero.write("Tiempo_de_respuesta\n")
        #Imprimimos el t.respuesta generico
        for m in self.muestraTRespuesta:
            trespFichero.write(str(m)+"\n")
        trespFichero.close()

        #Imprimimos los grupos de trespuesta en un fichero
        trespFichero = open(self.path_estadisticas+'clustertRespuesta_'+self.sufijoMetricas+'.csv', 'w')
        cabecera = ''
        for centroide in self.mediaTRcentroides:
            cabecera = cabecera + "Centroide " + str(centroide)+','
        line = ''
        for cluster in self.clusterTRespuesta:
            if len(line) > 0:
                line = line + str(np.mean(cluster))+','
            else:
                line = line + '0,'
        trespFichero.write(cabecera[:-1]+'\n')
        trespFichero.write(line[:-1]+'\n')
        trespFichero.close()
        self.ficheroTRRespuesta.close()

    def _print_resultado_simulacion(self, meanLlegadas, meanPeticiones, meanSesion, tRespuesta, stdRespuesta, cvRespuesta):
        tResultado = open(self.path_estadisticas+'resultado_simulacion_'+self.sufijoMetricas+'.csv', 'w')
        s = ""
        s = s + "NUM PETICIONES PROCESADAS: " + str(self._npeticions) + "\n"
        s = s + "NUM MEDIO DE CLIENTES ACUMULADOS: " + str(self.lastAcumulateClient) + "\n"
        s = s + "" + "\n"
        s = s + "TIEMPO ENTRE LLEGADA:" + "\n"
        s = s + "     Media Traza    " + str(self.mediaLlegadas) + "\n"
        s = s + "     Media Muestral "+ str(meanLlegadas) + " segundos" + "\n"
        s = s + "TIEMPO ENTRE PETICIONES:" + "\n"
        s = s + "     Media Traza    " + str(self.mediaSesion) + "\n"
        s = s + "     Media Muestral "+ str(meanPeticiones) + " segundos" + "\n"
        s = s + "TIEMPO DURACION SESION:" + "\n"
        s = s + "     Media Traza    " + str(self.mediaPeticion) + "\n"
        s = s + "     Media Muestral "+ str(meanSesion) + " segundos" + "\n"
        s = s + "TIEMPO DE RESPUESTA:" + "\n"
        s = s + "     Media Muestral           "+ str(tRespuesta) + " segundos" + "\n"
        s = s + "     Desviacion Estandar      "+ str(stdRespuesta) + " segundos" + "\n"
        s = s + "     Coeficiente de Variacion "+ str(cvRespuesta) + " segundos" + "\n"
        s = s + "" + "\n"
        print s
        tResultado.write(s)
        tResultado.close()


    def simular(self):
        """
            Main method for run the simulation
        """
        self.ficheroTRRespuesta.write('TR,PAGINA,OPERACION\n')
        error   = False
        tactual = self._tactual
        self.rutina_inicializacion(self.sufijoMetricas)
        self.mediaSesion,self.mediaPeticion,self.mediaLlegadas = self._estadistica.obtenerMedias(self.sufijoMetricas)
        ejecutar = True
        self.timeStart = time()

        try:
            while (not self._cola.empty()) and tactual < self._texec and ejecutar:
                evento          = self._cola.get()[1]  # Coge el evento
                clientsAcumults = self.clientsAc/(evento.tiempo-self.timeStart)

                if (clientsAcumults > self.transitorio) and (not self.regimenEstacionario):
                    self._start_metricas()
                    self.regimenEstacionario = True

                while (tactual < evento.tiempo) and (tactual < self._texec) and ejecutar:
                    if tactual < evento.tiempo:
                        tactual = time()
                    else:
                        ejecutar = False

                if ejecutar:
                    tactual = evento.tiempo
                    if evento.tipoEvento == "LlegadaCliente":
                        self.rutina_llegadas(evento,self.sufijoMetricas)
                    elif evento.tipoEvento == "SalidaCliente":
                        self.rutina_salida(evento)
                    else:
                        self.rutina_salida_sistema(evento)

        except KeyboardInterrupt:
            self.kill_threads()
            error = True

        if not error:
            self.kill_threads()

        tRespuesta   = 0
        stdRespuesta = 0
        cvRespuesta  = 0
        if self.regimenEstacionario:
            self._end_metricas()
            tRespuesta   = np.mean(self.muestraTRespuesta)
            stdRespuesta = np.std(self.muestraTRespuesta)
            cvRespuesta  = stdRespuesta/tRespuesta

        meanLlegadas   = np.mean(self.muestraMediaLlegadas)
        meanPeticiones = np.mean(self.muestraMediaPeticion)
        meanSesion     = np.mean(self.muestraMediaSesion)

        self.ficheroClientes.close()
        self._write_t_respuesta()

        self._print_resultado_simulacion(meanLlegadas, meanPeticiones, meanSesion, tRespuesta, stdRespuesta, cvRespuesta)
