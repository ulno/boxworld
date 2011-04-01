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
from Transport import Transport

class Box:
	'''
	Box - a 3D slab of "air with something in".
	A Box has (usually) 6 neighbors (up, down, left, right, front, back) and an Inbox for each neighbor.
	It also has a list of sources and a list of chemical sinks (will be usually one sink).
	TODO: Think about where the light comes from.
	'''
	
	def __init__(self, position, cube_length, light_time_function, 
				temperature_time_function, timedelta, initial_time, end_time, initial_terpene):
		
		self.cubelength = cube_length
		self.light_time_function = light_time_function
		self.temperature_time_function = temperature_time_function
		self.position = position
		
		self.terpene_concentration = initial_terpene
		# scaling to convert ppbv to molecules per cube centimeter (m3)
		#
		self.nair = 101325 * 6.022e23 / (8.314 * (25 + 273.15))
		self.fnair = self.nair * 1e-6 * 1e-9

		# Molecular weight of a monoterpene
		#
		self.mtWeight = 136
		
		self.inboxes = {}
		
		for n in self.position.surroundingCoords():
			if n.x >= 0 and n.y >= 0 and n.z >= 0:
				self.inboxes[n] = Inbox.LocalInbox()
		'''			
		self.up_inbox = self.inboxes[0]
		self.down_inbox = self.inboxes[1]
		self.left_inbox = self.inboxes[2]
		self.right_inbox = self.inboxes[3]
		self.front_inbox = self.inboxes[4]
		self.back_inbox = self.inboxes[5]
		'''		
		self.sources_list = ()
		self.sink_list = ()
		
		self.time = initial_time
		self.timedelta = timedelta
		self.end_time = end_time
		
		self.channels = [] # (inbox, outbox)
		
		self.neighbors = {}
		
	def set_sources(self, sources_list):
		self.sources_list = sources_list
	
	def set_sinks(self, sink_list):
		self.sink_list = sink_list
	
	def connect_left(self, neighbor):
		'''
		specify left neighbor
		'''
		self.left_outbox = neighbor.right_inbox
		neighbor.right_outbox = self.left_inbox
		self.channels.append((self.left_inbox, self.left_outbox))
		self.neighbors[neighbor.position] = neighbor

	def connect_right(self, neighbor):
		'''
		specify left neighbor
		'''
		self.right_outbox = neighbor.left_inbox
		neighbor.left_outbox = self.right_inbox
		self.channels.append((self.right_inbox, self.right_outbox))
		self.neighbors[neighbor.position] = neighbor

	def connect_up(self, neighbor):
		self.up_outbox = neighbor.down_inbox
		neighbor.down_outbox = self.up_inbox
		self.channels.append((self.up_inbox, self.up_outbox))
		self.neighbors[neighbor.position] = neighbor

	def connect_down(self, neighbor):
		'''
		specify left neighbor
		'''
		self.down_outbox = neighbor.up_inbox
		neighbor.up_outbox = self.down_inbox
		self.channels.append((self.down_inbox, self.down_outbox))
		self.neighbors[neighbor.position] = neighbor

	def connect_front(self, neighbor):
		'''
		specify left neighbor
		'''
		self.front_outbox = neighbor.back_inbox
		neighbor.back_outbox = self.front_inbox
		self.channels.append((self.front_inbox, self.front_outbox))
		self.neighbors[neighbor.position] = neighbor

	def connect_back(self, neighbor):
		'''
		specify left neighbor
		'''
		self.back_outbox = neighbor.front_inbox
		neighbor.front_outbox = self.back_inbox		
		self.channels.append((self.back_inbox, self.back_outbox))
		self.neighbors[neighbor.position] = neighbor
		
	def connect(self, neighbor):
		self.neighbors[neighbor.position] = neighbor
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
		
		print "Box %s running time %d, terplevel=%d" % (str(self.position), self.time, self.terpene_concentration)
		
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


	

		
		