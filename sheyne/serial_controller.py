import serial
from glob import glob
from time import sleep

def command(s, msg):
	s.write('%s\r' % msg)

def init(s):
	s.write('\x03')
	s.write('\x02')
	command(s, 'TC 1')
	command(s, 'TN 2,0')
	command(s, 'GU 1')
	command(s, 'TC 0')
	s.write('\x03')


def monitor(s):
	command(s, 'E OFF')
	command(s, 'M ON')

def shutdown(s):
	pass


with serial.Serial(glob("/dev/tty.PL2303-*")[0]) as ser:
	try:
		ser.timeout = 1
		
		def read(ser):
			got=ser.read()
			out=""
			while got!="\r" and got!="":
				out+=got
				got=ser.read()
			return out
		
		init(ser)
		print ser
		ser.write('E OFF\rM ON\r')
		while 1:
			r = read(ser)
			if r != '':
				print r.strip()
	finally:
		shutdown(ser)
