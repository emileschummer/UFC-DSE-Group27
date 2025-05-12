import numpy as np

CD0 = 0.05
piAe = 30
S = 1 #m^2
W = 150 #N
CLmax = 2
CL0 = 0.1
CLalpha = 0.1 #degrees
Tmax = 300 #N
Vstall = ((2*W)/(1.225*CLmax*S))**0.5 #m/s
print(Vstall)
alphastall = (CLmax - CL0)/CLalpha *np.pi/180 #radians
A = 0.0008
eta = 0.8
numberengines = 2
