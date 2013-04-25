from threads.master import Master
import sys, ast
from estadisticas.estadistica import Estadistica

def show_help():
    print 'python simulacionv2.py <Opcion> <Argumentos>'
    print '     Argumentos:'
    print '         <Opcion>         : start | gen_log'
    print '     Opciones'
    print '         start   <duracion en minutos> <numero de usuarios>'
    print '         gen_log <numero de usuarios> <ID noticia Inicial> <noticias Totales>'
    sys.exit(0)

def is_param_int_or_float(param):
    try:
        return (type(ast.literal_eval(sys.argv[2]))  in (int, float))
    except ValueError:
        return False

def gen_traza(tamanyo, noticiaInicial, numNoticiasTotales):
    a = Estadistica(tamanyo, noticiaInicial, numNoticiasTotales)
    a.generaFicheroLlegadas()
    a.generaFicheroPopularidad()
    a.generaFicheroSesion()
    a.generaFicheroPeticion()
    print 'Traza Generada'

def simular(numUsuarios, duracion):
    print 'Ejecutando Simulacion...'
    print ''
    m = Master(duracion, numUsuarios, '130.206.134.123')
    m.simular() 
    print ''
    print 'Simulacion Finalizada!'

def main():
    len_parameter         = (len(sys.argv) >= 2)
    option                = False
    last_parameter        = False

    if len_parameter:
        option  = (sys.argv[1] in ('start', 'gen_log'))
        try:
            last_parameter = is_param_int_or_float(sys.argv[2])
        except ValueError:
            last_parameter = False

    if not (len_parameter and option and last_parameter):
        show_help()
    else:
        if sys.argv[1] == 'start':
            if len(sys.argv) > 4:
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
