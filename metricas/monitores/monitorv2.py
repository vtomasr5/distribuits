# coding: utf-8
import psutil as ps


class Monitor():
	def __init__(self, path):
		self.path = path

	def cpu_monitor(self, f):
		s = ps.cpu_percent()
		print("CPU:" + str(s))
		f.write(str(s)+"\n")

	def memory_monitor(self, f):
		s = ps.virtual_memory()[2]
		print("Consumo Memoria: " + str(s))
		f.write(str(s)+"\n")

	def network_monitor(self, f):
		"""
			Packets sent or received
		"""
		sent = ps.network_io_counters()[0]
		received = ps.network_io_counters()[1]
		print("Network: Sent: " +str(sent)+ ", Received: " + str(received))
		f.write(str(sent)+","+str(received)+"\n")

	def disk_monitor(self, f):
		"""
			Bytes read or write in a disk
		"""
		read = ps.disk_io_counters()[2]
		write = ps.disk_io_counters()[3]
		print("Disk Read: " +str(read)+ ", Write: " + str(write))
		f.write(str(read)+","+str(write)+"\n")

if __name__ == "__main__" and __package__ is None:
    __package__ = "monitores.monitor"
