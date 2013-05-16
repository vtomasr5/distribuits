import sys
import os
import numpy
import random
import re

class tratamiento_metricas(object):

    def __init__(self):
        self.path = "/Metricas/"

    def _obtain_path(self):
        return os.path.realpath(os.path.dirname(sys.argv[0])) + self.path


    def sort_nicely(self,l ): 
        convert = lambda text: int(text) if text.isdigit() else text 
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        l.sort( key=alphanum_key)

    def tot(self):
        cabecera    = 'UTILIZACION,MEMORIA,BYTES ENVIADOS,BYTES RECIBIDOS,BYTES LEIDOS,BYTES ESCRITOS'
        files       = []
        filename    = 'medias_metricas.csv'

        output_file = open(filename,'w')
        output_file.write(cabecera+"\n")

        utilizacion = []
        memoria = []
        b_enviados = []
        b_recibidos = []
        b_leidos = []
        b_escritos = []

        path = self._obtain_path()
        d = os.listdir(path)
        self.sort_nicely(d)

        for item in d: 
            if item[-3:] == "csv":
                utilizacion,memoria,b_enviados,b_recibidos,b_leidos,b_escritos=self.csv(item)           
                output_file.write(str(utilizacion)+","+str(memoria)+","+str(b_enviados)+","+str(b_recibidos)+","+str(b_leidos)+","+str(b_escritos)+"\n")
        
            
    def suma_lista(self,l):
        sum = 0
        for i in range(len(l)):
            sum = sum + l[i]
        return sum

    def csv(self, filename):
        f = open(self._obtain_path()+filename, 'r')
        l = f.readlines()
        utilizacion = []
        memoria = []
        b_enviados = []
        b_recibidos = []
        b_leidos = []
        b_escritos = []
        
        for item in l[1:]:
            s = item[:-1].split(';')
            if len(s) == 6:
                utilizacion.append(float(s[0]))
                memoria.append(float(s[1]))
                b_enviados.append(float(s[2]))
                b_recibidos.append(float(s[3]))
                b_leidos.append(float(s[4]))
                b_escritos.append(float(s[5]))
        f.close()

        media_utilizacion = numpy.mean(utilizacion)
        media_memoria = numpy.mean(memoria)
        media_b_enviados = numpy.mean(b_enviados)
        media_b_recibidos = numpy.mean(b_recibidos)
        media_leidos = numpy.mean(b_leidos)
        media_b_escritos = numpy.mean(b_escritos)

        return media_utilizacion, media_memoria,media_b_enviados,media_b_recibidos,media_leidos,media_b_escritos


if __name__=='__main__':  #Cuerpo Principal
    o = tratamiento_metricas()
    o.tot()