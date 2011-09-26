#
# source.py 
#
# Definition of a terpene emission source.
#
# Author: Steffen M. Noe (steffen.noe@emu.ee)
# 
# last revision: 03.03.2011
#

#
# Note:
#
# This is a quick and dirty programmed class! Might be redesigned to have a proper
# implementation.
#

import numpy as np

class Source(object):
	'''
	Terpene emission source
	'''
	
	#__slots__ = ['light', 'temperature', 'baseEmission', 'emission']
	
	def __init__(self, light, temperature, baseEmission):
		self.light       = light		# actual light flux in mumol m-2 s-1
		self.temperature = temperature	# actual temperature in degree Celsius
		self.e0          = baseEmission	# species specific basal emission rate in conc per time
		self.alpha		 = 0.0027		# empirical parameter
		self.CL1         = 1.066		# empirical parameter
		self.R			 = 8.314		# universal gas constant in J mol-1 K-1
		self.Ts			 = 303.0    	# standard temperature (30 C) in K
		self.TM			 = 314.0		# in K
		self.CT1		 = 95.0E3		# empirical parameter in J mol-1
		self.CT2		 = 230.0E3		# empirical parameter in J mol-1
		self.emission    = self.guenther(light, temperature)

	
	def guenther(self, light, temperature):
		'''
		The Guenther terpene emission algorithm	
		
	 	The emission is calculated as a so called base emission rate e0 and two scaling
	 	functions CL and CT that modulate that basal rate according to the light and
	 	temperature. 
		'''
		self.emission = self.e0 * self.CL(light) * self.CT(temperature)
		return self.emission
		
	def CL(self, light):
		return self.alpha * self.CL1 * light / np.sqrt(1 + self.alpha**2 * light**2)
		
	def CT(self, temperature):
		T = temperature + 273.15	# Convert temperature to Kelvin
		return np.exp(self.CT1 * (T - self.Ts) / (self.R * self.Ts * T)) / \
			(1 + np.exp(self.CT2 * (T - self.TM) / (self.R * self.Ts * T)))
	
	def getEmission(self):
		'''
		Accessor method to read out the emission from that source.
		'''
		return self.emission
		
		