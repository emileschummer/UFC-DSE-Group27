import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import flat_plate_drag_coefficient, fuselage_drag_coefficient, cube_drag_coefficient
from Input.RaceData import Strava_input_csv as sva
import Input.fixed_input_values as input
import os
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
    Cm = Cn * l / c + Cmac
    Cmh = -Cnh * lh / c
    Cmy =  Cm + Cmh
    return Cmy

def old_get_tail_size(W, piAe, Clalpha, Clhalpha,Cl0,S,Cmac,lh,l,Iy,c,plot,tail_span,Clhmax,Cd0_wing, output_folder):
    output_folder_tail = os.path.join(output_folder, "Tail_Sizing")
    os.makedirs(output_folder, exist_ok=True)
    rho = 1.2
    m = W/9.81
    Sh_results = []
    Clh0_results = []
    alpha_results = []
    pitch_results = []
    progress = 0
    iteration = 20
    V = 30
    altitude = sva.altitude_from_density(rho)
    Cf_blade= flat_plate_drag_coefficient(V, rho, altitude, S, input.L_blade, input.w_blade)
    Cf_stab = flat_plate_drag_coefficient(V, rho, altitude,S,input.L_stab, input.w_stab)
    Cf_poles = flat_plate_drag_coefficient(V, rho, altitude, S, input.L_poles, input.w_poles)
    Cf_fus = flat_plate_drag_coefficient(V, rho, altitude, S, input.L_fus, S/input.L_fus)
    CD_speaker = cube_drag_coefficient(V, rho, altitude, S, input.L_speaker)
    CD_gimbal = cube_drag_coefficient(V, rho, altitude, S, input.L_gimbal)
    CD_motor = cube_drag_coefficient(V, rho, altitude, S, input.L_motor)
    CD_fus = fuselage_drag_coefficient(input.L_n, input.L_c, Cf_fus, input.d_fus, S)
    CD0= Cd0_wing+CD_fus + CD_gimbal + CD_speaker + 4 * CD_motor + 2 * Cf_poles+ 4 * Cf_blade + 3 * Cf_stab #Total drag coefficient
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
                plt.plot(time,pitchangle)
                if not os.path.exists(output_folder_tail):
                    os.makedirs(output_folder_tail)
                plt.savefig(os.path.join(output_folder_tail, f"tail_sizing_plot_{progress}_{int(Sh*1000)}_{int(Clh0*1000)}.png"))
        print('\r{:.2f}%'.format(100*progress/iteration), end='', flush=True)
    if plot:
        plt.show()
    plt.close()
    try:
        # Take minimum Sh that is not 0
        Sh_nonzero = [sh for sh in Sh_results if sh > 0]
        Sh = min(Sh_nonzero)
        min_index = Sh_results.index(Sh)
        Clh0 = Clh0_results[min_index]
        alpha_result = alpha_results[min_index]
        pitch_result = pitch_results[min_index]
        span = tail_span
        cord = Sh/span
        max_tail_force = 0.5*rho*Sh*Clhmax*33**2
    except (ValueError, ZeroDivisionError, Exception) as e:
        # Handle cases where min() fails or Sh_results is empty or division by zero
        print("There was an issue, reverted to default values")
        Sh = 1
        Clh0 = 0.4
        alpha_result = 0
        pitch_result = 0
        span = tail_span if tail_span != 0 else 1
        cord = 0
        max_tail_force = 0.5*rho*Sh*Clhmax*33**2
    return Sh, Clh0, span, cord,lh,max_tail_force#alpha_result*180/np.pi,pitch_result*180/np.pi

def get_tail(show,Clalpha,Clhalpha,Clmax,Clhmax,Cmac,S,c,lh,tail_span,stability_margin):
    Vmax = 120/3.6
    rho = 1.225
    def stability_curve(Sh):
        l_c = (Clhalpha/Clalpha)*(Sh*(lh))/(S*c) - stability_margin
        return l_c
    def control_curve(Sh):
        l_c = - Cmac/Clmax - Clhmax/Clmax*(Sh*(lh))/(S*c)
        return l_c


    surface = np.linspace(0,1,100)
    stab = []
    contr = []

    for Sh in surface:
        stab.append(stability_curve(Sh))
        contr.append(control_curve(Sh))
        
    
    plt.plot(stab,surface)
    plt.plot(contr,surface)
    plt.xlabel('(Xcg - Xac)/c')       # X-axis label
    plt.ylabel('Sh/S')   # Y-axis label
    if show: plt.show()
    for i in range(len(surface)):
        margin = stab[i] - contr[i]
        if margin > 0:
            break
    bh = tail_span
    ch = surface[i]/bh
    max_tail_load = 0.5*surface[i]*rho*Vmax**2*Clhmax

    Sh = surface[i]
    Clh0 = 0
    tail_span_loop = bh
    tail_chord_loop = ch
    lh = input.lh
    max_tail_force = max_tail_load
    return Sh, Clh0, tail_span_loop, tail_chord_loop,lh,max_tail_force

#print(get_tail_size(200,30,4.635,4,0.7,2,0.05,-0.5,1,0,14,0.36,True,0.7366,1.5))
#plt.show()



