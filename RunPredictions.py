import LocalPredict
import datetime

tracks = [("Duchesne",(40.191903,-110.38099,5826)),("Myton",(40.149089,-110.127036,5826)),("Delta",(39.3806386,-112.5077147,4759)),
          ("Evanston",(41.2747778,-111.0346389,7143))]
launchtime = datetime.datetime(year=2012,month=7,day=22,hour=9,minute=0)
ascentrate = 1045
descentrate = 1763
burstaltitude = 98000


for track in tracks:
    launchsite = track[1]
    LocalPredict.main(launchtime=launchtime,launchsite=launchsite,writefile=str(track[0])+"Prediction.kml")
    print "Flight Track completed for: "+track[0]