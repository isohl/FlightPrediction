D710_startup="""# $Id: tnc-startup.d700,v 1.9 2006/06/07 14:18:13 we7u Exp $
#
# Copyright (C) 2004-2006  The Xastir Group
#
# TNC Init file for KENWOOD D700.  Also reported to work with the
# Alinco DR-135TP radio (with the EJ-41U TNC which also uses a Tasco
# TNC just like the Kenwoods).  Perhaps works with the Alinco DR-635
# radio (with the EJ-50U TNC) too.
#
# NOTE:  TXD on a D700A is fixed at 500ms (1/2 second) in "APRS"
# mode.  In "packet" mode we can change the txd to other values.
#
#
#Don't send CONTROL-C before this line
##META <no-ctrl-c>
TC 1
##Pause for one second
##META <delay>
##META <delay>
#Put the TNC in packet mode since this is where we want to end up
# Change the 1 to 0 to go to normal radio mode
##META <no-ctrl-c>
TNC 2
# Pause for one second
##META <delay>
##META <delay>
# Enable 4800 baud GPS
# Change to 2 for 9600 baud GPS
# Disable both the META line and the GU line for no change
##META <no-ctrl-c>
GU 1
# Pause for one second
##META <delay>
##META <delay>
#Turn off Terminal Control
##META <no-ctrl-c>
TC 0
# Pause for one second just in case
##META <delay>
##META <delay>
HID off
#CWID off
AWlen 8
BBSMsgs ON
B E 0
LOC E 0
Echo off
FLow off
AUTOLF off
MCOM off
MON ON
MRPt on
PACLen 128
PASSALL off
HBAUD 1200
TXDELAY 25
HEADERLN off
BEACON EVERY 0
# Delete following lines if without GPS
GBAUD 4800
GPSTEXT $GPRMC
LTMH OFF
LTM 10
#"""

D710_shutdown="""# $Id: tnc-stop.d700,v 1.3 2006/01/17 21:03:52 we7u Exp $
#
# Copyright (C) 2004-2006  The Xastir Group
#
#TNC STOP FILE
# Undo any settings make in tnc-startup.sys
# Edit this file for your tnc!
UNPROTO CQ
AUTOLF ON
ECHO ON
#Don't send CONTROL-C before this line
##META <no-ctrl-c>
TC 1
##Pause for one second
##META <delay>
##META <delay>
# Turn off AUX port
##META <no-ctrl-c>
GU 0
##META <delay>
#Put the TNC in internal mode since this is where we want to end up
# Change the 1 to 0 to go to normal radio mode
##META <no-ctrl-c>
TNC 1
# Pause for one second
##META <delay>
##META <delay>
# Enable 4800 baud GPS
# Change to 2 for 9600 baud GPS
# Disable both the META line and the GU line for no change
##META <no-ctrl-c>
GU 1
# Pause for one second
##META <delay>
##META <delay>
#Turn off Terminal Control
##META <no-ctrl-c>
#TC 0"""

import time
import serial

def run_tnc(ser,lines):
	ctrlC=chr(0x03)
	for line in lines.split("\n"):
		if line[0:2]=="##":
			if line=="##META <delay>":
				print "delaying"
				time.sleep(.5)
			elif line=="##META <no-ctrl-c>":
				print "NO-Ctrl-C"
				ctrlC=""
		elif line[0:1]=="#":
			print "\t\t", line
		else:
			print "command", line
			ser.write(ctrlC+line+"\r")
			ctrlC=chr(0x03)
def run_d710_tnc_shutdown(ser):
	run_tnc(ser,D710_shutdown)
def run_d710_tnc_startup(ser):
	run_tnc(ser,D710_startup)