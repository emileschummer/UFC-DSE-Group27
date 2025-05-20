import numpy as np
from Battery_Modelling.Input.Configuration_inputs import largest_real_positive_root

numberengines_vertical_MMA4 = 4
numberengines_horizontal_MMA4 = 1


def calculate_power_UFC_MMA_4(incline,V,rho, inputs, max_iter=100, tol=1e-3):
    A = np.pi*(inputs[6]**2)/numberengines_vertical_MMA4 #m^2
    L = np.cos(incline)*inputs[0]
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000#to jump into else statement
    if CL <= inputs[5]:
        CD = inputs[2] + CL**2/inputs[3]
        D_parasite = 0.5*rho*CD*inputs[4]*V**2 #D_parasite includes both the parasite drag of the fusealge and the drag of the lifting force of the wing
        T_horizontal = (D_parasite + np.sin(incline)*inputs[0])
        P = T_horizontal*V/inputs[1]
    else:
        #Vertical propellers kick in to aid with lift
        CL = inputs[5]#np.sqrt(inputs[3]*inputs[2]) 
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 * inputs[7]  #parameter for wake of propellers
        D_parasite = 0.5*rho*CD*inputs[4]*V**2#D_parasite includes both the parasite drag of the fusealge and the drag of the lifting force of the wing
        #Calculate thrust and power per engine
        Tvertical = (np.cos(incline)*inputs[0] - L)/numberengines_vertical_MMA4
        Thorizontal = (D_parasite + np.sin(incline)*inputs[0])
        A_prop = inputs[10]/(numberengines_vertical_MMA4)
        #Solve for vi
        alpha_T= 0 
        A=4*(rho*A_prop)**2
        B=8*(rho*A_prop)**2*(V*np.sin(alpha_T))
        C=4*(rho*A_prop*V)**2
        D=0
        E=-Thorizontal**2
        vi_roots = np.roots([A,B,C,D,E])
        vi = largest_real_positive_root(vi_roots)
        #Calculate Total Powers
        P_induced = vi * Tvertical * numberengines_vertical_MMA4
        P_parasite = Thorizontal * V #normal thrust of an aircraft
        P_profile = (inputs[11]*inputs[12]*rho*inputs[13]*inputs[14]**3*inputs[6]**4*(1+3*(V/(inputs[14]*inputs[6]))**2))/8
        P = (P_induced + P_parasite + P_profile) / inputs[1]
    return P
