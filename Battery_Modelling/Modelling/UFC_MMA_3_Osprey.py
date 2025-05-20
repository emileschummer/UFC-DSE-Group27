import numpy as np
numberengines_MMA3=2
def calculate_power_UFC_MMA_3(incline, V, rho, inputs, max_iter=100, tol=1e-3):
    A = np.pi*(inputs[6]**2)/numberengines_MMA3 #m^2
    L = np.cos(incline)*inputs[0]
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000#to jump into else statement
    if CL <= inputs[5]:
        CD = inputs[2] + CL**2/inputs[3]
        D = 0.5*rho*CD*inputs[4]*V**2
        Thorizontal = (D + np.sin(incline)*inputs[0])
        P = Thorizontal*V/inputs[1]
    else:
        CL = inputs[5]#np.sqrt(inputs[3]*inputs[2])
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 *inputs[7]
        D = 0.5*rho*CD*inputs[4]*V**2
        Tvertical = (np.cos(incline)*inputs[0] - L)/numberengines_MMA3
        Thorizontal = (D + np.sin(incline)*inputs[0])/numberengines_MMA3
        T = (Tvertical**2 + Thorizontal**2)**0.5
        alpha_T= np.cos(Tvertical/T)
        V_ind_hover= (T/(2*rho*A))**0.5
        
        
        vi = V_ind_hover  # initial guess
        for _ in range(max_iter):
            vi_new = V_ind_hover**2 / np.sqrt((V * np.sin(alpha_T) + vi)**2 + (V * np.cos(alpha_T))**2)
            if abs(vi_new - vi) < tol:
                vi = vi_new
                break
            vi = vi_new
        
        #vi= V_ind_hover/(1+V/V_ind_hover)**0.5
        P_induced = vi * numberengines_MMA3 * T#vertical
        P_parasite = 0#Thorizontal * V * numberengines_MMA3
        P = (P_induced + P_parasite) / inputs[1]
    
    #P = (abs(T)**3/(2*rho*A))**0.5*(numberengines_MMA3/inputs[1])
    return P

