# coding: utf-8
import psutil as ps
import threading
import Queue
from time import sleep


class Monitor(threading.Thread):
    def __init__(self, rol, resolution, path):
        threading.Thread.__init__(self)

        self._mailbox   = Queue.Queue()
        self.exitFlag   = False
        self.resolution = resolution
        self.path       = path
        self.rol        = rol
        self.file       = None
        self.roles      = {
                            'cpu_monitor'    : self._cpu_monitor,
                            'memory_monitor' : self._memory_monitor,
                            'network_monitor': self._network_monitor,
                            'disk_monitor'   : self._disk_monitor
                          }

    def run(self):
        self.file = open(self.path+self.rol+'.txt','w')
        while not self.exitFlag:
            try:
                while not self.exitFlag:
                    self.roles[self.rol]()
                    sleep(self.resolution)
            except KeyError:  # Operation not in self.operation
                self._print(self.rol+" monitor no permitido")
                self.file.close()
                return
            except KeyboardInterrupt:  # CTRL+C interrupt
                self.file.close()
                return

    def _print(self, msg=''):
        """
            Print a Message
        """
        print "#" + str(self.rol) + " Msg: " + str(msg)

    def shutdown(self, info=None):
        self._print('shutdown')
        self.exitFlag = True
        self.file.close()

    def _cpu_monitor(self):
        s = ps.cpu_percent()
        self._print(s)
        self.file.write(str(s)+"\n")

    def _memory_monitor(self):
        s = ps.virtual_memory()[2]
        self._print(s)
        self.file.write(str(s)+"\n")

    def _network_monitor(self):
        """
            Packets sent or received
        """
        sent = ps.network_io_counters()[0]
        received = ps.network_io_counters()[1]
        self._print("Sent: " +str(sent)+ ", Received: " + str(received))
        self.file.write(str(sent)+";"+str(received)+"\n")

    def _disk_monitor(self):
        """
            Bytes read or write in a disk
        """
        read = ps.disk_io_counters()[2]
        write = ps.disk_io_counters()[3]
        self._print("Read: " +str(read)+ ", Write: " + str(write))
        self.file.write(str(read)+";"+str(write)+"\n")

if __name__ == "__main__" and __package__ is None:
    __package__ = "monitores.monitor"
