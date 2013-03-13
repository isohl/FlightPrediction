import collections
import errno
import simplekml
import fap
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Distributor(object):
	keyAll = object()
	def __init__(self):
		self.listeners = collections.defaultdict(set)
	
	def addListener(self, key, func):
		self.listeners[key].add(func)

	def getListeners(self, key):
		for listener in self.listeners[Distributor.keyAll]:
			yield key, listener
		if key in self.listeners:
			for listener in self.listeners[key]:
				yield key, listener

	def removeListener(self, key, func):
		self.listeners[key].remove(func)
	
	def message(self, key, message, sender=None):
		for k, listener in self.getListeners(key):
			try:
				listener(key, message,  sender)
			except TypeError:
				try:
					listener(key, message)
				except TypeError:
					listener(message)
				

class Packet(collections.namedtuple("Packet", 'callsign time latitude longitude altitude')):
	def __new__(self, callsign, time, latitude, longitude, altitude):
		return super(Packet, self).__new__(self, callsign, float(time), float(latitude), float(longitude), float(altitude))

class PacketLogger(object):
	packetFileHeader = "Callsign, Time, Latitude, Longitude, Altitude"
	periodicallyWrite = "Periodically"
	@classmethod
	def stringFromPacket(cls, p):
		return ",".join(str(a) for a in p)
		
	@classmethod
	def packet(cls, s):
		parts = s.strip().split(',')
		if len(parts) == 5:
			return Packet(*parts)
		else:
			raise ValueError, "Invalid Packet, %s" % s
	
	def __init__(self, path, erase=False, write_frequency = -1):
		self.write_frequency = write_frequency
		self.adds_since_write = 0
		self.path = path
		self.distributor = Distributor()
		if erase:
			self.empty_packets()
			self.write()
		else:
			self.read()
		
	def write(self, force=False):
		if force or not self.written:
			with open(self.path, 'w') as file:
				file.write(PacketLogger.packetFileHeader+'\n')
				for packetset in self.packets.itervalues():
					for packet in packetset:
						file.write(PacketLogger.stringFromPacket(packet)+'\n')
			self.written = True
	
	def empty_packets(self):
		self.packets = collections.defaultdict(set)
		self.written = False
	
	def read(self):
		self.empty_packets()
		try:
			with open(self.path, 'r') as file:
				f = iter(file)
				try:
					line = next(f)
				except StopIteration:
					self.write()
					return
				if line.rstrip() != PacketLogger.packetFileHeader: 
					raise ValueError, "File is not in correct format"
				for line in file:
					self.addPacket(PacketLogger.packet(line))
					
		except IOError as err:
			if err[0] == errno.ENOENT:
				self.write()
			else:
				raise
		
	def addPacket(self, packet, write_on_add="Periodically"):
		if isinstance(packet, basestring):
			packet = packetconvert(packet)
		if packet not in self.packets[packet.callsign]:
			self.written = False
			self.packets[packet.callsign].add(packet)
			self.distributor.message(packet.callsign, packet, self)
			self.adds_since_write += 1
			if (self.write_frequency >= 0 and write_on_add == PacketLogger.periodicallyWrite
				and self.adds_since_write >= self.write_frequency) or write_on_add:
				self.adds_since_write = 0
				self.write()		
	
	def sortedPackets(self, callsign,key=lambda x: x.time):
		packets = list(self.packets[callsign])
		packets.sort(key=key)
		return packets
	
	def monitor(self, callsign, function):
		self.distributor.addListener(callsign, function)

	def stopMonitoring(self, callsign, function):
		self.distributor.removeListener(callsign, function)
	
	def __enter__(self):
		return self
	
	def __exit__(self, *args):
		self.write()

class TrackWriter(object):
	def __init__(self, path, color='FF00FF00', width=2):
		self.path = path
		self.linestrings = {}
		self.linestyle = simplekml.LineStyle(color=color, width=width)
	
	def setupMonitoring(self, callsign, packetlogger):
		if not isinstance(callsign, basestring):
			raise TypeError, 'bad callsign'
		packetlogger.monitor(callsign, self.getPacket)
		self.getPacket(callsign, None, packetlogger)
	
	def getPacket(self, callsign, packet, sender):
		kml = simplekml.Kml(name=callsign)
		ls = kml.newlinestring(name=callsign,
			coords=((packet.longitude, packet.latitude, packet.altitude) for packet in sender.sortedPackets(callsign)))
		ls.style.linestyle = self.linestyle
		kml.save(self.path)
		
def packetconvert(s):
	# note, needs to be feet altitude
	p = fap.Packet(s)
	return Packet(p.src_callsign, p.timestamp, p.latitude, p.longitude, p.altitude)
	
class TNCHandler(FileSystemEventHandler):
	def on_any_event(self,event):
		if event.src_path.endswith('tnc.log'):
			with open(event.src_path, 'r') as f:
				try:
					l = f.readlines()[-1]
					print l
					self.logger.addPacket(l)
				except fap.BadPacket as e:
					print e

if __name__ == "__main__":
	with PacketLogger('test.csv') as p:
		tw = TrackWriter('test.kml')		
		tw.setupMonitoring('KD7FDH-2', p)
		observer = Observer()
		tnc = TNCHandler()
		tnc.logger = p
		observer.schedule(tnc, '.')
		observer.start()
		print 'started'
		try:
			while True:
				time.sleep(0.5)
		except KeyboardInterrupt:
			observer.stop()
		observer.join()
