"""
writetoKML.py is a module for a HAM Radio tracking program for the HARBOR High Altitude Balloon Project.
    This module contains functions for writing data to Google Earth KML files
    
Ian Sohl
"""
import os

def writeonce(position,aFile):
    """Write a single coordinate to file (altitude optional)"""
    keepgoing=True
    while keepgoing==True:
        #Keep trying while file processes are tied up.
        try:
            keepgoing=False
            #Rename the file to a temporary one
            os.rename(aFile,aFile+"~" )
        except:
            print "Error"
            try:
                #If the temporary file exists, remove it
                os.remove(aFile+"~")
            except:
                keepgoing=True
    try:
        #Create the output file
        destination= open( aFile, "w" )
        source= open( aFile+"~", "r" )
        for line in source:
            #Write lines from the source into the output, appending the coordinate data when appropriate
            if line == '\t\t\t</coordinates>\n':
                if len(position)==2:
                    #If no altitude is specified, use an altitude of 0
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
        #Even if an error occured, make sure to close the files safely
        source.close()
        os.remove(aFile+"~")
        destination.close()
    return True

def rewrite(coordlist,aFile):
    """Completely erase all data in a file and add a list of coordinates"""
    while 1:
        #More efficient rename loop
        try:
            #Exit loop upon the successful rename
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
            #Keep writing until encountering coordinates tag, then append all coordinates in list
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

"""
Everything below is part of Sheyne's rewrite into an object-oriented mode
Really need to switch over to using this...
"""


class KML(object):
    kmlbase = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>%(name)s</name>
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
			<color>%(color)s</color>
			<width>%(width)s</width>
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
			<color>%(color)s</color>
			<width>%(width)s</width>
		</LineStyle>
	</Style>
	<Placemark>
		<name>%(name)s</name>
		<styleUrl>#msn_ylw-pushpin</styleUrl>
		<LineString>
			<tessellate>1</tessellate>
			<coordinates>
			%(coordList)s
			</coordinates>
		</LineString>
	</Placemark>
</Document>
</kml>
'''

    def __init__(self, name, data=[], color='ff00ff00', width=2):
        self.name = name
        self.color = color
        self.width = width
        self.data = list(data)

    def __str__(self):
        self.coordList = '\n'.join('%s,%s,%s' % i for i in self.data if len(i)==3)	

        return KML.kmlbase % self.__dict__

    def add_data_point(self, lat, lon, alt):
        self.data.append((lat, lon, alt))

    def write(self, filename):
        with open(filename,'w') as destination:
            destination.write(str(self))


if __name__ == "__main__":
    kml = KML('TestKML')
    kml.data = [(45,144,4), (56,100,6)]
    kml.add_data_point(20, 45, 10)
    kml.write('testKML.kml')

