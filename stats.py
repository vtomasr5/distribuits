#!/usr/bin/python
from meneame.obtenerEstadisticas import obtenerEstadisticas
from meneame.utils import get_path
from meneame.properties import MENEAME_BASE_RSS
from meneame.properties import MENEAME_COMENTARIOS_RSS
from meneame.properties import MENEAME_PENDIENTES_RSS
from meneame.properties import DIROUT
import os
import datetime
import time

#FIXED PARAMETERS
MINUTES = 10		#CADA CUANTO SE VA A EJECUTAR
NUMBER_OF_DAYS = 1  #CUANTOS DIAS SE VA A EJECUTAR

SLEEP = 60*MINUTES

end = datetime.datetime.now() + datetime.timedelta(days=NUMBER_OF_DAYS)


while datetime.datetime.now() < end:
	# check if exists output dir
	path = get_path()
	d = os.listdir(path)
	if DIROUT not in d:
	    os.mkdir(DIROUT)

	stats_base 		  = obtenerEstadisticas(path, MENEAME_BASE_RSS)
	stats_comentarios = obtenerEstadisticas(path, MENEAME_COMENTARIOS_RSS)
	stats_pendientes  = obtenerEstadisticas(path, MENEAME_PENDIENTES_RSS)

	stats_base.getStats()
	stats_comentarios.getStats()
	stats_pendientes.getStats()
	print "Durmiendo..."
	time.sleep(SLEEP) #Sleep 5 minutos

