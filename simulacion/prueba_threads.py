from master import Master
from time import sleep

m = Master()

print 'Creand todos los hilos...'
for i in range(1, 10):
	url = 'http://www.google.es'
	sesionTime = 0
	consumptionTime = 0
	
	m.add_client(url, sesionTime, consumptionTime)
	ident = m.get_last_client()

	m.messato_to_client(ident, 'Soy un nuevo hilo')

print 'Proceso finalizado...'
sleep(10)
print 'Eliminando hilos...'
for i in range(1, 10):
	m.remove_client(i)

print 'Hilos eliminados...'