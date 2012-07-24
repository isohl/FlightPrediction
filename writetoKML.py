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
    pass

"""
while 1:
    writeonce()
    raw_input("Waiting...")
"""
