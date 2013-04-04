from estadistica import Estadistica

a = Estadistica(1000)
a.generaFicheroLlegadas()
a.generaFicheroPopularidad()
a.generaFicheroSesion()
a.generaFicheroPeticion()

for i in range(0,0):
	print a.obtenerLlegada()
	print a.obtenerPeticion()
	print a.obtenerPopularidad()
	print a.obtenerSesion()
