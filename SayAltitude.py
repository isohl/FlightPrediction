import pyttsx
import fap
import os
from math import *
import time

def getNewPacket(savedtime):
    global filepath
    for i in range(100):
        time = os.stat(filepath)
        if time == savedtime:
            continue
        savedtime = time
        f = open(filepath)
        #print "Retrieving data"
        allLines = f.readlines()
        while allLines == []:
            allLines = f.readlines()
        lastline = allLines[len(allLines)-1]
        f.close()
        return lastline, savedtime
    return None,savedtime
    

def checkCompatibility(packet):
    acceptedSigns = ["KE7ROS","WB1SAR","KF7WII","KF7WIG","KF7WIJ"]
    src = packet.src_callsign.strip("-11")
    #src = src.strip("-7")
    if src in acceptedSigns:
        return True
    else:
        return False

def sayAltitude(packet,ascentrate=0):
    alt = packet.altitude
    src = packet.src_callsign
    if alt is not None:
        alt = int(floor(alt/1000*3.28084)*1000)
        text = "Balloon currently at %d feet" % (int(alt))
        if ascentrate is not 0:
            text2 = "Ascent Rate is %d Feet per minute" % ascentrate
        engine.say(text)
        #engine.say(text2)
        engine.runAndWait()
        print "Said"

def sayBearing():
    pass


if __name__=="__main__":    
    engine = pyttsx.init()
    #engine.say('Altitude speech engine starting')
    #engine.runAndWait()
    fap.init()
    if os.name=="nt":
        filepath = os.path.expanduser('~')+"\\tnclogs\\tnc.log"
    elif os.name=="posix":
        filepath = os.path.expanduser("~/Documents/tnc.log")
    else:
        print "UNKNOWN OPERATING SYSTEM. GET A LIFE."
    savedtime=os.stat(filepath).st_mtime
    ascentrate = 0
    lasttime = time.time()
    lastpacket = None
    lastpackettime = None
    try:
        while 1:
            newpacket,savedtime = getNewPacket(savedtime)
            if not newpacket==None:
                try:
                    p = fap.Packet(newpacket)
                except fap.DecodeError:
                    continue
                compatible = checkCompatibility(p)
                #compatible = True
                if compatible:
                    if lastpacket is not None:
                        lastalt = lastpacket.altitude
                        if not lastalt==p.altitude:
                            currentpackettime = time.time()
                            ascentrate = floor(((p.altitude-lastalt)*3.28084)/((currentpackettime-lastpackettime)/60)/100)*100
                    lastpacket = p
                    lastpackettime = time.time()
                    
            curtime = time.time()
            if curtime-lasttime>30:
                if not lastpacket == None:
                    sayAltitude(lastpacket,ascentrate)
                lasttime = curtime
    except KeyboardInterrupt:
        print "KeyBoardInterrupt"
        pass
    finally:
        fap.cleanup()
