'''
sourcesinktest.py

test for the playing together of the source and sink with conversion of units.
source releases in ppb s-1, the "box", yet not explicit has molecules cm-3 and
the sink uses molecules cm-3 s-1. 
time step is chosen to be 10 s.

Created on 5.3.2011

@author: steffen
'''
import Source as so
import Chemical_Sink as cs
import numpy as np
import matplotlib.pyplot as plt

# scaling to convert ppbv to molecules per cube centimeter (m3)
#
nair = 101325 * 6.022e23 / (8.314 * (25 + 273.15))
fnair = nair * 1e-6 * 1e-9

# Molecular weight of a monoterpene
#
mtWeight = 136

#smt = so.Source(1000,25,3.777)
smt = so.Source(1000,25,4)
csi = cs.Chemical_Sink(5.e11,25,15*fnair,2*fnair,1e-4*fnair)

# generate 100 random ozone and nox data
oz = np.random.rand(100) * 15
no = np.random.rand(100) * 2

# generate some sinus curved light and temperature day course
li = []
vec = np.linspace(0.0,100.0,100)
li = np.sin((vec/100)*np.pi) * 1500
tp = np.sin((vec/100)*np.pi) * 35

# timestep and calculation of terpene budget with source and sink 
dt = 10
terp =[5e11]
for i in np.arange(100):
    csi.ozone = oz[i]
    csi.nox = no[i]
    terp.append(terp[i] + (smt.guenther(li[i],tp[i])*fnair*dt - csi.compute(dt)))
    
plt.plot(terp)
plt.xlabel("time")
plt.ylabel("terpene concentration")
plt.show()
