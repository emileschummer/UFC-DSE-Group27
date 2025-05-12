import numpy as np

CD0 = 0.05
piAe = 30
S = 1 #m^2
W = 150 #N
CLmax = 2
CL0 = 0.1
CLalpha = 0.1 #degrees
Tmax = 300 #N
A = 0.0008
eta = 0.8
numberengines = 2
Vstall = ((2*W)/(1.225*CLmax*S))**0.5 #m/s
alphastall = (CLmax - CL0)/CLalpha *np.pi/180 #radians
print('Vstall:', Vstall, 'alphastall:', alphastall)

def calculate_power_UFC_MMA_3(incline,V,rho):

    L = np.cos(incline)*W
    CL = 2*L/(rho*S*V**2)
    if CL <= CLmax:
        CD = CD0 + CL**2/piAe
        T = (0.5*rho*CD*S*V**2 + np.sin(incline)*W)/numberengines
    else:
        CL = CLmax
        CD = CD0 + CL**2/piAe
        L = 0.5*rho*CL*S*V**2
        Tvertical = np.cos(incline)*W - L
        Thorizontal = 0.5*rho*CD*S*V**2 + np.sin(incline)*W
        T = (Tvertical**2 + Thorizontal**2)**0.5/numberengines
    P = (T**(3/2)/(eta*(2*rho*A)**0.5))*numberengines
    return P
