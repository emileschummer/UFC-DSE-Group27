import numpy as np
from Battery_Modelling.Input.Configuration_inputs import largest_real_positive_root

numberengines_MMA3=2
def calculate_power_UFC_MMA_3(incline, V, rho, inputs):
    L = np.cos(incline)*inputs[0]
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000#to jump into else statement
    if CL <= inputs[5]:
        #Wing is solely responsible for lift
        CD = inputs[2] + CL**2/inputs[3]
        D_parasite = 0.5*rho*CD*inputs[4]*V**2 #D_parasite includes both the parasite drag of the fusealge and the drag of the lifting force of the wing
        Thorizontal = (D_parasite + np.sin(incline)*inputs[0])
        P = Thorizontal*V/inputs[1]
    else:
        #Vertical propellers kick in to aid with lift
        CL = inputs[5]#np.sqrt(inputs[3]*inputs[2])
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 *inputs[7]
        D_parasite = 0.5*rho*CD*inputs[4]*V**2 #D_parasite includes both the parasite drag of the fusealge and the drag of the lifting force of the wing
        #Calculate thrust and power per engine
        Tvertical = (np.cos(incline)*inputs[0] - L)/numberengines_MMA3
        Thorizontal = (D_parasite + np.sin(incline)*inputs[0])/numberengines_MMA3
        T = (Tvertical**2 + Thorizontal**2)**0.5
        A_prop = inputs[9]/numberengines_MMA3
        #Solve for vi
        alpha_T= np.cos(Tvertical/T)
        A=4*(rho*A_prop)**2
        B=8*(rho*A_prop)**2*(V*np.sin(alpha_T))
        C=4*(rho*A_prop*V)**2
        D=0
        E=-T**2
        vi_roots = np.roots([A,B,C,D,E])
        vi = largest_real_positive_root(vi_roots)
        #Calculate Total Powers
        P_induced = vi * T * numberengines_MMA3
        P_parasite = D_parasite * V #normal thrust of an aircraft
        P_profile = (inputs[10]*inputs[11]*rho*inputs[12]*inputs[13]**3*inputs[6]**4*(1+3*(V/(inputs[13]*inputs[6]))**2))/8
        P = (P_induced + P_parasite + P_profile) / inputs[1]
        P = (P_induced + P_parasite) / inputs[1]
    return P

