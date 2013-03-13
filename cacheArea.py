from __future__ import division
import writetoKML


NW = (40.187158,-109.681162)
SE = (39.821682,-109.280980)
NE = (NW[0],SE[1])
SW = (SE[0],NW[1])

difference = (NW[0]-SE[0],NW[1]-SE[1])

stops = 100

writetoKML.rewrite([],"SavePath.kml")

coords = []
for x in range(stops):
    for y in range(stops):
        if x%2==0:
            newpoint = (SE[1]+((y/stops)*difference[1]),SE[0]+((x/stops)*difference[0]),0)
        else:
            newpoint = (SW[1]-((y/stops)*difference[1]),SE[0]+((x/stops)*difference[0]),0)
        #writetoKML.writeonce(newpoint,"SavePath.kml")
        coords.append(newpoint)
    print "Saved Row %s" % x
print "Writing to file"
writetoKML.rewrite(coords,"SavePath.kml")
print "Done"