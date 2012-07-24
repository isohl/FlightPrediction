import sys
import fap
import datetime
from math import *
import os
import time
import writetoKML
import LocalPredict
import decodeTNC
from Tkinter import *
from threading import Thread


class Application(Frame):
    def getNewPacket(self):
        time = os.stat(self.filepath).st_mtime
        while time - self.savedtime < 1:
            time = os.stat(self.filepath).st_mtime
        self.savedtime = time
        f = open(self.filepath)
        #print "\nRetrieving data"
        allLines = f.readlines()
        while allLines == []:
            allLines = f.readlines()
        lastline = allLines[len(allLines)-1]
        f.close()
        return lastline
    
    def checkCompatibility(self,packet):
        src = packet.src_callsign.strip("-11")
        src = src.strip("-7")
        if src in self.acceptedSigns:
            return True
        else:
            return False        
    
    def writetrack(self,track,latitude=0,longitude=0,altitude=0,append=True,coordlist=[]):
        track = track.lower()
        if self.tracks[track]["active"]==True:
            filepath = self.tracks[track]["file"]
            if append:                
                position = (longitude, latitude, altitude)                
                writetoKML.writeonce(position,filepath)
            else:
                writetoKML.rewrite(coordlist,filepath)
                
    def wipeballoon(self):
        self.writetrack("balloon",append=False)
        
    def wipeD710(self):
        self.writetrack("d710",append=False)
            
    def runPrediction(self,launchpos=(40.191903,-110.38099,5826),direction="up",launchtime=None,
                          ascentrate=1045,descentrate=1763,burstaltitude=98000,wxstation="VEL",source="GFS",data=None):
            print("Running Flight Prediction")
            track = LocalPredict.main(launchsite=launchpos,launchtime=launchtime,ascentrate=ascentrate,descentrate=descentrate,
                                      burstaltitude=burstaltitude,direction=direction)
            self.writetrack("prediction",coordlist=track,append=False)
            #if launchtime==None:
                ##Time of launch, default: Now.
                #launchtime = datetime.datetime.now()
            #if groundalt==None:
                #groundalt=launchpos[2]
            #if data==None:
                #data=LocalPredict.getData(launchtime,wxstation,source)
            #if data=="" or data==None:
                #print "No Data"
                #return False
            #atmosphere = parse_wind(data)
            #track = makeTrack(atmosphere,launchpos,ascentrate,descentrate,burstaltitude)
            #earthtrack = []
            #for point in track:
                #earthtrack.append((point[1],point[0],point[2]))
            #self.writetrack("prediction",coordlist=earthtrack,append=False)
            print("Done with Prediction")
        
    def userprediction(self):
        pass
    
    def main(self):
        #messageroot = Tk()
        #self.banishRoot()
        #self.root.withdraw()
        if self.predictioncheckvar==1:
            self.runPrediction()
        while 1:
            #mainloop
            packet = self.getNewPacket()
            try:
                p = fap.Packet(packet)
            except fap.DecodeError:
                gpscompatible = decodeTNC.determineCompatability(packet,self.d710Signs)
                if gpscompatible:
                    latlong = decodeTNC.latlong(packet)
                    self.writetrack("d710",latitude=latlong[1],longitude=latlong[0])
                    print "Added D710 Track"
                else:
                    print "No D-Track Added"
                continue
            except AttributeError:
                print "Error in packet"
                continue
            compatible = self.checkCompatibility(p)
            if compatible:
                self.writetrack("balloon",latitude=p.latitude,longitude=p.longitude,altitude=p.altitude)
                print "Added Balloon Track: "+str(p.src_callsign)
            else:
                print "No B-Track Added: "+str(p.src_callsign)
            #sys.stdout.flush()
                  
    
    def submit(self):
        fileget=self.fileaddress.get()
        if fileget.lower() == "default":
            if os.name=="nt":
                self.filepath = os.path.expanduser('~')+"\\tnclogs\\tnc.log"
            elif os.name=="posix":
                self.filepath = os.path.expanduser("~/Documents/tnc.log")
            else:
                print "UNKNOWN OPERATING SYSTEM. GET A LIFE."
                return
        else:
            self.filepath = fileget
        #self.savedtime=os.stat(self.filepath).st_mtime        
        self.savedtime=0
        self.acceptedSigns = self.listeners.get()
        self.acceptedSigns=self.acceptedSigns.split(', ')
        self.d710Signs=["$GPRMC","PKWDPOS"]
        print self.filepath
        print self.acceptedSigns
        self.main()
        #self.mainthread = Thread(target=self.main)

    def createWidgets(self):
        self.instructions = Label(self)
        self.instructions["text"] = "Location of TNC Log:"
        #self.instructions.pack({"side": "top"})
        self.instructions.grid(row=0, sticky=W)
        self.fileaddress = Entry(self, justify=LEFT)
        #self.fileaddress.pack()
        self.fileaddress.grid(row=0, column=1, columnspan=2, sticky=E+W)
        self.fileaddress.insert(0,"default")
        self.fileaddress.bind('<Return>',self.submit)
        self.instructions2 = Label(self)
        self.instructions2["text"] = "Accepted Callsigns:"
        #self.instructions2.pack()
        self.instructions2.grid(row=1, sticky=W)
        self.listeners = Entry(self, justify=LEFT)
        #self.listeners.pack()
        self.listeners.grid(row=1, column=1, columnspan=2, sticky=E+W)
        self.listeners.insert(0,"KE7ROS, WB1SAR, KF7WII")
        self.listeners.bind('<Return>',self.submit)
        self.instructions4 = Label(self,text="Add another chase-team")
        self.instructions4.grid(row=3, columnspan = 3)
        self.instructions3 = Label(self)
        self.callsigntoadd = Entry(self, justify=LEFT)
        self.callsigntoadd.grid(row=4,column=1, columnspan=2)
        self.addcallsign 
        self.instructions3["text"] = "\nFiles to be tracked:"
        #self.instructions3.pack()
        self.instructions3.grid(row=3, columnspan=3)
        self.ballooncheckvar = IntVar()
        self.ballooncheckvar.set(1)
        self.ballooncheck = Checkbutton(self, text="Balloon",variable=self.ballooncheckvar)
        #self.ballooncheck.pack()
        self.ballooncheck.grid(row=4, column=0, sticky=W+E)
        self.d710checkvar = IntVar()
        self.d710checkvar.set(1)
        self.d710check = Checkbutton(self, text="D710",variable=self.d710checkvar)
        #self.d710check.pack()
        self.d710check.grid(row=4, column=1, sticky=W, padx=5)
        self.predictioncheckvar = IntVar()
        self.predictioncheckvar.set(1)
        self.predictioncheck = Checkbutton(self, text="Prediction",variable=self.predictioncheckvar)
        #self.predictioncheck.pack()
        self.predictioncheck.grid(row=4, column=2, sticky=W)
        self.submiter = Button(self, bg="#0055EE", fg="white")
        self.submiter["text"] = "Submit"
        self.submiter["command"] = self.submit
        #self.submiter.pack()
        self.submiter.grid(row=5,columnspan=3, pady=10)
        self.balloonwipe = Button(self, text="Wipe Balloon", command=self.wipeballoon)
        self.balloonwipe.grid(row=6)
        self.d710wipe = Button(self, text="Wipe D710", command=self.wipeD710)
        self.d710wipe.grid(row=6,column=1)
        self.newprediction = Button(self, text="New Prediction", command=self.userprediction)
        self.newprediction.grid(row=6, column=2)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        fap.init()
        self.tracks = {"balloon":{"active":True, "file":"./Balloon Track.kml"},
                               "d710":{"active":True, "file":"./D710 Track.kml"},
                               "prediction":{"active":True, "file":"./Prediction.kml"}}        
        self.createWidgets()


if __name__=="__main__":
    root = Tk()
    ##root.geometry("500x500")
    app = Application(master=root)
    app.master.title("Flight Tracker")
    app.mainloop()    

