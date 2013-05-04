from threads.master import Master
import sys
import ast
from estadisticas.estadistica import Estadistica

PASSWORD_WEB_METRICAS = '1234'

def show_help():
    print 'python simulacionv2.py <Opcion> <Argumentos>'
    print '     Argumentos:'
    print '         <Opcion>         : start | gen_log'
    print '     Opciones'
    print '         start   <numero de usuarios> <duracion en minutos>'
    print '         gen_log <numero de usuarios> <ID noticia Inicial> <noticias Totales>'
    sys.exit(0)

def is_param_int_or_float(param):
    try:
        return (type(ast.literal_eval(sys.argv[2]))  in (int, float))
    except ValueError:
        return False

def gen_traza(tamanyo, noticiaInicial, numNoticiasTotales):
    a = Estadistica(tamanyo, noticiaInicial, numNoticiasTotales)
    mSesion     = a.generaFicheroSesion()
    mPeticion   = a.generaFicheroPeticion()
    mLlegadas   = a.generaFicheroLlegadas()

    a.generaFicheroPopularidad()
    a.generaFicheroPeticionEsc()
    path = a._obtain_path()
    cabecera = "Media Tiempo entre Sesion;Media tiempo entre peticiones;Media tiempo entre llegadas\n"
    f = open(path+"medias.csv", 'w')
    f.write(cabecera)
    line = str(mSesion)+ ";" + str(mPeticion)+ ";" + str(mLlegadas)
    f.write(line)
    f.close
    print 'Traza Generada'

def simular(numUsuarios, duracion):
    print 'Ejecutando Simulacion...'
    print ''
    m = Master(duracion, numUsuarios, '130.206.134.123', PASSWORD_WEB_METRICAS)
    m.simular()
    print ''
    print 'Simulacion Finalizada!'

def main():
    len_parameter   = (len(sys.argv) >= 3)
    option          = False
    last_parameter  = False

    if len_parameter:
        option         = (sys.argv[1] in ('start', 'gen_log'))
        last_parameter = is_param_int_or_float(sys.argv[2])

    if not (len_parameter and option and last_parameter):
        show_help()
    else:
        if sys.argv[1] == 'start':
            if (not is_param_int_or_float(sys.argv[2])) or  len(sys.argv) > 4:
                show_help()

            simular(float(sys.argv[2]), int(sys.argv[3]))
        else: #Generamos la traza
            len_parameter = (len(sys.argv) == 5)
            if len_parameter:
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[3]))
                len_parameter = (len_parameter and is_param_int_or_float(sys.argv[4]))
            if not len_parameter:
                show_help()

            gen_traza(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

if __name__ == "__main__":
    main()
