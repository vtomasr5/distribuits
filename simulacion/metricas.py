# coding: utf-8

import psutil as ps
import threading


def mesura():
    print str(ps.cpu_percent()) + "%"

# Main
threads = []
for i in range(5):
    t = threading.Thread(target=mesura)
    threads.append(t)
    t.start()
