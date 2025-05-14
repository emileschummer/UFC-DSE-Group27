import numpy as np

CD =0.105 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/0a756857-3708-4250-9524-bdbcc0020d33/content 
S = 0.16 # http://eprints.gla.ac.uk/116394/1/116394.pdf
W = 250 #N

diameter = 1.041 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/9dc27553-90f0-4209-b744-0adee5c75f27/content 
A = (diameter/2)**2*np.pi
eta = 0.8

input =[CD,S,diameter]
def calculate_power_UFC_MMA_1(incline,V,rho, inputs):
    D = 0.5*rho*S*CD*V**2
    Tvertical = np.cos(incline)*W
    Thorizontal = D + np.sin(incline)*W
    T = (Tvertical**2 + Thorizontal**2)**0.5
    P = (abs(T)**3/(2*rho*A))**0.5/eta
    return P