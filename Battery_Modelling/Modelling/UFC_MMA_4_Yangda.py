import numpy as np

CD0 = 0.05
piAe = 30
S = 1 #m^2
W = 250 #N
CLmax = 2
CL0 = 0.1


A = 0.3
eta = 0.8
prop_efficiency = 0.8
numberengines_vertical = 4
numberengines_horizontal = 1


def calculate_power_UFC_MMA_4(incline,V,rho):

    L = np.cos(incline)*W
    if V >0:
        CL = 2*L/(rho*S*V**2)
    else:
        CL = 10000
    if CL <= CLmax:
        CD = CD0 + CL**2/piAe
        Thorizontal = (0.5*rho*CD*S*V**2 + np.sin(incline)*W)/numberengines_horizontal
        Tvertical = 0
    else:
        CL = CLmax
        CD = CD0 + CL**2/piAe
        L = 0.5*rho*CL*S*V**2
        Tvertical = (np.cos(incline)*W - L)/numberengines_vertical
        Thorizontal = (0.5*rho*CD*S*V**2 + np.sin(incline)*W)/numberengines_horizontal
    Pvertical = (abs(Tvertical)**3/(2*rho*A))**0.5*(numberengines_vertical/eta)
    Phorizontal = (abs(Thorizontal)**3/(2*rho*A))**0.5*(numberengines_horizontal/eta)
    P = Pvertical + Phorizontal
    return P
print(calculate_power_UFC_MMA_4())