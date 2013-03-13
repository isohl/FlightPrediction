import serial
import datetime
import time
import D710_start_stop
from glob import glob
import os

"""Currently, the pyserial module is located in the same folder as the program,
        If that is ever not the case, or must be changed, then pyserial must be installed,
        The window's binary of which is located in the same folder as this file"""


if os.name=="posix": #Posix is the special name for Unix (Mac)
        try:
            try:
                ser=serial.Serial("/dev/tty.usbserial") #Which of these works will determine on which drivers you have
            except serial.serialutil.SerialException:
                ser=serial.Serial(glob("/dev/tty.PL2303-*")[0])
        except:
                print "Error Connecting to Device" #If you get this, either the device is not responding or is not plugged in
                import sys
                sys.exit()
        filepath = os.path.expanduser("~/Documents/tnc.log")
        log=open(filepath,"a") #This opens the log, change it to whichever file you like
        log.close()
elif os.name=="nt": #NT is the special name for Windows
        #The best way to determine what the port is, is to open Device manager and look under COM
        comport = raw_input("What is the name of the COM Port? (COM1, etc) ")
        try:
                ser=serial.Serial(comport)
        except IndexError:
                print "Serial Device not connected" #Again, if this isn't working, make sure its plugged in
        try:
                filepath = os.path.expanduser(os.path.join('~','tnclogs','tnc.log'))
                log=open(filepath,"a")
        except IOError: #This will only ever have problems if the folder defined doesn't exist
                os.mkdir(os.path.expanduser(os.path.join('~','tnclogs')))
                log=open(os.path.expanduser(os.path.join('~','tnclogs','tnc.log')),"a")
        log.close()
#This will run the main startup sequence, which consists of sending a large amount of gibberish to the D710
D710_start_stop.run_d710_tnc_startup(ser)

try:                #This entire try statement is a complicated way of pulling data 
        while 1:    #   off of the D710 and attaching a time stamp to it in the file
                log=open(filepath,"a")
                got=ser.read()
                out=""
                while got!="\r":
                        out+=got
                        got=ser.read()
                if out!="":
                        currentTimestamp="# "+str(int(round(time.time())))+datetime.datetime.now().strftime(" %a %b %d %H:%M:%S %Z %Y")
                        print currentTimestamp
                        print out
                        log.write(currentTimestamp+"\n")
                        log.write(out+"\n")
                        log.flush()
                        log.close()
except:#In case off failure, or even a keyboard interrupt, this will shut down the port.
        D710_start_stop.run_d710_tnc_shutdown(ser)
        log.close()
        ser.close()
        raise


