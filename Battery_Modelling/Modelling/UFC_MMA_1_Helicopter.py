import numpy as np

CD = 0.105 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/0a756857-3708-4250-9524-bdbcc0020d33/content
S = 0.3
W = 250 #N

A = 0.8
eta = 0.8


def calculate_power_UFC_MMA_1(incline,V,rho):
    D = 0.5*rho*S*CD*V**2
    Tvertical = np.cos(incline)*W
    Thorizontal = D + np.sin(incline)*W
    T = (Tvertical**2 + Thorizontal**2)**0.5
    P = (T**3/(2*rho*A))**0.5/eta
    return P
import matplotlib.pyplot as plt
V = np.linspace(0,40,1043)
t = []
for i in V:
    t.append(calculate_power_UFC_MMA_1(0,i,1.225))
plt.plot(V,t)
plt.show()