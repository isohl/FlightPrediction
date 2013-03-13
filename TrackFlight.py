"""
TrackFlight.py is a HAM Radio tracking program for the HARBOR High Altitude Balloon Project.

Ian Sohl

Things to do:
Rewrite the KML interface so that all data runs through one file 
    and an unlimited number of objects can be tracked individually
    
Combine the wipe-data functions into one and add wipe capability to chase teams and prediction

Fix the live-flight predictions

Add functionality for retrieving local atmospheric data


"""
import sys
import fap
import datetime
from math import *
import os
import time
from Tkinter import *
from threading import Thread

#SOHL modules:
import writetoKML
import LocalPredict
import decodeTNC

class Application(Frame):
    """Tkinter Interface and Main program"""
    def getNewPacket(self):
        """Monitor Log File for new Packets"""
        #Set a current time
        time = os.stat(self.filepath).st_mtime
        while time - self.savedtime < 1:
            #Recheck if one second has passed since the last update
            time = os.stat(self.filepath).st_mtime
        #Set the current time as updated
        self.savedtime = time
        #Open the log as indicated in 'filepath'
        f = open(self.filepath)
        #Read all of the data from the log into an array
        #     May be inefficient for large logs, but no troubles so far
        allLines = f.readlines()
        while allLines == []:
            #In case the read fails (unknown cause)
            allLines = f.readlines()
        #Identify the line in the last position of the array
        lastline = allLines[len(allLines)-1]
        f.close()
        return lastline
    
    def checkCompatibility(self,packet):
        """Check packet with FAP for compatibility"""
        #src = packet.src_callsign.strip("-11") #Necessarily strip all -11's from the packet end
        #src = src.strip("-7") #Strip -7's from the packet end
        src = packet.src_callsign #Not compatible with previous 2 statements
        src = src.strip("cmd:") #Remove all cmd dialogs from D710 Communication
        #Check to see if the callsign is in the list of tracked callsigns
        if src.lower() in self.acceptedSigns:
            return True
        #Check if the callsign is a chase-team track
        elif src.lower() in self.tracks:
            return "Chase"
        #Otherwise, indicate that the callsign does not meet any specifications
        else:
            return False        
    
    def renamelog(self,logfile,savetime):
        """Rename a saved path log for archiving"""
        #The file is named by the name with the extension .sohl
        oldfile = logfile+".sohl"
        newfile = logfile+str(savetime)+".sohl"
        count = 0
        while True:
            try:
                #Attempt to rename the file to the new name
                os.rename(oldfile,newfile)
                #If no error is encountered, return function
                return True
            except OSError:
                #If the file is unable to be saved (i.e. If there's already a file with that name)
                count+=1
                #Iterate sucessively through increasing numbers until the file is saved
                newfile = logfile+str(savetime)+"--"+str(count)+".sohl"
                if count>50:
                    #Or the indicator that you have too many logs. Sheesh.
                    return False
        
    
    def writelog(self,coords,logfile):
        """Save a list of coordinates in a path to a logfile"""
        #The file is named by the name with the extension .sohl
        newfile = logfile+".sohl"
        opened = open(newfile,"a")
        for coord in coords:
            #write each coordinate onto a new line in the file
            opened.write(str(coord)+"\n")
        opened.close()
        #Only returns True if entire process is successful
        return True
    
    def readlog(self,logfile):
        """Read coordinate list from a saved logfile"""
        #The file is named by the name with the extension .sohl
        newfile = logfile+".sohl"
        opened = open(newfile,"r")
        #The datafile will be split by the \n's with one coordinate per entry
        data = opened.readlines()
        opened.close()
        return data
    
    def writetrack(self,track,latitude=0,longitude=0,altitude=0,append=True,coordlist=[],log=True):
        """Append a track  or display a coordinate list in Google Earth"""
        #Track is a string key for the self.tracks dictionary (i.e. "balloon")
        track = track.lower()
        #Check to see if the track is currently being plotted (checkboxes on GUI)
        if self.tracks[track]["active"]==True:
            #Determine where the kml files are stored from the dict
            filepath = self.tracks[track]["file"]
            #Default for the function unless the user specifically indicates otherwise
            if append:
                #User must also specify the current long, lat, or altitude, default (0,0,0)
                position = (longitude, latitude, altitude)                
                #Log the new coordinate to file if currently saving logs
                if log==True:
                    logfile = self.tracks[track]["log"]
                    self.writelog([position],logfile)
                #Use writetoKML to append the position into the Google Earth KML
                writetoKML.writeonce(position,filepath)
            #If Append is false, and the user has defined a coordinate list
            else:
                #Log the list to file if currently saving logs
                if log==True:
                    logfile = self.tracks[track]["log"]
                    savetime = datetime.datetime.now().date()
                    #Rename the old log before overwriting
                    if self.renamelog(logfile,savetime):
                        self.writelog(coordlist,logfile)
                #Completely rewrite the coordinate list with the current data
                writetoKML.rewrite(coordlist,filepath)
                
    def wipeballoon(self):
        """Erase the current balloon track in Google Earth"""
        #Simply pass no data to the writetrack function, saving it with a coordinate list of []
        self.writetrack("balloon",append=False)
        savetime = datetime.datetime.now().date()
        #Arbitrary redundancy
        self.renamelog(self.tracks["balloon"]["log"],savetime)
        
    def wipeD710(self):
        """Erase the current D710 track in Google Earth"""
        #This should be integrated into the wipeBalloon function (should)
        self.writetrack("d710",append=False)
        savetime = datetime.datetime.now()
        self.renamelog(self.tracks["d710"]["log"],savetime)        
            
    def runPrediction(self):
        """Run a new flight prediction based on current data and plot in Google Earth"""
        #Note this function is under (semi-permanent) construction...
        #    It really needs to be fixed to handle live-tracking and prediction.
        print "Running Flight Prediction"
        #Read the current flight path from the log file
        logfile = self.tracks["balloon"]["log"]
        loggedposition = self.readlog(logfile)
        ##Experimental function to pull wind data out of current track. Needs work.
        #atmosphere, goingup = LocalPredict.getDataFromFlightPath(loggedposition)
        #atmosphere = sorted(atmosphere)
        #direction="down"
        #if goingup:
            #direction="up"
        #direction = "up"
        #atmosphere = LocalPredict.getData(datetime.datetime.now(),"PUC",timeout=20)
        #atmosphere = LocalPredict.parse_wind(atmosphere)
        ##Set the launchsite based on the first position in the track
        launchsite = eval(loggedposition[0].strip("\n"))
        #Which is out of order.
        launchsite = (launchsite[1],launchsite[0],launchsite[2])
        #Factory made ascent, descent, and burst values.
        ascentrate = 1045
        descentrate = 1763
        burstaltitude = 98000
        ##Track if using an adaptive atmosphere, disabled when such atmosphere is disabled. See above.
        #track = LocalPredict.makeTrack(atmosphere,launchsite,ascentrate,descentrate,burstaltitude,direction=direction)
        #earthdata = []
        lastpoint = 0
        direction = "up"
        #Step through the current data to find the highest point
        for position in loggedposition:
            alt = eval(position.strip("\n"))
            if alt[2] < lastpoint[2] and alt[2] > 10000:
                #If the current point is lower than altitude than the last point (and not on the ground)
                direction = "down"
                #Indicate that the balloon is in decent, and record the highest point
                lastpoint = eval(loggedposition[-1].strip("\n"))
                break
            else:
                lastpoint = alt
        #This will either be the highest altitude as the balloon decends, or the current altitude on ascent
        lastpoint = (lastpoint[1],lastpoint[0],lastpoint[2])
        #Numerically determine the closest weather staton.
        wxstation = LocalPredict.getClosestStation(launchsite=launchsite)
        #Pull the wind data from NOAA. (Note: I need to enable local weather data storage)
        data = LocalPredict.getData(datetime.datetime.now(),wxstation,timeout=1)
        #Parse the data for atmospheric wind levels.
        atmosphere = LocalPredict.parse_wind(data)
        #Create a prediction track based on this wind data
        track = LocalPredict.makeTrack(atmosphere,launchsite,ascentrate,descentrate,burstaltitude,direction)
        for position in track:
            #Step through the track and switch the coordinates for use with Google Earth (frustrating)
            earthdata.append((position[1],position[0],position[2]))
        #Display the new track in Google Earth
        self.writetrack("prediction",append=False,coordlist=earthdata)
        
    def userprediction(self):
        """Holder Function for the """
        pass
    
    def main(self):
        """Main function and loop"""
        ##Uncomment these lines to remove the root window for running without a GUI
        ##    Note, this may be necessary for running on Cygwin or other emulators without Tkinter.
        #messageroot = Tk()
        #self.banishRoot()
        #self.root.withdraw()
        while 1:
            #Main Loop that runs continuously. When mainloop terminates, 
            #     the applicatoin GUI will be freed up for another run
            #For each update cycle, begin by getting a new packet
            packet = self.getNewPacket()
            try:
                #Pass the packet to FAP for parsing (accepts MicE, but not D710)
                p = fap.Packet(packet)
            except fap.DecodeError:
                #A Decode Error will occur whenever FAP is unable to parse the packet
                #In this case, check to see if the packet is a GPRMC or PKWDPOS packet
                gpscompatible = decodeTNC.determineCompatability(packet,self.d710Signs)
                if gpscompatible:
                    #If it is a D710 packet, parse it.
                    latlong = decodeTNC.latlong(packet) #returned as (latitude,longitude)
                    if self.d710checkvar.get()==1:
                        #If we are plotting D710 tracks, Plot it on Google Earth
                        self.writetrack("d710",latitude=latlong[1],longitude=latlong[0],log=True)
                        print "Added D710 Track"
                else:
                    #This will print whenever a corrupted packet or command line is encountered
                    print "No D-Track Added"
                continue
            except AttributeError:
                print "Error in packet"
                continue
            #Check to see if the current packet is being tracked
            compatible = self.checkCompatibility(p)
            if compatible == True:                
                #Packets with True compatibility are Balloon packets
                if self.ballooncheckvar.get()==1:                
                    #Plot the coordinate on Google Earth
                    self.writetrack("balloon",latitude=p.latitude,longitude=p.longitude,altitude=int(p.altitude*3.28084),log=True)
                    print "Added Balloon Track: "+str(p.src_callsign)
                    if self.predictioncheckvar.get()==1:
                        #If predictions are currently enabled, run one now.
                        self.runPrediction()                
            elif compatible == "Chase":
                #Recently added, Chase team tracks for D710's and VX-8R's in Chase vehicles
                #   Note, all incoming coordinates will be plotted on the same line, so only track vehicles in the same convoy
                #   This can also be used in a pinch to track 2 balloons
                self.writetrack(p.src_callsign,latitude=p.latitude,longitude=p.longitude,altitude=int(p.altitude*3.28084),log=True)
                print "Added Chase Team: "+str(p.src_callsign)
            else:
                #This is printed for any callsigns not currently being tracked
                print "No B-Track Added: "+str(p.src_callsign)
            #Dump all print messages to the stdout
            sys.stdout.flush()
    
    def addchasecallsign(self):
        """Function to add a callsign to the chase team list"""
        #Pull callsign from the input field.
        newcallsign = self.callsigntoadd.get()
        if newcallsign in self.tracks:
            print "Already Used"
        elif newcallsign == "":
            print "Please Enter a valid callsign"
        else:
            #Give each callsign an entry in self.tracks, but the same filename
            self.tracks[newcallsign.lower()] = {"active":True, "file":"./Tracks/ChaseTeams.kml", "log":"./Logs/ChaseTeams"}
    
    
    def submit(self):
        """Submit and function start for main loop"""
        #This function is called when the user clicks the Submit button
        #grid_forget will remove the indicated widget from being plotted on the GUI
        self.submiter.grid_forget()
        self.fileaddress.grid_forget()
        self.instructions.grid_forget()
        #Refocus the intructions fields and change the text
        self.instructions.grid(row=0,columnspan=3)
        self.instructions["text"] = "Running..."
        self.instructions["fg"] = "blue"
        self.instructions["font"] = "20"
        self.instructions2.grid_forget()
        self.listeners.grid_forget()
        self.instructions2.grid(row=1,columnspan=3)
        self.instructions2["text"] = self.listeners.get()
        self.instructions2["fg"] = "blue"
        #Get the manual address for the TNCLog
        fileget=self.fileaddress.get()
        if fileget.lower() == "default":
            #Default indicates that it is unchanged
            if os.name=="nt":
                #For Windows systems
                self.filepath = os.path.expanduser('~')+"\\tnclogs\\tnc.log"
            elif os.name=="posix":
                #For Unix systems
                self.filepath = os.path.expanduser("~/Documents/tnc.log")
            else:
                print "UNKNOWN OPERATING SYSTEM. GET A LIFE."
                return
        else:
            self.filepath = fileget
        self.savedtime=0
        #Get the list of tracked callsigns and converts it to lowercase
        self.acceptedSigns = self.listeners.get().lower()
        #Split it into an array based on the comma delimiters
        self.acceptedSigns=self.acceptedSigns.split(', ')
        #Define the D710 'callsigns' no need to give Users control over this
        self.d710Signs=["$GPRMC","$PKWDPOS"]
        #Starts main in a new thread so that the Tkinter GUI doesn't freeze up annoyingly
        self.mainthread = Thread(target=self.main)
        #This should allow for eventual implementation of all interfaces through the GUI instead of stdout
        self.mainthread.start()

    def createWidgets(self):
        """Create all objects on the Tkinter GUI"""
        #Create a label that displays text
        self.instructions = Label(self)
        self.instructions["text"] = "Location of TNC Log:"
        self.instructions.grid(row=0, sticky=W) #Stick instructions in the top row
        #Add an input field for user typed data
        self.fileaddress = Entry(self, justify=LEFT)
        self.fileaddress.grid(row=0, column=1, columnspan=2, sticky=E+W)
        #Insert is required to place text in the field.
        self.fileaddress.insert(0,"default")
        #Bind the field such that hitting the 'enter' button also runs submit
        self.fileaddress.bind('<Return>',self.submit)
        self.instructions2 = Label(self)
        self.instructions2["text"] = "Accepted Callsigns:"
        self.instructions2.grid(row=1, sticky=W)
        self.listeners = Entry(self, justify=LEFT)
        self.listeners.grid(row=1, column=1, columnspan=2, sticky=E+W)
        self.listeners.insert(0,"KF7WIG-11, KF7WII-11")
        self.listeners.bind('<Return>',self.submit)
        self.instructions4 = Label(self,text="Add another chase-team")
        self.instructions4.grid(row=3, columnspan = 2)
        self.instructions3 = Label(self)
        self.callsigntoadd = Entry(self, justify=LEFT)
        self.callsigntoadd.grid(row=4,column=0, columnspan=2)
        #Add a button that calls a function (without arguments)
        self.addcallsign = Button(self, text="Add Callsign", command=self.addchasecallsign)
        self.addcallsign.grid(row=4,column=2)
        self.instructions3["text"] = "\nFiles to be tracked:"
        self.instructions3.grid(row=5, columnspan=3)
        #Create a dynamic object to track the checkbutton values (integer only in this case)
        self.ballooncheckvar = IntVar()
        #Set it to the on state
        self.ballooncheckvar.set(1)
        #Create a checkbutton that reflects and changes the value of the variable
        self.ballooncheck = Checkbutton(self, text="Balloon",variable=self.ballooncheckvar)
        self.ballooncheck.grid(row=6, column=0, sticky=W+E)
        self.d710checkvar = IntVar()
        self.d710checkvar.set(1)
        self.d710check = Checkbutton(self, text="D710",variable=self.d710checkvar)
        self.d710check.grid(row=6, column=1, sticky=W, padx=5)
        self.predictioncheckvar = IntVar()
        self.predictioncheckvar.set(0)
        self.predictioncheck = Checkbutton(self, text="Prediction",variable=self.predictioncheckvar)
        self.predictioncheck.grid(row=6, column=2, sticky=W)
        #Add a submit button to run self.submit
        self.submiter = Button(self, bg="#0055EE", fg="white")
        self.submiter["text"] = "Submit"
        self.submiter["command"] = self.submit
        self.submiter.grid(row=7,columnspan=3, pady=10)
        self.balloonwipe = Button(self, text="Wipe Balloon", command=self.wipeballoon)
        self.balloonwipe.grid(row=8)
        self.d710wipe = Button(self, text="Wipe D710", command=self.wipeD710)
        self.d710wipe.grid(row=8,column=1)
        self.newprediction = Button(self, text="New Prediction", command=self.userprediction)
        self.newprediction.grid(row=8, column=2)

    def __init__(self, master=None):
        """Initialize the application"""
        #Create the Tkinter frame for the GUI
        Frame.__init__(self, master)
        self.pack()
        #Initialize FAP (Finnish APRS Parser)
        fap.init()
        #Create a dictionary to hold relevant data about tracked data
        #Each entry in the field is a seperate file in Google Earth
        self.tracks = {"balloon":{"active":True, "file":"./Tracks/Balloon Track.kml", "log":"./Logs/Balloon"},
                               "d710":{"active":True, "file":"./Tracks/D710 Track.kml", "log":"./Logs/D710"},
                               "prediction":{"active":True, "file":"./Tracks/Prediction.kml", "log":"./Logs/Prediction"}}        
        #Create all of the interfaces on the GUI
        self.createWidgets()


if __name__=="__main__":
    #These functions will only run if the application is run directly (not imported)
    #Create a window for the Tkinter Interface
    root = Tk()
    #Specify the size of the window, if needed
    ##root.geometry("500x500")
    #Create a new application for running the GUI
    app = Application(master=root)
    #Change the text in the application bar
    app.master.title("Flight Tracker")
    #Run the Tkinter App
    app.mainloop()    

