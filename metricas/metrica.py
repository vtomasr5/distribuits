# coding: utf-8

import psutil as ps
import threading
import time


def mesura_cpu():
    print "CPU usage: " + str(ps.cpu_percent(interval=1)) + "%"


def mesura_mem():
    """
        Memory available
    """
    print "Mem usage: " + str(ps.virtual_memory()[2]) + "%"


def mesura_net():
    print "Bytes sent: " + str(ps.network_io_counters()[0])
    print "Bytes received: " + str(ps.network_io_counters()[1])


def mesura_disk():
    print "Read bytes: " + str(ps.disk_io_counters()[2])
    print "Write bytes: " + str(ps.disk_io_counters()[3])


def handler(mesura):
    if mesura == 'cpu':
        mesura_cpu()
    elif mesura == 'mem':
        mesura_mem()
    elif mesura == 'net':
        mesura_net()
    elif mesura == 'disk':
        mesura_disk()
    else:
        raise NameError("Parametre incorrecte")

# Main
threads = []
m = ('cpu', 'mem', 'net', 'disk')
for i in m:
    t = threading.Thread(target=handler, args=(i,))  # NO llevar sa coma de i,
    threads.append(t)
    time.sleep(0.02)
    t.start()
