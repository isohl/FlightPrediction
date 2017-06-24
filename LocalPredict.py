"""
LocalPredict.py is a module for a HAM Radio tracking program for the HARBOR High Altitude Balloon Project.
    This module contains functions that create balloon predictions based on weather data.

Ian Sohl

"""
from __future__ import division
from math import *
import time
import datetime
import urllib2
import StationData
import sys
import traceback

# Constant for Earths radius in miles
earth_radius = 3960.0

webinputs = [("Launch Site", (
("Launch Time", ("Hours Until Launch", '')), ("Latitude", ("Latitude", "(Decimal Degrees)")),
("Longitude", ("Longitude", "(Decimal Degrees)")),
("Launch Altitude", ("Launch Altitude", "(feet)")))),
             ("Flight Properties", (("Burst Altitude", ("Burst Altitude", "(feet)")),
                                    ("Ascent Rate", ("Ascent Rate", "(feet/minute)")),
                                    ("Descent Rate", ("Descent Rate", "(feet/minute)"))))]


def change_in_latitude(miles):
    """Given a distance north, return the change in latitude."""
    return degrees(miles / earth_radius)


def change_in_longitude(latitude, miles):
    """Given a latitude and a distance west, return the change in longitude."""
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius * cos(radians(latitude))
    return degrees(miles / r)


def milechangelatitude(change):
    """Given a latitude change, return the change in miles"""
    return radians(change) * earth_radius


def milechangelongitude(latitude, change):
    """Given a latitude and change in longitude, return the change in miles"""
    r = earth_radius * cos(radians(latitude))
    return radians(change) * r


def req(url, mode=False, timeout=20):
    """Query a webserver and download data"""
    try:
        if mode == True:
            # If mode is set to True, download the data through TOR
            proxy_support = urllib2.ProxyHandler({"http": "127.0.0.1:8118"})
            opener = urllib2.build_opener(proxy_support)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        else:
            # Otherwise, download it normally
            opener = urllib2.build_opener()
        return opener.open(url, timeout=timeout).read()
    except urllib2.HTTPError:
        # There is no data at the given address (or no connection)
        print "Non-existant"
        return None
    except urllib2.URLError:
        # URLErrors indicate that the address is wrong/corrupt
        print "URL Error"
        return None


def getData(launchtime=None, wxstation="VEL", source="GFS", timeout=10, hourdifference=0):
    """Get new wind data from NOAA servers"""
    ##Forecast Times and Month names are actually deprecated and not needed at the moment
    # forecasttimes = [0, 1, 3, 6, 9, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 144, 168, 192]
    # monthnames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ##Determine the current time
    if launchtime:
        rightnow = datetime.datetime.now()
        timedifference = launchtime - rightnow
        ##Determine how many hours in the future the launch will be
        hourdifference = int(timedifference.total_seconds() / 3600)
    if hourdifference > 120:
        hourdifference = 120
    # forecast = min([(abs(hourdifference-x), x) for x in forecasttimes])[1]
    ##The forecast is the floored to the nearest multiple of 3
    forecast = int(hourdifference / 3) * 3
    if source == "AUTO" and forecast <= 48:
        source = "RAP_221"
    elif source == "AUTO":
        source = "GFS"
    ##The URL with correct data plugged in
    url = """http://rucsoundings.noaa.gov/get_soundings.cgi?data_source=%s;
    n_hrs=1;
    fcst_len=%d;
    airport=%s;
    text=Ascii%%20text%%20%%28GSD%%20format%%29;
    hydrometeors=false&start=latest""" % (source, forecast, wxstation)
    # print url
    ##Remove line breaks
    url = url.replace("\n    ", "")
    ##Request the data from the server
    try:
        data = req(url, timeout=timeout)
    except:
        data = req(url, timeout=timeout)

    # print data
    return data


def getDataFromFlightPath(flighttrack, ascentrate=1045, burstaltitude=98000):
    """Parse a flight track for wind data"""
    flightup = []
    lastalt = 0
    goingup = True
    for trackpoint in flighttrack:
        # Iterate through coordinates on the track
        # Convert Strings to tuples (Make sure you know the source of the file)
        trackpoint = eval(trackpoint.strip("\n"))
        # Retrieve the long, lat, and alt out of the tuple
        longitude, latitude, altitude = trackpoint
        # Convert the altitude into Meters
        altitude = altitude / 3.28084
        if altitude < lastalt and altitude > 10000:
            # Determine whether the balloon is still going up
            goingup = False
            break
        else:
            # Otherwise, append the coordinates to be parsed into wind data
            flightup.append((altitude, longitude, latitude))
            lastalt = altitude
    lastpoint = None
    data = []
    for point in flightup:
        # Iterate through points in the flight up
        if lastpoint is not None:
            # Figure out how much time it took for the balloon to move through the layer
            timediff = (point[0] - lastpoint[0]) * 3.28084 / ascentrate  # in minutes
            if abs(timediff) > 0.0000000000000001:
                # i.e. A really small number
                # Determine the change in latitude and longitude and convert to miles
                xdiff = milechangelatitude(point[2] - lastpoint[2])
                ydiff = milechangelongitude(point[2], (point[1] - lastpoint[1]))
                # Determine the speed (scalar) in miles per hours (clunky)
                speedmph = hypot(xdiff, ydiff) / (timediff / 60)  # mph
                # Convert to Knots (clunkier)
                speed = speedmph * 0.868976  # Knots
                # rotate the data and mirror it across the y-axis so that it matches NOAA data
                angle = (90 - degrees(atan2(xdiff, ydiff))) + 180
                data.append((altitude, angle, speed))
        lastpoint = point
    if len(data) == 0 or data[-1][0] < burstaltitude:
        # Fill in the rest of the ascent data with NOAA wind data
        launchtime = datetime.datetime.now()
        groundlevel = int(flightup[0][0])
        # Determine closest Wx Station
        wxstation = getClosestStation((flightup[0][2], flightup[0][1]))
        wxstation = wxstation[0]
        # Retrieve data from NOAA
        weatherdata = getData(launchtime, wxstation, timeout=2)
        if weatherdata is None:
            weatherdata = getDataFromFile()
        parsed_data = parse_wind(weatherdata)
        for altitude in parsed_data:
            # Append it to remaining slots to burst altitude
            altitude = (int(altitude[0]) + groundlevel, float(altitude[1]), float(altitude[2]))
            data.append(altitude)
    return data, goingup


def getDataFromFile(filename="./WindData.sohl"):
    """Retrieve wind data from save file"""
    aFile = open(filename, "r")
    data = aFile.read()
    aFile.close()
    return data


def saveDataToFile(filename="./WindData.sohl", data=None):
    """Save wind data to save file"""
    if data == None:
        return False
    aFile = open(filename, "w")
    aFile.write(data)
    aFile.close()
    return True


def getClosestStation(launchsite=None, wxStation=None, filename="./StationData.sohl"):
    """Return the WxStation list, and closest station to the launchsite or the data of a designated station"""
    # Read the WxStations from file
    stations = StationData.data
    stationdifference = []
    closest = None
    if launchsite != None:
        for station in stations:
            # Iterate through stations, and assign each station a value determining it's distance to the launchsite
            xdist = abs(launchsite[0] - stations[station]["position"][0])
            ydist = abs(launchsite[1] - stations[station]["position"][1])
            stationdifference.append((xdist + ydist, station))
        # Choose the closest of the list
        closest = (min(stationdifference)[1], stations[min(stationdifference)[1]])
        return closest
    elif wxStation != None:
        # Return the data for that WxStation
        closest = stations[wxStation]
        return closest
    return stations


def parse_wind(data):
    """Parse NOAA wind raw data for python-format information"""
    byline = data.split("\n")
    parsed_data = []
    for line in byline:
        # Split each line of data by spaces and \t
        bycolumn = line.split()
        # Lines <6 are leader information lines
        if len(bycolumn) > 6 and bycolumn[0] in ('4', '5', '6', '7', '8', '9'):
            # Each column number type is for a specific dataset, but 4-9 contain what we want
            if 99999 in [bycolumn[2], bycolumn[5], bycolumn[6]]:
                continue
            # Altitude, Wind Direction, Wind Speed (knots)
            parsed_data.append((bycolumn[2], bycolumn[5], bycolumn[6]))
        elif "Oops!" in line:
            return None
    return parsed_data


def parse_wind_baltrak(data):
    """Parse NOAA wind data through NSV BALTRAK source"""
    byline = data.split("\n")
    parsed_data = []
    for line in byline:
        bycolumn = line.split()
        # print bycolumn[1],bycolumn[4],bycolumn[5]
        parsed_data.append((bycolumn[1], int(float(bycolumn[4])), float(bycolumn[5]) * 1.94384449))
    return parsed_data


def makeTrack(atmosphere, launchsite, ascentrate, descentrate, burstaltitude, direction="up", criticalpoints=False):
    """Simulate a balloon track with given atmospheric wind data"""
    # Convert atmospheric wind data into feet,degrees,and whatever knots *101.3 is
    atmosphere = [(int(float(x[0]) * 3.2808399), int(x[1]), (float(x[2]) * 101.268591)) for x in atmosphere]
    # Sort the data by altitude
    atmosphere = sorted(atmosphere)
    # Determine which layer of atmosphere the balloon is currently in
    balloonlevel = min([(launchsite[2] - i[0], i) for i in atmosphere if launchsite[2] >= i[0]] or [(0, None)])[1]
    # Set the groundlevel as the altitude of the closest wxStation
    groundlevel = getClosestStation(launchsite=launchsite)[1]["position"][2] * 3.28084
    # Remove layers of altitude beyond ground and burst
    atmosphere = [x for x in atmosphere if (x[0] < burstaltitude and x[0] > groundlevel)]
    if direction == "up" and balloonlevel != None:
        # Add a layer of atmosphere at the balloon at the bottom
        atmosphere.insert(0, (launchsite[2], balloonlevel[1], balloonlevel[2]))
    # Append the launchsite as the first location on the track
    trail = [launchsite]
    trailup = []
    traildown = []
    first = True
    totalxdist = 0
    totalydist = 0
    number = [1, 2]
    if direction == "down":
        # If the balloon is descending, don't run the data for ascent (explained later)
        number = [1]
        atmosphere.reverse()
        atmosphere.pop(0)
        first = False
    for levels in number:
        # For ascent/descent
        for level in range(len(atmosphere)):
            # Iterate through the atmosphere by layer
            altitude = atmosphere[level][0]
            if first == True and altitude < launchsite[2]:
                continue
            # Shift the wind-data into a system approximating typical trigonometric system
            windir = 90 - (atmosphere[level][1] + 180)
            # windir = 180 - atmosphere[level][1]
            windmag = atmosphere[level][2]
            if level + 1 < len(atmosphere):
                # Continue iterating
                nextaltitude = atmosphere[level + 1][0]
            else:
                # Unless reached the end of an altitude track
                if first is True:
                    # If ascending, the end is the burst
                    nextaltitude = burstaltitude
                else:
                    # If descending, the end is the ground
                    nextaltitude = launchsite[2]
            # Determine change in altitude between this layer and the next one
            deltaalt = abs(nextaltitude - altitude)
            # Determine the time it took to travel through this layer based on the velocity
            if first is True:
                deltatime = deltaalt / ascentrate
            else:
                deltatime = deltaalt / descentrate
            # Determine how far horizontally (scalar) the balloon has traveled while moving through the layer
            distancetraveled = deltatime * windmag
            # Split magnitude into components based on wind direction and convert to miles
            xdist = distancetraveled * cos(radians(windir)) / 5280
            ydist = distancetraveled * sin(radians(windir)) / 5280
            # Convert change into Latitude and Longitude
            latitudechange = change_in_latitude(ydist)
            longitudechange = change_in_longitude(trail[-1][0], xdist)
            # Add to existing values
            newpos = (trail[-1][0] + latitudechange, trail[-1][1] + longitudechange, nextaltitude)
            if not first:
                traildown.append(newpos)
            else:
                trailup.append(newpos)
            trail.append(newpos)
            totalxdist += xdist
            totalydist += ydist
        # Reverse the order of the atmosphere for the descent
        atmosphere.reverse()
        # Remove the top pop in order to eliminate redundancy
        atmosphere.pop(0)
        if first:
            traildown.append(trailup[-1])
        first = False
    if criticalpoints:
        return trailup, traildown
    return trail


def findLanding(track, launchsite):
    """Pulls landing coordinates and an extremely rough bearing measurement"""
    # Doesn't work at the moment and is not in use
    landing = track[-1]
    """THESE ARE IN DEGREES (CONVERT)"""
    xdist = landing[1] - launchsite[1]
    ydist = landing[0] - launchsite[0]
    totaldist = hypot(xdist, ydist)
    angle = atan2(ydist, xdist)
    if ydist > 0:
        if xdist > 0:
            angle = 90 - angle
        else:
            angle = 450 - angle
    else:
        angle = 90 + abs(angle)
    return landing, (totaldist, angle)


class PredictionException(Exception): pass


class PredictionError(Exception): pass


def webPredict(data):
    """Incoming data:
    {"Launch Time":("Hours Until Launch: ",""),"Latitude":("Latitude: ","(Decimal Degrees)"),"Longitude":("Longitude: ","(Decimal Degrees)"),
    "Launch Altitude":("Launch Altitude","(feet)"),"Burst Altitude":("Burst Altitude: ","(feet)"),
    "Ascent Rate":("Ascent Rate: ","(feet/minute)"),"Descent Rate":("Descent Rate: ","(feet/minute)")}"""
    keys = ["date","time","lat","lon","launch-alt","burst-alt","asc-rate","des-rate"]
    for key in keys:
        try:
            (data[key])
            # raise PredictionException, "Invalid %s" % str(key)
        except:
            raise PredictionException, "Invalid %s, Data:%s" % (str(key), data)
            # raise PredictionError, str(traceback.format_exc())
    try:
        wxstation = getClosestStation((float(data["lat"]), float(data["lon"])))
        rawTime = datetime.datetime.strptime(data["time"],"%H:%M")
        timeDay = datetime.timedelta(hours = rawTime.hour, minutes = rawTime.minute)
        hours = (datetime.datetime.strptime(data["date"],'%Y-%m-%d') + timeDay) - datetime.datetime.utcnow()
        winddata = getData(wxstation=wxstation[0],
                           hourdifference=int(hours.days * 24 + int(hours.seconds / 3600)))
        atmosphere = parse_wind(winddata)
        track, trackdown = makeTrack(atmosphere,
                                     (float(data["lat"]), float(data["lon"]), int(data["launch-alt"])),
                                     int(data["asc-rate"]), int(data["des-rate"]), int(data["burst-alt"]),
                                     criticalpoints=True)
        # raise PredictionException, trackdown
        return track, trackdown
    except:
        raise PredictionError, str(traceback.format_exc())


def main(launchtime=None, launchsite=(40.191903, -110.38099, 5826), ascentrate=1045, descentrate=1763,
         burstaltitude=98000,
         wxstation=None, source="GFS", messages=False, direction="up", writefile="Tracks\Prediction.kml", timeout=20):
    """Self-running predictor"""
    if launchtime == None:
        # If no launchtime is set, assume an immediate launch
        launchtime = datetime.datetime.now()
    if wxstation == None:
        # If no WxStation is set, find the closest
        wxstation = getClosestStation(launchsite)
        wxstation = wxstation[0]
        if messages: print "WxStation: %s" % wxstation
    if messages: print "Retrieving Data..."
    data = getData(launchtime, wxstation, source, timeout=timeout)
    if messages: print "\t...Done"
    if messages: print "Parsing Data"
    if data == "" or data == None:
        print "No Data, Loading from File...\n*** Warning, this data may be out of date ***"
        data = getDataFromFile()
    else:
        saveDataToFile(data=data)
    atmosphere = parse_wind(data)
    if messages: print "Simulating Balloon Flight"
    track = makeTrack(atmosphere, launchsite, ascentrate, descentrate, burstaltitude, direction=direction)
    if messages:
        print "\t...Done"
    else:
        return track
    landing, bearing = findLanding(track, launchsite)
    # for point in track:
    # print "%s\t%s" % (point[0],point[1])
    # print "%s,%s,%s" % (point[1],point[0],point[2]) #Google Earth
    # print "{%s,%s}," % (point[0],point[1]) #Mathematica
    if messages: print "Balloon landed at Latitude: %s, Longitude: %s" % (landing[0], landing[1])
    if messages: print "\tand %s miles from start at %s degrees East of North" % (bearing[0], bearing[1])
    earthtrack = []
    for point in track:
        # Convert the track to google-earth coordinates
        earthtrack.append((point[1], point[0], point[2]))
    if messages:
        import writetoKML
        writetoKML.rewrite(earthtrack, writefile)
    if messages: print "Written to file"


if __name__ == "__main__":
    # The time of balloon release (minutes and seconds allowed but not used)
    launchtime = datetime.datetime(year=2013, month=5, day=4, hour=9, minute=0)
    # The place of balloon release. (Latitude, Longitude, Altitude) *Decimal Degrees and Feet*
    launchsite = (40.191903, -110.38099, 5826)
    # Ascent rate in feet per minute
    ascentrate = 1045
    # Descent rate in feet per minute
    descentrate = 1763
    # Burst Altitude in feet above sea level
    burstaltitude = 98000
    # burstaltitude = 80000
    # The closest weather station (http://nearspaceventures.com/w3Baltrak/htdocs/stationlist.html)
    wxstation = getClosestStation(launchsite)[0]
    # The datasource you want to use, recommended: GFS
    source = "GFS"
    main(launchtime, launchsite, ascentrate, descentrate, burstaltitude, wxstation, source, messages=True)
    """
    #Data-source analysis tool
    datas = []
    altdatas = []
    #sources = ["NAM","Op40","Bak40","FIM","RR1h","Bak20","Dev1320","GFS"]
    sources = ["GFS","RR1h","FIM"]
    altitudes = range(0,30001,2000)
    for source in sources:
        print "\n\n%s\nSource: %s\n" % ("*"*20,source)
        data = getData(launchtime,wxstation,source)
        #print "\n%s\nRaw Data: %s" % ("-"*10,data)
        parsed_data = parse_wind(data)
        print "\n%s\nParsed Data:" % ("-"*10)
        for datapoint in parsed_data:
            print "%s\t%s\t%s" % datapoint
        datas.append(parsed_data)
    for sourceset in datas:
        altitudedata = {}
        for alt in altitudes:
            altitudedata[alt] = 0
        for datapoint in sourceset:
            if 99999 in datapoint:
                continue
            pointaltitude = floor(datapoint[0]/2000)*2000
            if not altitudedata[pointaltitude]==0:
                tempdata = altitudedata[pointaltitude]
                average = tempdata+datapoint[2]
                altitudedata[pointaltitude] = average
            else:
                altitudedata[pointaltitude] = datapoint[2]
        altdatas.append(altitudedata)
    i = 0
    for dataset in altdatas:
        print source[i]
        for datapoint in dataset:
            for altitude in altitudes:
                print "%s\t%s" % (altitude,datapoint[altitude])
       """

"""

http://www.ready.noaa.gov/ready2-bin/profile2.pl?Lat=40.43&Lon=-109.52&cntry=US&elev=1609&gsize=96&hgt=0&map=WORLD&mdatacfg=GFS&metcyc=18%2020120607&metdata=GFS&metdate=June%2007,%202012%20at%2018%20UTC%20(+%2000%20Hrs)&metdir=/pub/forecast/20120607/&metext=gfsf&metfil=hysplit.t18z.gfsf&nhrs=12&password1=RQVCPV&pdf=No&proc=6209&sid=VEL&skewt=0&sname=VERNAL_(ASOS)&state=UT&textonly=Yes&type=0&userid=7778

http://rucsoundings.noaa.gov/get_soundings.cgi?data_source=GFS;latest=latest;start_year=2012;start_month_name=Jun;start_mday=8;start_hour=0;start_min=0;n_hrs=72;fcst_len=72;airport=VEL;text=Ascii%20text%20%28GSD%20format%29;hydrometeors=false&start=latest

"""