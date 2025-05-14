import numpy as np
<<<<<<< HEAD

CD0 = 0.0264 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
piAe = 20.41 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle

S = 1.25 #m^2 x2.5 compared to research (cuz reearch is 10kg, we go 25)
W = 250 #N
CLmax = 1.3824 *0.9 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
#clmax is 2 says: https://www.sciencedirect.com/science/article/pii/S2090447922004051


r=0.21 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
A = np.pi*(r**2) #m^2
eta = 0.8 
numberengines = 2
def calculate_power_UFC_MMA_3(incline,V,rho):

    L = np.cos(incline)*W
=======
numberengines_MMA3=2
def calculate_power_UFC_MMA_3(incline, V, rho, inputs):
    A = np.pi*(inputs[6]**2) #m^2
    L = np.cos(incline)*inputs[0]
>>>>>>> 7a912145a690572d711c3eaf53bf950b2780cb7b
    if V >0:
        CL = 2*L/(rho*S*V**2)
    else:
        CL = 10000
    if CL <= CLmax:
        CD = CD0 + CL**2/piAe
        T = (0.5*rho*CD*S*V**2 + np.sin(incline)*W)/numberengines
    else:
        CL = CLmax
        CD = CD0 + CL**2/piAe
        L = 0.5*rho*CL*S*V**2 *0.5
        Tvertical = np.cos(incline)*W - L
        Thorizontal = 0.5*rho*CD*S*V**2 + np.sin(incline)*W
        T = (Tvertical**2 + Thorizontal**2)**0.5/numberengines
    P = (abs(T)**3/(2*rho*A))**0.5*(numberengines/eta) #https://www.spinningwing.com/the-helicopter/momentum-theory/?utm_source=chatgpt.com
    return P

