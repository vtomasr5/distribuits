from threads.master import Master
import sys


def main():
	len_parameter = (len(sys.argv) == 2)
	parameter = False
	if len_parameter:
		parameter = (sys.argv[1] in ('start', 'gen_log'))

	if not (len_parameter and parameter):
		print 'python simulacionv2.py <start|gen_log>'
		sys.exit(0)
	else:
		if sys.argv[1] == 'start':
			print 'start'
			m = Master(.5, 10, 'www.google.com')
			m.simular()
		else:
			print 'gen_log'

if __name__ == "__main__":
    main()
