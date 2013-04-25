from threads.master import Master
import sys
from estadisticas.estadistica import Estadistica


def main():
    len_parameter = (len(sys.argv) == 3)
    parameter = False

    noticiaInicial     = 2826
    numNoticiasTotales = 56

    if len_parameter:
        parameter = (sys.argv[1] in ('start', 'gen_log'))

    if not (len_parameter and parameter):
        print 'python simulacionv2.py start <tiempo simulacion en minutos>'
        print 'python simulacionv2.py gen_log'
        sys.exit(0)
    else:
        if sys.argv[1] == 'start':
            print 'Empezando Simulacion...'
            print '-------------------------------------'
            m = Master(float(sys.argv[2]), '130.206.134.123', noticiaInicial, numNoticiasTotales)
            m.simular()
            print '-------------------------------------'
            print 'Simulacion Finalizada'
        else:
            a = Estadistica(1000, noticiaInicial, numNoticiasTotales)
            a.generaFicheroLlegadas()
            a.generaFicheroPopularidad()
            a.generaFicheroSesion()
            a.generaFicheroPeticion()
            print 'Traza Generada'

if __name__ == "__main__":
    main()
