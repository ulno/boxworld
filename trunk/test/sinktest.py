'''
Testing the sink behaviour

Created on 5.3.2011

@author: steffen
'''

import boxworld.Chemical_Sink as cs
import numpy as np
import matplotlib.pyplot as plt

# scaling to convert ppbv to molecules per cube meter (m3)
#
nair = 101325 * 6.022e23 / (8.314 * (25 + 273.15))
fnair = nair * 1e-6 * 1e-9

x = cs.Chemical_Sink(5.0e11,30,15*fnair,2*fnair,1e-4*fnair)

time = np.arange(100)
deltaTime = 10
y = [x.terpene_concentration]

for t in time:
    h = x.terpene_concentration - x.compute(deltaTime)
    x.terpene_concentration = h
    y.append(h)
    
plt.plot(y)
plt.xlabel("time")
plt.ylabel("concentration rate")
plt.show()
