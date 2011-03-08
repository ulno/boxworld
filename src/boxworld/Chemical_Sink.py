#
# chemicalsink.py
#
# Definition of a sink caused by chemical reactions with emitted terpenes.
#
# Author: Steffen M. Noe (steffen.noe@emu.ee)
# 
# last revision: 04.03.2011
#

# 
# Aim:
#
# The chemical sink, in our case mostly for terpenes needs reactants that can interact with the
# terpenes. There will be two dynamic factors, ozone and NOx (nitrogen oxides) that are variable
# over the day and season. For now, we assume the hydroxyl radical (OH) as a constant background.
# Ozone and NOx can be used as read in look-up table data as example.
#

import numpy as np

class Chemical_Sink:
	'''
	Definition of a chemical sink for a box.
	
	Reaction rate constants are based on the MCM 3.1 (http://www1.chem.leeds.ac.uk//Atmospheric/MCM/mcmproj.html)
	for alpha-pinene as a "general surrogate monoterpene" 
	'''
	__slots__ = ['terpene_concentration', 'temperature', 'ozone', 'nox', 'oh']
	
	def __init__(self, terpene_concentration, temperature, ozone, nox, oh):
		
		self.terpene_concentration = terpene_concentration
		self.temperature = temperature + 273.15 # convert celsius to Kelvin
		self.ozone       = ozone
		self.nox         = nox
		self.oh          = oh
		
		
	
	def Koh(self, temp):
		'''
		Reaction constant for the terpene - hydroxyl radical reaction
		'''
		return 1.2e-11 * np.exp(444./temp) 
	
	def Ko3(self, temp):
		'''
		Reaction constant for the terpene - ozone reaction
		'''
		return 1.01e-15 * np.exp(-732./temp)
	
	def Knox(self, temp):
		'''
		Reaction canstant for the terpene - nitrate oxygen reaction
		'''
		return 1.19e-12 * np.exp(490./temp)
	
	def compute(self, time):
		'''
		Calculate the decay rate of the sink according to the current time interval and store the new
		value of the terpene concentration locally
		'''
		return self.terpene_concentration * \
			np.exp((- self.Knox(self.temperature)*self.nox 
				    - self.Ko3(self.temperature)*self.ozone 
				    - self.Koh(self.temperature)*self.oh) * time)
		
	