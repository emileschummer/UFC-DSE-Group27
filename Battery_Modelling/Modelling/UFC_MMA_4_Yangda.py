import numpy as np

CD0 = 0.0264 #same as osprey
piAe = 20.41 #same as osprey
S = 1.25 #m^2 x2.5 compared to research (cuz reearch is 10kg, we go 25)
W = 250 #N
CLmax = 1.3824 *0.9 #same as osprey


r=0.21 #same as osprey
A = np.pi*(r**2) #m^2
eta = 0.8
prop_efficiency = 0.8
numberengines_vertical = 4
numberengines_horizontal = 1
Avertical = A #individual propellor
Ahorizontal = A #individual propellor

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
        L = 0.5*rho*CL*S*V**2 * 0.5 #parameter for wake of propellers
        Tvertical = (np.cos(incline)*W - L)/numberengines_vertical 
        Thorizontal = (0.5*rho*CD*S*V**2 + np.sin(incline)*W)/numberengines_horizontal
    Pvertical = (abs(Tvertical)**3/(2*rho*Avertical))**0.5*(numberengines_vertical/eta)
    Phorizontal = (abs(Thorizontal)**3/(2*rho*Ahorizontal))**0.5*(numberengines_horizontal/eta)
    P = Pvertical + Phorizontal
    return P
