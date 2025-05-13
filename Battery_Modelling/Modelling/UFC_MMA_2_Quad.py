import numpy as np

CD = 0.105 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/0a756857-3708-4250-9524-bdbcc0020d33/content

W = 250 #N

A = 0.3
eta = 0.8
totalA = (1.041/2)**2*np.pi
numberengines = 4
A = totalA/numberengines
Stop = 0.45
Sfront = 0.35
S = Stop*np.sin(eta) + Sfront*np.cos(eta)
def calculate_power_UFC_MMA_2(incline,V,rho):
    D = 0.5*rho*S*CD*V**2
    Tvertical = np.cos(incline)*W
    Thorizontal = (D + np.sin(incline)*W)
    T = (Tvertical**2 + Thorizontal**2)**0.5/numberengines
    P = (abs(T)**3/(2*rho*A))**0.5*(numberengines/eta)
    return P
