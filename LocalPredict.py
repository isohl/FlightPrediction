from __future__ import division
from Tkinter import *
from math import *
import time
import datetime
import urllib2
import writetoKML


earth_radius = 3960.0
degrees_to_radians = pi/180.0
radians_to_degrees = 180.0/pi

def change_in_latitude(miles):
    "Given a distance north, return the change in latitude."
    return degrees(miles/earth_radius)

def change_in_longitude(latitude, miles):
    "Given a latitude and a distance west, return the change in longitude."
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius*cos(radians(latitude))
    return degrees(miles/r)

def req(url,mode=False):
    try:
        if mode==True:
            proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
            opener = urllib2.build_opener(proxy_support)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        else:
            opener = urllib2.build_opener()
        return opener.open(url).read()
    except urllib2.HTTPError:
        print "Non-existant"
        return None
    except urllib2.URLError:
        print "URL Error"

def getData(launchtime,wxstation,source="GFS"):
    #forecasttimes = [0, 1, 3, 6, 9, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 144, 168, 192]
    #monthnames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rightnow = datetime.datetime.now()
    timedifference = launchtime-rightnow
    hourdifference = int(timedifference.total_seconds()/3600)
    #forecast = min([(abs(hourdifference-x), x) for x in forecasttimes])[1]
    forecast = int(hourdifference/3)*3
    #print "\t%s hours out" % (forecast)
    #if forecast == 0:
        #forecast=1
    url = """http://rucsoundings.noaa.gov/get_soundings.cgi?data_source=%s;
    n_hrs=1;
    fcst_len=%d;
    airport=%s;
    text=Ascii%%20text%%20%%28GSD%%20format%%29;
    hydrometeors=false&start=latest""" % (source,forecast,wxstation)
    #print url
    url = url.replace("\n    ","")
    data = req(url)
    #print data
    return data

def getDataFromFile(filename="./WindData.sohl"):
    aFile = open(filename,"r")
    data = aFile.read()
    aFile.close()
    return data

def saveDataToFile(filename="./WindData.sohl",data=None):
    if data==None:
        return False
    aFile = open(filename,"w")
    aFile.write(data)
    aFile.close()
    return True

def getClosestStation(launchsite=None, wxStation=None, filename="./StationData.sohl"):
    aFile = open(filename,"r")
    stations = eval(aFile.read())
    aFile.close()
    stationdifference = []
    closest = None
    if launchsite != None:    
        for station in stations:
            stationdifference.append((abs(launchsite[0]-stations[station]["position"][0])+abs(launchsite[1]-stations[station]["position"][1]),station))
        closest = (min(stationdifference)[1],stations[min(stationdifference)[1]])
        return stations, closest
    elif wxStation != None:
        closest = stations[wxStation]
        return stations, closest
    return stations
    

def parse_wind(data):
    byline = data.split("\n")
    parsed_data = []
    for line in byline:
        bycolumn = line.split()
        if len(bycolumn)>6 and bycolumn[0] in ('4','5','6','7','8','9'):
            #print bycolumn[2],bycolumn[5],bycolumn[6]
            if 99999 in [bycolumn[2],bycolumn[5],bycolumn[6]]:
                continue
            parsed_data.append((bycolumn[2],bycolumn[5],bycolumn[6]))
    return parsed_data

def parse_wind_baltrak(data):
    byline = data.split("\n")
    parsed_data = []
    for line in byline:
        bycolumn = line.split()
        #print bycolumn[1],bycolumn[4],bycolumn[5]
        parsed_data.append((bycolumn[1],int(float(bycolumn[4])),float(bycolumn[5])*1.94384449))
    return parsed_data    

def makeTrack(atmosphere,launchsite,ascentrate,descentrate,burstaltitude,station,direction="up"):
    #Whatever adds on stuff to the beginning
    #Add launchaltitude onto beginning and pull out entries lower than it, giving it the wind of the one right below it
    #atmosphere.insert(0,launchsite[2])
    atmosphere = [(int(float(x[0])*3.2808399),int(x[1]),(float(x[2])*101.268591)) for x in atmosphere]
    balloonlevel = min([(launchsite[2]-i[0],i) for i in atmosphere if launchsite[2]>=i[0]] or [(0,None)])[1]
    groundlevel = getClosestStation(launchsite=launchsite)[1][1]["position"]
    atmosphere = [x for x in atmosphere if (x[0]<burstaltitude and x[0]>groundlevel[2])]
    if direction=="up" and balloonlevel != None:
        atmosphere.insert(0,(launchsite[2],balloonlevel[1],balloonlevel[2]))
    trail = [launchsite]
    first = True
    totalxdist = 0
    totalydist = 0
    number = [1,2]
    if direction=="down":
        number = [1]
        atmosphere.reverse()
        atmosphere.pop(0)
        first = False        
    for levels in number:
        for level in range(len(atmosphere)):
            altitude = atmosphere[level][0]
            if first==True and altitude<launchsite[2]:
                continue
            windir = 90 - (atmosphere[level][1]+180)
            #windir = 180 - atmosphere[level][1]
            windmag = atmosphere[level][2]
            if level+1<len(atmosphere):
                nextaltitude = atmosphere[level+1][0]
            else:
                if first is True:
                    nextaltitude = burstaltitude
                else:
                    nextaltitude = launchsite[2]
            deltaalt = abs(nextaltitude-altitude)
            if first is True:
                deltatime = deltaalt/ascentrate
            else:
                deltatime = deltaalt/descentrate
            distancetraveled = deltatime*windmag
            xdist = distancetraveled*cos(radians(windir))/5280
            ydist = distancetraveled*sin(radians(windir))/5280
            #print "xdist: %s, ydist: %s" % (xdist,ydist)
            latitudechange = change_in_latitude(ydist)
            longitudechange = change_in_longitude(trail[-1][0],xdist)
            #Add to existing values
            newpos = (trail[-1][0]+latitudechange,trail[-1][1]+longitudechange,nextaltitude)
            trail.append(newpos)
            totalxdist+=xdist
            totalydist+=ydist
        atmosphere.reverse()
        atmosphere.pop(0)
        first = False 
    return trail

def findLanding(track,launchsite):
    #Pulls landing coordinates and an extremely rough bearing measurement
    landing = track[-1]
    """THESE ARE IN DEGREES (CONVERT)"""
    xdist = landing[1]-launchsite[1]
    ydist = landing[0]-launchsite[0]
    totaldist = hypot(xdist,ydist)
    angle = atan2(ydist,xdist)
    if ydist>0:
        if xdist>0:
            angle = 90 - angle
        else:
            angle = 450 - angle
    else:
        angle = 90 + abs(angle)
    return landing,(totaldist,angle)

def main(launchtime=None,launchsite=(40.149089,-110.127036,5826),ascentrate=1045,descentrate=1763,burstaltitude=98000,
         wxstation=None,source="GFS",messages=False,direction="up",writefile="Prediction.kml"):
    if launchtime==None:
        launchtime = datetime.datetime.now()
    if wxstation==None:
        stationlist, wxstation=getClosestStation(launchsite)
        wxstation=wxstation[0]
        if messages: print "WxStation: %s" % wxstation
    if messages: print "Retrieving Data..."
    data = getData(launchtime,wxstation,source)
    if messages: print "\t...Done"
    if messages: print "Parsing Data"
    if data=="" or data==None:
        print "No Data, Loading from File...\n*** Warning, this data may be out of date ***"
        data = getDataFromFile()
    else:
        saveDataToFile(data=data)
    atmosphere = parse_wind(data)
    if messages: print "Simulating Balloon Flight"
    track = makeTrack(atmosphere,launchsite,ascentrate,descentrate,burstaltitude,wxstation,direction=direction)
    if messages: print "\t...Done"
    else: return track
    landing,bearing = findLanding(track,launchsite)
    #for point in track:
       #print "%s\t%s" % (point[0],point[1])
        #print "%s,%s,%s" % (point[1],point[0],point[2]) #Google Earth
        #print "{%s,%s}," % (point[0],point[1]) #Mathematica
    if messages: print "Balloon landed at Latitude: %s, Longitude: %s" % (landing[0],landing[1])
    if messages: print "\tand %s miles from start at %s degrees East of North" % (bearing[0],bearing[1])
    earthtrack = []
    for point in track:
        earthtrack.append((point[1],point[0],point[2]))
    if messages: writetoKML.rewrite(earthtrack,writefile)
    if messages: print "Written to file"

if __name__=="__main__":
    #The time of balloon release (minutes and seconds allowed but not used)
    launchtime = datetime.datetime(year=2012,month=7,day=22,hour=9,minute=0)
    #The place of balloon release. (Latitude, Longitude, Altitude) *Decimal Degrees and Feet*
    launchsite = (40.149089,-110.127036,5826)
    #Ascent rate in feet per minute
    ascentrate = 1045
    #Descent rate in feet per minute
    descentrate = 1763
    #Burst Altitude in feet above sea level
    burstaltitude = 98000
    #burstaltitude = 80000
    #The closest weather station (http://nearspaceventures.com/w3Baltrak/htdocs/stationlist.html)
    wxstation = "VEL"
    #The datasource you want to use, recommended: GFS
    source = "GFS"
    main(launchtime,launchsite,ascentrate,descentrate,burstaltitude,wxstation,source,messages=True)
    #datas = []
    #altdatas = []
    ##sources = ["NAM","Op40","Bak40","FIM","RR1h","Bak20","Dev1320","GFS"]
    #sources = ["GFS","RR1h","FIM"]
    #altitudes = range(0,30001,2000)
    #for source in sources:
        #print "\n\n%s\nSource: %s\n" % ("*"*20,source)
        #data = getData(launchtime,wxstation,source)
        ##print "\n%s\nRaw Data: %s" % ("-"*10,data)
        #parsed_data = parse_wind(data)
        #print "\n%s\nParsed Data:" % ("-"*10)
        #for datapoint in parsed_data:
            #print "%s\t%s\t%s" % datapoint
        #datas.append(parsed_data)
    #for sourceset in datas:
        #altitudedata = {}
        #for alt in altitudes:
            #altitudedata[alt] = 0
        #for datapoint in sourceset:
            #if 99999 in datapoint:
                #continue
            #pointaltitude = floor(datapoint[0]/2000)*2000
            #if not altitudedata[pointaltitude]==0:
                #tempdata = altitudedata[pointaltitude]
                #average = tempdata+datapoint[2]
                #altitudedata[pointaltitude] = average
            #else:
                #altitudedata[pointaltitude] = datapoint[2]
        #altdatas.append(altitudedata)
    #i = 0
    #for dataset in altdatas:
        #print source[i]
        #for datapoint in dataset:
            #for altitude in altitudes:
                #print "%s\t%s" % (altitude,datapoint[altitude])
            










"""

http://www.ready.noaa.gov/ready2-bin/profile2.pl?Lat=40.43&Lon=-109.52&cntry=US&elev=1609&gsize=96&hgt=0&map=WORLD&mdatacfg=GFS&metcyc=18%2020120607&metdata=GFS&metdate=June%2007,%202012%20at%2018%20UTC%20(+%2000%20Hrs)&metdir=/pub/forecast/20120607/&metext=gfsf&metfil=hysplit.t18z.gfsf&nhrs=12&password1=RQVCPV&pdf=No&proc=6209&sid=VEL&skewt=0&sname=VERNAL_(ASOS)&state=UT&textonly=Yes&type=0&userid=7778

http://rucsoundings.noaa.gov/get_soundings.cgi?data_source=GFS;latest=latest;start_year=2012;start_month_name=Jun;start_mday=8;start_hour=0;start_min=0;n_hrs=72;fcst_len=72;airport=VEL;text=Ascii%20text%20%28GSD%20format%29;hydrometeors=false&start=latest

"""