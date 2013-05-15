from threads.master import Master
import sys
import ast
from estadisticas.estadistica import Estadistica
from time import sleep

PASSWORD_WEB_METRICAS = '1234'
TRANSITORIO           = 0

def show_help():
    print 'python simulacion.py <Opcion> <Argumentos>'
    print '     Argumentos:'
    print '         <Opcion>          start | gen_log | auto'
    print '     Opciones'
    print '         auto    <numero de usuarios> <duracion en minutos> <ID noticia Inicial> <noticias Totales>'
    print '         gen_log <numero de usuarios> <ID noticia Inicial> <ID noticia Final>'
    print '         start   <numero de usuarios> <duracion en minutos>'
    print '     Ejemplo:'
    print '         python simulacion.py auto 100000 45 2826 2932'
    sys.exit(0)

def is_param_int_or_float(param):
    try:
        return (type(ast.literal_eval(sys.argv[2]))  in (int, float))
    except ValueError:
        return False

def escribir_medias(path, mSesion, mPeticion, mLlegadas, sufix=''):
    cabecera = "Media Tiempo entre Sesion,Media tiempo entre peticiones,Media tiempo entre llegadas\n"
    f = open(path+"medias_"+sufix+".csv", 'w')
    f.write(cabecera)
    line = str(mSesion)+ "," + str(mPeticion)+ "," + str(mLlegadas)
    f.write(line)
    f.close

def automode(usuarios, duracion, noticiaInicial, noticiaFinal):
    a          = Estadistica(usuarios, noticiaInicial, noticiaFinal)
    print 'Generadando Traza ...'
    path       = a._obtain_path()
    mSesion    = a.generaFicheroSesion()
    mPeticion  = a.generaFicheroPeticion()
    a.generaFicheroPopularidad()
    a.generaFicheroPeticionEsc()
    print 'Traza Generada...'
    mu         = a.obtenerMu()
    contadorMu = 0

    while mu != "":
        print 'Generando Tiempo de Llegadas...'
        mLlegadas = a.generaFicheroLlegadas(sufix=str(contadorMu),mu=mu)
        escribir_medias(path, mSesion, mPeticion, mLlegadas, str(contadorMu))
        print 'Tiempo de Llegadas Generado...'
        print 'Simulando...'
        simular(usuarios, duracion,str(contadorMu), path)
        contadorMu = contadorMu + 1
        mu = a.obtenerMu()
        print ''
        sleep(1) #Dormimos 1 minuto entre simulacion y simulacion

def gen_traza(tamanyo, noticiaInicial, noticiaFinal,sufix):
    a           = Estadistica(tamanyo, noticiaInicial, noticiaFinal)
    mSesion     = a.generaFicheroSesion()
    mPeticion   = a.generaFicheroPeticion()
    mLlegadas   = a.generaFicheroLlegadas(str(sufix))

    a.generaFicheroPopularidad()
    a.generaFicheroPeticionEsc()
    path = a._obtain_path()
    escribir_medias(path, mSesion, mPeticion, mLlegadas)
    print 'Traza Generada'

def simular(numUsuarios, duracion, sufijo, path_estadisticas=''):
    print 'Ejecutando Simulacion...'
    print ''
    m = Master(duracion, numUsuarios, '130.206.134.123', PASSWORD_WEB_METRICAS, TRANSITORIO, sufijo, path_estadisticas)
    m.simular()
    print ''
    print 'Simulacion Finalizada!'

def main():
    len_parameter   = (len(sys.argv) >= 3)
    option          = False
    last_parameter  = False
    sufijo_metricas = '1'

    if len_parameter:
        option         = (sys.argv[1] in ('start', 'gen_log', 'auto'))
        last_parameter = is_param_int_or_float(sys.argv[2])

    if not (len_parameter and option and last_parameter):
        show_help()
    else:
        if sys.argv[1] == 'start':
            len_parameter = (len(sys.argv) == 4)
            if len_parameter:
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[2]))
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[3]))
            if not len_parameter:
                show_help()

            simular(float(sys.argv[2]), int(sys.argv[3]), sufijo_metricas)
        elif sys.argv[1] == 'gen_log': #Generamos la traza
            len_parameter = (len(sys.argv) == 5)
            if len_parameter:
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[3]))
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[4]))
            if not len_parameter:
                show_help()

            gen_traza(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),sufijo_metricas)
        else:
            len_parameter = (len(sys.argv) == 6)
            if len_parameter:
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[2]))
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[3]))
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[4]))
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[5]))
            if not len_parameter:
                show_help()

            automode(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))

    sys.exit(0) #Terminando con todos los threads creados
if __name__ == "__main__":
    main()
