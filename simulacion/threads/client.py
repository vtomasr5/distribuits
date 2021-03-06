import threading
import httplib
import Queue
from time import sleep, time
from sesion import Sesion
import sys


class Client(threading.Thread):
    def __init__(self, threadID, url, sesionTime, consumptionTime):
        threading.Thread.__init__(self)
        #Threads Variables
        self._threadID       = threadID
        self.url             = url
        self._connection     = None
        self.exitFlag        = False
        #Events Queue Messages
        self._mailbox        = Queue.Queue()
        #Simulation Variables
        self.sesionTime      = sesionTime
        self.consumptionTime = consumptionTime
        self.responseTime    = 0
        self.lastOperation   = ''
        self.lastPage        = ''
        #Permited Operation
        self.operation        = {'shutdown': self._shutdown,
                                 'wait': self._wait,
                                 'print': self._print,
                                 'setConsumptionTime': self._setConsumptionTime,
                                 'openPath': self._obtain_path_connection}

    def run(self):
        while not self.exitFlag:
            try:
                self._open_connection()
                msg = self._mailbox.get()
                operation = msg['operation']
                param = msg['parameter']
                self.operation[operation](param)
            except KeyError:  # Operation not in self.operation
                pass
            except KeyboardInterrupt:  # CTRL+C interrupt
                return
        sys.exit()

    def _open_connection(self):
        """
            Open http connection
        """
        self._connection = httplib.HTTPConnection(self.url)

    def _obtain_path_connection(self, d):
        """
            Open path
        """
        timeStart          = time()
        path 	           = '/meneame/story.php?id='+str(d['url'])
        action             = d['action']
        self.lastOperation = action
        self.lastPage      = d['url']
        html = ''
        if action == 'No':
            try:
        	   self._connection.request("GET", path)
        	   html = self._connection.getresponse()
            except httplib.BadStatusLine:
                pass
            except Exception, e: #Servidor Saturado
                self._print("Unexpected error:" + str(e))
        else:# Es un comentario o una noticia
            try:
            	s = Sesion('cajainas', 'miquel1234')

            	if action == 'Comentario':
            		s.make_a_comment(d['url']) #noticia 2858
            	else:
            		s.make_a_new('www.meneame.net/story.php?id='+str(d['url']))
            except Exception, e: #Servidor Saturado
                self._print("Mechanize error:" + str(e))
        endTime = time() - timeStart
        #self.responseTime = endTime + self.responseTime
        self.responseTime = endTime
        #self._print("Salgo de request")
        return html

    def _close_connection(self):
        """
            Close Open connection
        """
        self._connection.close()

    def set_message(self, msg):
        """
            Set a message for this client
        """
        self._mailbox.put(msg)

    """
        Threads Operations
    """
    def _print(self, msg=''):
        """
            Print a Message
        """
        print "#"+str(self._threadID) + " Msg: " + msg

    def _shutdown(self, info=None):
        """
            Exit Thread
        """
        self._print('shutdown')
        self._close_connection()
        self.exitFlag = True

    def _wait(self, seconds=0):
        """
            Thread Wait a x seconds
        """
        self._print("Sleeping " + str(seconds) + " seconds")
        sleep(seconds)

    def _setConsumptionTime(self, consumptionTime=0):
        """
            Set a consumption Time for this Thread
        """
        #self._print("Changing consumptionTime: " + str(consumptionTime))
        self.consumptionTime = consumptionTime
