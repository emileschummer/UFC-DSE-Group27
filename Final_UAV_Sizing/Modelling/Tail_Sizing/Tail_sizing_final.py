import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import flat_plate_drag_coefficient, fuselage_drag_coefficient, cube_drag_coefficient
from Input.RaceData import Strava_input_csv as sva
import Input.fixed_input_values as input
#initial conditions


def get_Cx(alpha, pitch, V, W,Clalpha,Cl0,Cd0,piAe,rho,S):
    Cl = alpha * Clalpha + Cl0
    Cd = Cd0 + Cl**2 / piAe
    Ct = np.cos(alpha) * Cd - np.sin(alpha) * Cl
    Cx =  - np.sin(pitch) * W / (0.5 * rho * S * V**2) - Ct
    return Cx


def get_Cz(alpha, pitch, V, Vz, q, Clh0, Sh,  W,Clalpha,Cl0,Cd0,piAe,Clhalpha,S,rho,lh):
    Cl = alpha * Clalpha + Cl0
    Cd = Cd0 + Cl**2 / piAe
    Clh = np.arcsin((lh * q + Vz) / V) * Clhalpha * (Sh / S) + Clh0 * (Sh / S) 
    Cn = np.cos(alpha) * Cl + np.sin(alpha) * Cd
    Cnh = np.cos(alpha) * Clh
    Cz = np.cos(pitch) * W / (0.5 * rho * S * V**2)  - Cn - Cnh
    return Cz


def get_Cmy(alpha, V, Vz, q, Clh0, Sh,Clalpha,Cl0,Cd0,piAe,Clhalpha,lh,l,c,Cmac,S):
    Cl = alpha * Clalpha + Cl0
    Cd = Cd0 + Cl**2 / piAe
    Clh = ((Vz + lh * q) / V) * Clhalpha * (Sh / S) + Clh0 * (Sh / S) 
    Cn = np.cos(alpha) * Cl + np.sin(alpha) * Cd
    Cnh = np.cos(alpha) * Clh
    if l > 0:
        Cm = Cn * l / c + Cmac
    else:
        Cm = -Cn * l / c + Cmac
    Cmh = -Cnh * lh / c
    Cmy =  Cm + Cmh
    return Cmy

def get_tail_size(W, piAe, Clalpha, Clhalpha,Cl0,S,Cmac,lh,l,Iy,c,plot,tail_span,Clhmax,Cd0_wing):
    rho = 1.2
    m = W/9.81
    Sh_results = []
    Clh0_results = []
    alpha_results = []
    pitch_results = []
    progress = 0
    iteration = 20
    V = 30
    Cf_fus = flat_plate_drag_coefficient(V, rho, sva.altitude_from_density(rho), input.L_fus)
    CD_fus = fuselage_drag_coefficient(input.L_n, input.L_c, Cf_fus, input.d, S)
    CD_cube = cube_drag_coefficient(V, rho, sva.altitude_from_density(rho), S)
    Cf_blade = flat_plate_drag_coefficient(V, rho, sva.altitude_from_density(rho), input.L_blade)
    Cf_stab = flat_plate_drag_coefficient(V, rho, sva.altitude_from_density(rho), input.L_stab)
    CD0= CD_fus + CD_cube + Cd0_wing + 4 * Cf_blade + 3 * Cf_stab
    for Clh0 in np.linspace(-0.4,0.4,iteration):
        progress = progress + 1
        for Sh in np.linspace(0,1,iteration):
            V = 30
            Vx = 30#np.cos(stall_alpha)*V
            Vz = 0#np.sin(stall_alpha)*V
            alpha = np.arcsin(Vz/V)
            pitch = 0
            q = 0
            t = 0
            tend = 100
            dt = 0.01
            pitchangle = []
            time = []
            stop = False

            while t < tend and abs(pitch) < np.pi/2:
                t = t + dt
                stop = True
                if not (t > 0.7 * tend and abs(q) >= 0.1):
                    stop = False
                    Fx = 0.5*rho*S*V**2 * get_Cx(alpha, pitch, V, W,Clalpha,Cl0,CD0,piAe,rho,S)
                    Fz = 0.5*rho*S*V**2 * get_Cz(alpha, pitch, V, Vz, q, Clh0, Sh,  W,Clalpha,Cl0,CD0,piAe,Clhalpha,S,rho,lh)
                    My = 0.5*rho*S*c*V**2 * get_Cmy(alpha, V, Vz, q, Clh0, Sh,Clalpha,Cl0,CD0,piAe,Clhalpha,lh,l,c,Cmac,S)
                    Vx = Vx + dt*Fx/m
                    Vz = Vz + dt*Fz/m
                    q = q + dt*My/Iy #pitchrate
                    pitch = pitch + dt*q
                    V = (Vx**2 + Vz**2)**0.5
                    alpha =  np.arcsin(Vz/V)
                    pitchangle.append(pitch*180/np.pi)
                    time.append(t)
            if not stop and t > 0.9*tend:
                Sh_results.append(Sh)
                Clh0_results.append(Clh0)
                alpha_results.append(alpha)
                pitch_results.append(pitch)
                if plot: plt.plot(time,pitchangle)
        print('\r{:.2f}%'.format(100*progress/iteration), end='', flush=True)
    if plot:
        plt.show()
    Sh = min(Sh_results)
    min_index = Sh_results.index(Sh)
    Clh0 = Clh0_results[min_index]
    alpha_result = alpha_results[min_index]
    pitch_result = pitch_results[min_index]
    span = tail_span
    cord = Sh/span
    max_tail_force = 0.5*rho*Sh*Clhmax*33**2
    return Sh, Clh0, span, cord,lh,max_tail_force#alpha_result*180/np.pi,pitch_result*180/np.pi

#print(get_tail_size(200,30,4.635,4,0.7,2,0.05,-0.5,1,0,14,0.36,True,0.7366,1.5))
#plt.show()



