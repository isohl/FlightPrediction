import re
import writetoKML
done=False

def delimit(rawdata):
    if "PKWDPOS" in rawdata:
        splitonce = rawdata.split(',')
        splittwice = rawdata[10].split('*')
        if 'N' in splitonce[4] and 'W' in splitonce[6]:
            returnable = [splitonce[3]+"N",splitonce[5]+"W","A="+splittwice[0]]
            return returnable
    if "GPRMC" in rawdata:
        splitonce = rawdata.split(',')
        if 'N' in splitonce[4] and 'W' in splitonce[6]:
            returnable = [splitonce[3]+"N",splitonce[5]+"W"]
            return returnable
    else:
        splitonce = re.split('/|h|O',rawdata)
        if len(splitonce)>=7:
            if 'A=' in splitonce[6]:
                returnable = [splitonce[2],splitonce[3],splitonce[6]]
                return returnable


def latlong(newdata):
    output = delimit(newdata)
    latitude = str(float(output[0][:2])+(float(output[0][2:7])/60))
    longitude = "-"+str(float(output[1][:3])+(float(output[1][3:8])/60))
    return longitude,latitude

def determineCompatability(APRSstring,listenfor):
    if not done:
        for listento in listenfor:
            if APRSstring.startswith(listento):
                returnable = True, listento
##                print returnable
                return returnable
    else:
        return False

##print latlong()
