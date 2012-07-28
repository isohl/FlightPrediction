import os

def writeonce(position,aFile):
    keepgoing=True
    while keepgoing==True:
        try:
            keepgoing=False
            os.rename(aFile,aFile+"~" )
        except:
            print "Error"
            try:
                os.remove(aFile+"~")
            except:
                keepgoing=True
    try:
    ##    aFile = 'Test File.kml'
        destination= open( aFile, "w" )
        source= open( aFile+"~", "r" )
        for line in source:
            if line == '\t\t\t</coordinates>\n':
                if len(position)==2:
                    destination.write(str(position)+",0\n" )
                else:
                    destination.write("%s,%s,%s\n" % position)
            destination.write( line )
    ##        print line
    except KeyboardInterrupt:
        source.close()
        os.remove(aFile+'~')
        destination.close()
        return False
    finally:
        source.close()
        os.remove(aFile+"~")
        destination.close()
    return True

def rewrite(coordlist,aFile):
    while 1:
        try:
            os.rename(aFile,aFile+"~")
            break
        except:
            print "Error"
            try:
                os.remove(aFile+"~")
            except:
                pass
    destination = open(aFile,"w")
    source = open(aFile+"~","r")
    write = True
    try:
        for line in source:
            if "</coordinates>" in line:
                if coordlist == None:
                    pass
                else:
                    for position in coordlist:
                        destination.write("%s,%s,%s\n" % position)
                write=True
            if write:
                destination.write(line)
            if "<coordinates>" in line:
                write=False
    except KeyboardInterrupt:
        return False
    finally:
        source.close()
        os.remove(aFile+"~")
        destination.close()
    return True

def writeFresh(filename,data):
	kmlPrefix = ''''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>D710 Track.kml</name>
	<StyleMap id="msn_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#sn_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#sh_ylw-pushpin</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="sn_ylw-pushpin">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ff0000ff</color>
			<width>3</width>
		</LineStyle>
	</Style>
	<Style id="sh_ylw-pushpin">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ff0000ff</color>
			<width>3</width>
		</LineStyle>
	</Style>
	<Placemark>
		<name>D710 Track</name>
		<styleUrl>#msn_ylw-pushpin</styleUrl>
		<LineString>
			<tessellate>1</tessellate>
			<coordinates>
'''		
	kmlSuffix = ''''
</coordinates>
		</LineString>
	</Placemark>
</Document>
</kml>
'''
	destination = open(filename,"w")
    
	write = True
	destination.write(kmlPrefix)
	try:     
		for i in data:
			destination.write("%s,%s,%s\n" % data[i])
			print ('Wrote coordinate line ' + i+1)
	except KeyboardInterrupt:
		return False
	finally:
		destination.write(kmlSuffix)
		destination.close()
	return True

"""
while 1:
    writeonce()
    raw_input("Waiting...")
"""
