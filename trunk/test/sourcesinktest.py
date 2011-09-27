'''
sourcesinktest.py

test for the playing together of the source and sink with conversion of units.
source releases in ppb s-1, the "box", yet not explicit has molecules cm-3 and
the sink uses molecules cm-3 s-1. 
time step is chosen to be 1.0 s. 
THIS IS BECAUSE LARGE STEPS CAUSE THE SIMPLE SOLVER TO FAIL - THE SMALLER THE SMOOTHER!

Created on 27.09.2011

@author: steffen
'''
import Source as so
import Sink as cs
import numpy as np
import matplotlib.pyplot as plt

# scaling to convert ppbv to molecules per cube centimeter (m3)
#
nair = 101325 * 6.022e23 / (8.314 * (25 + 273.15))
fnair = nair * 1e-6 * 1e-9 * 1e-11

# Molecular weight of a monoterpene
#
mtWeight = 136

# This set of initial values is giving a possible artificial daycourse as set by the sinus
# curves given for light and temperature!
#
smt = so.Source(1000,25,30)
csi = cs.Sink(5.0,25,15,2,1e-4)

# generate 100 random ozone and nox data, simulate kind a change in atmosperic oxidation state
#
oz = np.random.rand(100) * 15
no = np.random.rand(100) * 2

# generate some sinus curved light and temperature day course
#
li = []
vec = np.linspace(0.0,100.0,100)
li = np.sin((vec/100)*np.pi) * 1500
tp = np.sin((vec/100)*np.pi) * 25

# timestep and calculation of terpene budget with source and sink 
#
dt = 1.0
terp =[1.0]
for i in np.arange(100):
    csi.ozone = oz[i]
    csi.nox = no[i]
    csi.terpene_concentration = terp[i]
    terp.append(terp[i] + (smt.guenther(li[i],tp[i])*fnair*dt + csi.compute(dt)))
    # Ok, here we need to have a sum as the Sink is set to calculate the loss by applying 
    # already a minus sign!

    
plt.plot(terp)
plt.xlabel("time")
plt.ylabel("terpene concentration")
plt.show()
