#
# box.py
#
# Definition of a box class.
#
# Author: Steffen M. Noe (steffen.noe@emu.ee)
# 
# last revision: 04.03.2011
#

#
# Aim:
# 
# The box should hold one or more sources and should contain sinks. The sinks can be a chemical 
# sink that changes the concentration within the box and there should be a transport of matter 
# into and out of the box to neighbouring boxes. Transport can be passive, by diffusion, or 
# active by wind and turbulent mixing.
#
# The box needs a volume, then all boxes will have a unit of concentration as the sources and
# sinks release a chemical per time and we have a timestep then is multiplicative!
#
import Inbox

from threading import Thread
from .Transport import Transport
from .Geometry import Coord

class Box:
	'''
	Box - a 3D slab of "air with something in".
	A Box has (usually) 6 neighbors (up, down, left, right, front, back) and an Inbox for each neighbor.
	It also has a list of sources and a list of chemical sinks (will be usually one sink).
	TODO: Think about where the light comes from.
	'''
	
	def __init__(self, position, cube_length, light_time_function, 
				temperature_time_function, timedelta, initial_time, 
				end_time, initial_terpene, sources=(), sinks=()):
		
		assert isinstance(position, Coord)
		
		self.cubelength = cube_length
		self.light_time_function = light_time_function
		self.temperature_time_function = temperature_time_function
		self.position = position
		
		self.terpene_concentration = initial_terpene
		# scaling to convert ppbv to molecules per cube centimeter (m3)
		#
		self.nair = 101325 * 6.022e23 / (8.314 * (25 + 273.15))
		self.fnair = self.nair * 1e-6 * 1e-9 * 1e-11 # adapted to get rid of large numbers for molecules!

		# Molecular weight of a monoterpene 
		# 
		self.mtWeight = 136
		
		self.inboxes = {}
		
		for n in self.position.surroundingCoords():
			self.inboxes[n] = Inbox.LocalInbox()

		self.sources_list = list(sources)
		self.sink_list = list(sinks)
		
		self.time = initial_time
		self.timedelta = timedelta
		self.end_time = end_time
		
		self.channels = [] # (inbox, outbox)
		
		self.neighbors = {}
		self.stateConsumer = None
		
		
	def set_sources(self, sources_list):
		self.sources_list = sources_list
	
	def set_sinks(self, sink_list):
		self.sink_list = sink_list
	
	def connect_left(self, neighbor):
		self.connect(neighbor)

	def connect_right(self, neighbor):
		self.connect(neighbor)

	def connect_up(self, neighbor):
		self.connect(neighbor)

	def connect_down(self, neighbor):
		self.connect(neighbor)

	def connect_front(self, neighbor):
		self.connect(neighbor)
		
	def connect_back(self, neighbor):
		self.connect(neighbor)
		
	def connect(self, neighbor):
		self.neighbors[neighbor.position] = neighbor
		
		assert self.inboxes.has_key(neighbor.position), "Box %s does not have neighbor %s" % (self.position, neighbor.position)
		assert neighbor.inboxes.has_key(self.position), "Box %s does not have neighbor %s" % (neighbor.position, self.position)
		
		self.channels.append((self.inboxes[neighbor.position], neighbor.inboxes[self.position]))
		
	def run(self):
		'''
		Spawns a Thread that will run the course of the simulation
		for this Box. Returns a handle to the Thread useful for joining on.
		'''	
		
		t = Thread(target=self.__run)
		t.start()

		return t		
		
	def __run(self):
		
		for (_, outbox) in self.channels:
			outbox.put(Transport(self.terpene_concentration, 0))
		
		while self.time <= self.end_time:
			self.__runStep()
			
	def __runStep(self):
		
		#print "Box %s running time %d, terplevel=%d" % (str(self.position), self.time, self.terpene_concentration)
		
		# Notify consumer of current state
		if self.stateConsumer is not None:
			self.stateConsumer.register(self)
		
		prevStates = []
		
		for (inbox, outbox) in self.channels:
			transport = inbox.take()
			prevStates.append((transport.prev_state, outbox))
			self.terpene_concentration += transport.delta
		
		self.applySourcesSinks()	
		
		self.time += self.timedelta
		
		for (prev_state, outbox) in prevStates:
			delta = self.calculateDelta(prev_state)
			outbox.put(Transport(self.terpene_concentration, delta))
		
		
	def calculateDelta(self, terp_concentration):
		
		if terp_concentration > self.terpene_concentration:
			old_conc = self.terpene_concentration
			self.terpene_concentration -= self.terpene_concentration*0.1
			return old_conc*0.1/6
		
		return 0


	def __runOld(self):
		
		while self.time <= self.end_time:
			
			# Broadcast my state to all my neighbors
			for (inbox, outbox) in self.channels:
				print "Box: " + str(self.position) + " notify"
				outbox.put('state', Transport(self.terpene_concentration))
			
			# Compute my new state
			self.compute()
			
			#increase time
			self.time += self.timedelta
			
			print "Box: " + str(self.position) + " new state is " + str(self.terpene_concentration)

	def applySourcesSinks(self):

		emission = 0.0
		for i in self.sources_list:
			emission += i.guenther(self.light_time_function(self.time),
									self.temperature_time_function(self.time)) * self.fnair * self.timedelta
		
		decay = 0.0	
		for j in self.sink_list:
			decay += j.compute(self.timedelta)
	
		# calculate a budget for current time step and set new concentration
		self.terpene_concentration += emission + decay

	def compute(self):
		'''
		compute one timestep:
		- get all inboxes
		- calculate sources and sink + inbox values correspondant to geometry, temperature, light, and timedelta
		   - Notify neighbors of change 
		'''
		
		emission = 0.0
		for i in self.sources_list:
			emission += i.guenther(self.light_time_function(self.time),
									self.temperature_time_function(self.time)) * self.fnair * self.timedelta
		
		decay = 0.0	
		for j in self.sink_list:
			decay += j.compute(self.timedelta)
	
		# calculate a budget for current time step and set new concentration
		self.terpene_concentration += emission + decay
		
		# here should now come the loss by transport
		# Caution: that's just a "pseudo" as there is lacking the transport and links to other boxes.
		for (inbox, outbox) in self.channels:
			
			transport = inbox.take('state')
			
			if transport.terpene_concentration > self.terpene_concentration:
				outbox.put('change', Transport(self.terpene_concentration*0.1/6)) 
				self.terpene_concentration -= self.terpene_concentration*0.1
				# push overall 10% out each time and uniform to the boxes around
			else:
				# The current implementation requires we always notify our neighbor, even if nothing changes
				outbox.put('change', Transport(0)) 
			print "Taking"
			self.terpene_concentration += inbox.take('change').terpene_concentration
				
		print "Done doing calc"


	

		
		