import decodeTNC
import pyttsx
import fap
import os
from math import *
import time

earth_radius = 3960.0
degrees_to_radians = pi/180.0
radians_to_degrees = 180.0/pi

def milechangelatitude(change):
    return radians(change)*earth_radius

def milechangelongitude(latitude, change):
    r = earth_radius*cos(radians(latitude))
    return radians(change)*r


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
    #acceptedSigns = ["KE7ROS","WB1SAR","KF7WII","KF7WIG","KF7WIJ"]
    acceptedSigns = ["KF7WIG-11", "WB1SAR-11"]
    #src = packet.src_callsign.strip("-11")
    src = packet.src_callsign
    #src = src.strip("-7")
    if src in acceptedSigns:
        return True
    else:
        return False

def sayAltitude(packet,ascentrate=0,bearing = (0,0), calledlast = False):
    alt = packet.altitude
    src = packet.src_callsign
    if alt is not None:
        alt = int(floor(alt/1000*3.28084)*1000)
        text = "Balloon currently at %s feet" % (int(alt))
        print text
        if ascentrate is not None and int(ascentrate) is not 0:
            text2 = "Ascent Rate is %s Feet per minute" % ascentrate
            print text2
            engine.say(text2)
        if not bearing == (0,0) and not calledlast:
            text3 = "Bearing is %s degrees azimuth and %s degrees altitude" % bearing
            print text3
            engine.say(text3)
        engine.say(text)
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
    ascentaverage = None
    lasttime = time.time()
    lastpacket = None
    lastpackettime = None
    bearing = (0,0)
    calledlast = True
    try:
        while 1:
            newpacket,savedtime = getNewPacket(savedtime)
            if not newpacket==None:
                try:
                    p = fap.Packet(newpacket)
                    
                    compatible = checkCompatibility(p)
                    #compatible = True
                    if compatible:
                        if lastpacket is not None:
                            lastalt = lastpacket.altitude
                            if not lastalt==p.altitude:
                                currentpackettime = time.time()
                                ascentrate = floor(((p.altitude-lastalt)*3.28084)/((currentpackettime-lastpackettime)/60)/100)*100
                                if ascentaverage is None:
                                    ascentaverage = ascentrate
                                else:
                                    ascentaverage = int(floor((ascentaverage+ascentrate)/2/100)*100)
                        lastpacket = p
                        lastpackettime = time.time()
                except fap.DecodeError:
                    #newpacket = str("TEST1>TEST:")+newpacket
                    #try:
                        #p = fap.Packet(newpacket)
                    #except fap.DecodeError:
                        #continue
                    if lastpacket is not None and newpacket.startswith("$PKWDPOS"):
                        latitude, longitude = decodeTNC.latlong(newpacket)
                        longitudediff = float(longitude) - lastpacket.longitude
                        latitudediff = float(latitude) - lastpacket.latitude
                        groundalt = 5800
                        packagealt = lastpacket.altitude
                        xdiff = milechangelongitude(float(latitude),longitudediff)
                        ydiff = milechangelatitude(latitudediff)
                        angle = 360 + int(degrees(atan2(ydiff,xdiff)))
                        distance = hypot(xdiff,ydiff)
                        fromhorizon = int(degrees(atan(packagealt/distance)))
                        bearing = (angle,fromhorizon)
                        continue                
                    
            curtime = time.time()
            if curtime-lasttime>30:
                if not lastpacket == None:
                    sayAltitude(lastpacket,ascentaverage,bearing,calledlast)
                    if calledlast:
                        calledlast = False
                        pass
                    else:
                        calledlast = True
                lasttime = curtime
    except KeyboardInterrupt:
        print "KeyBoardInterrupt"
        pass
    finally:
        fap.cleanup()
