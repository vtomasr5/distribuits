# coding: utf-8
from monitores.monitor import Monitor
import sys
import os

RESOLUCION   = 1 #Resolucion minima de Monitor
OUTPUT_DIR   = 'output'
METRICAS_DIR = 'metricas'
STOP_FILE    = 'exec.stop'


def return_path():
    return os.path.realpath(os.path.dirname(sys.argv[0]))

def return_path_salida(path):
    return  path + '/' + OUTPUT_DIR + '/'

def return_path_metricas(path):
    return  path + '/' + OUTPUT_DIR + '/' + METRICAS_DIR + '/'

def mkdir(path, directory_name):
    d = os.listdir(path)
    if directory_name not in d:
        os.mkdir(path+directory_name)

def shutdown_threads(threads):
    for thread in threads:
        thread.shutdown()

def wait_for_keyboard(threads, monitores, sufix):
    error = False
    try:
        path = return_path()
        d    = os.listdir(path)
        while STOP_FILE not in d: #Ejecutamos hasta tener STOP_FILE
            d = os.listdir(path)
    except KeyboardInterrupt:
        error = True
        shutdown_threads(threads)
    print "Ejecucion Finalizada"
    if not error:
        shutdown_threads(threads)
        make_csv_file(path, monitores, sufix)

def get_min_lines(path, monitores):
    min = sys.maxint  #9999999999999999
    for monitor in monitores:
        f = open(return_path_salida(path)+monitor+'.txt','r')
        f.seek(0)
        lines = sum(1 for line in f)
        if lines < min:
            min = lines
        f.close()
    return min

def make_csv_file(path, monitores, sufix):
    min         = get_min_lines(path, monitores)
    cabecera    = 'UTILIZACION;MEMORIA;BYTES ENVIADOS;BYTES RECIBIDOS;BYTES LEIDOS;BYTES ESCRITOS'
    files       = []
    filename    = 'metricas_'+str(sufix)+'.csv'

    mkdir(return_path_salida(path), METRICAS_DIR)
    output_path = return_path_metricas(path)

    output_file = open(output_path+filename,'w')
    output_file.write(cabecera+"\n")

    for monitor in monitores:
        f = open(return_path_salida(path)+monitor+'.txt','r')
        f.seek(0)
        files.append(f)

    for i in range(0, min):
        line_csv = ''
        for idx, monitor in enumerate(monitores):
            line     = files[idx].readline().split('\n')
            line_csv = line_csv + str(line[0]) + ';'
        output_file.write(line_csv[:-1]+"\n") #Quitamos el ; final

    for f in files:
        f.close()

    output_file.close()

def main():
    len_parameter = (len(sys.argv) == 2)
    if not len_parameter:
        print "Faltan parametros"
        sys.exit(0)

    sufix       = sys.argv[1]
    path        = return_path()+'/'
    print path
    mkdir(path, OUTPUT_DIR)
    path        = return_path_salida(path)
    threads     = []
    monitores   = ('cpu_monitor', 'memory_monitor', 'network_monitor', 'disk_monitor')

    if STOP_FILE in os.listdir(return_path()):
        os.remove(return_path()+'/'+STOP_FILE)

    for monitor in monitores:
        m = Monitor(monitor, RESOLUCION, path)
        threads.append(m)
        m.start()

    wait_for_keyboard(threads, monitores, sufix)

if __name__ == "__main__":
    main()
