import numpy as np
import matplotlib.pyplot as plt

def largest_real_positive_root(roots):
    real_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]
    if not real_roots:
        return 0  # or raise an exception or return some sentinel value
    return max(real_roots)

g=9.81 #m/s^2, gravitational acceleration
def calculate_power_UFC_FC(incline,V,V_stall,rho, W, a, gamma_dot,D_rest,D_wing,L_wing,CLmax,alpha_T, N_blades, Chord_blade,CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal,eta_prop_vertical, propeller_wake_efficiency):	
    L_req = np.cos(incline)*W + W/g * V * gamma_dot #vertical force required for flight (stationary or not)
    if V > V_stall:
        """As soon as MArco, fix this!"""
        CL = 2*L_req/(rho*1.25*V**2)
        CD = 0.0264 + CL**2/20.41
        D_wing = 0.5*rho*CD*1.25*V**2
        T_horizontal = (D_wing+D_rest + np.sin(incline)*W) + W/g * a
        """until here"""
        #T_horizontal = (D_wing+D_rest + np.sin(incline)*W) + W/g * a
        """Check with Jorge this power consumption is fine"""
        P_wing = T_horizontal*V/eta_prop_horizontal
        P = P_wing
        P_induced, P_parasite, P_profile = 0, 0, 0
    else:
        """As soon as MArco, fix this!"""
        CL = CLmax
        CD = 0.0264 + CL**2/20.41
        D_wing = 0.5*rho*CD*1.25*V**2
        T_horizontal = ((D_wing+D_rest)*V**2 + np.sin(incline)*W) + W/g * a
        L_wing = 0.5*rho*CL*1.25*V**2 * propeller_wake_efficiency  #parameter for wake of propellers
        """until here"""
        #L_wing *= propeller_wake_efficiency#Lifting force of the wing
        L_prop = L_req - L_wing
        T_horizontal = (D_wing+D_rest+ np.sin(incline)*W) + W/g * a
        P_wing = T_horizontal*V/eta_prop_horizontal #Power required to overcome the horizontal thrust
        """Check with Jorge this power consumption is fine"""
        T_vertical_prop = L_prop/numberengines_vertical/eta_prop_vertical #Thrust per vertical propeller
        
        A_prop = r_prop_vertical**2 * np.pi #Area of the propeller	
        #Solve for vi
        alpha_T= 0 
        A=4*(rho*A_prop)**2
        B=8*(rho*A_prop)**2*(V*np.sin(alpha_T))
        C=4*(rho*A_prop*V)**2
        D=0
        E=-T_vertical_prop**2
        vi_roots = np.roots([A,B,C,D,E])
        vi = largest_real_positive_root(vi_roots)
        #Calculate Total Powers
        P_induced = vi * T_vertical_prop * numberengines_vertical
        P_profile = (N_blades*Chord_blade*rho*CD_blade*omega**3*CLmax**4*(1+3*(V/(omega*CLmax))**2))/8
        P = (P_induced + P_wing + P_profile)
        """Should we calculate Power differently? Add efficiency here?"""
    return P
    