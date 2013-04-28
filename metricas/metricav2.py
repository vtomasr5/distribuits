# coding: utf-8
from monitores.monitor import Monitor
import sys
import os

RESOLUCION = 1 #Resolucion minima de Monitor
OUTPUT_DIR = 'output'
STOP_FILE  = 'exec.stop'


def return_path():
	return os.path.realpath(os.path.dirname(sys.argv[0]))

def return_path_salida(path):
	return  path + '/' + OUTPUT_DIR + '/'

def mkdir():
	path = return_path()
	d = os.listdir(path)
	if OUTPUT_DIR not in d:
		os.mkdir(OUTPUT_DIR)
	return  return_path_salida(path)

def shutdown_threads(threads):
	for thread in threads:
			thread.shutdown()

def wait_for_keyboard(threads, monitores):
	error = False
	try:
		path = return_path()
		d 	 = os.listdir(path)
		while STOP_FILE not in d: #Ejecutamos hasta tener STOP_FILE
			d = os.listdir(path)
	except KeyboardInterrupt:
		error = True
		shutdown_threads(threads)
	print "Ejecucion Finalizada"
	if not error:
		shutdown_threads(threads)
		make_csv_file(path, monitores)

def get_min_lines(path, monitores):
	min = 9999999999999999
	for monitor in monitores:
		f = open(return_path_salida(path)+monitor+'.txt','r')
		f.seek(0)
		lines = sum(1 for line in f)
		if lines < min:
			min = lines
		f.close()
	return min

def make_csv_file(path, monitores):
	min = get_min_lines(path, monitores)
	cabecera = 'UTILIZACION;MEMORIA;BYTES ENVIADOS;BYTES RECIBIDOS;BYTES LEIDOS;BYTES ESCRITOS'
	files = []
	output_file = open(return_path_salida(path)+'metricas.csv','w')
	output_file.write(cabecera+"\n")
	for monitor in monitores:
		f = open(return_path_salida(path)+monitor+'.txt','r')
		f.seek(0)
		files.append(f)

	for i in range(0, min):
		line_csv = ''
		for idx, monitor in enumerate(monitores):
			line 	 = files[idx].readline().split('\n')
			line_csv = line_csv + str(line[0]) + ';'
		output_file.write(line_csv[:-1]+"\n") #Quitamos el ; final

	for f in files:
		f.close()

	output_file.close()

def main():
	path 		= mkdir()
	threads 	= []
	monitores 	= ('cpu_monitor', 'memory_monitor', 'network_monitor', 'disk_monitor')

	if STOP_FILE in os.listdir(return_path()):
		os.remove(return_path()+'/'+STOP_FILE)

	for monitor in monitores:
		m = Monitor(monitor, RESOLUCION, path)
		threads.append(m)
		m.start()

	wait_for_keyboard(threads, monitores)

if __name__ == "__main__":
    main()
