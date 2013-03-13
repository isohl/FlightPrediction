from LocalPredict import *
import datetime
import simplekml

tracks = [("Duchesne",(40.191903,-110.38099,5826)),("Myton",(40.149089,-110.127036,5826)),("Delta",(39.3806386,-112.5077147,4759)),
		  ("Evanston",(41.2747778,-111.0346389,7143)),("Roosevelt",(40.296358,-109.986943,5331)),("Near Delta",(39.6676,-113.1269,5220))]
launchtime = datetime.datetime(year=2012,month=11,day=4,hour=9,minute=0)
ascentrate = 1045
descentrate = 1763
burstaltitude = 98000

kml = simplekml.Kml(name='Predictions')
for name, launchsite in tracks:
	#LocalPredict.main(launchtime=launchtime,launchsite=launchsite,writefile=str(track[0])+"Prediction.kml",messages=True)
	if launchtime==None:
		launchtime = datetime.datetime.now()
	wxstation=getClosestStation(launchsite)
	wxstation=wxstation[0]
	data = getData(launchtime,wxstation,"GFS")
	if data=="" or data==None:
		print "No Data, Loading from File...\n*** Warning, this data may be out of date ***"
		data = getDataFromFile()
	else:
		saveDataToFile(data=data)
	atmosphere = parse_wind(data)
	track = makeTrack(atmosphere,launchsite,ascentrate,descentrate,burstaltitude)
	earthtrack = []
	for point in track:
		earthtrack.append((point[1],point[0],point[2]))
	ls = kml.newlinestring(name=name, coords=earthtrack)
	ls.linestyle.color = 'ff00ff00'
	ls.linestyle.width = 3
	ls.altitudemode = simplekml.AltitudeMode.clamptoground
	kml.save('predictions/predictedpath.kml')
	print "Done with %s" % name
	
nl = simplekml.Kml()
netlink = nl.newnetworklink(name="Network Link")
#netlink.open = 1
netlink.link.href = "predictedpath.kml"

netlink.link.refreshmode = "onInterval"
netlink.link.refreshinterval = 2
nl.save("predictions/NetworkLink.kml")
print "Done"