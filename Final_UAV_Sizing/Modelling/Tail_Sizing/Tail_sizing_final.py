import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

def get_tail_size(W, piAe, Clalpha, Clhalpha,Cl0,S,Cd0,Cmac,lh,l,Iy,c,plot,tail_span,Clhmax):
    rho = 1.2
    m = W/9.81
    results = [[],[],[],[]]
    progress = 0
    iteration = 10
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

                    Fx = 0.5*rho*S*V**2 * get_Cx(alpha, pitch, V, W,Clalpha,Cl0,Cd0,piAe,rho,S)

                    Fz = 0.5*rho*S*V**2 * get_Cz(alpha, pitch, V, Vz, q, Clh0, Sh,  W,Clalpha,Cl0,Cd0,piAe,Clhalpha,S,rho,lh)

                    My = 0.5*rho*S*c*V**2 * get_Cmy(alpha, V, Vz, q, Clh0, Sh,Clalpha,Cl0,Cd0,piAe,Clhalpha,lh,l,c,Cmac,S)
                    Vx = Vx + dt*Fx/m

                    Vz = Vz + dt*Fz/m

                    q = q + dt*My/Iy #pitchrate
                    pitch = pitch + dt*q
                    V = (Vx**2 + Vz**2)**0.5
                    alpha =  np.arcsin(Vz/V)

                    pitchangle.append(pitch*180/np.pi)
                    time.append(t)


            print(100*progress/iteration, '%')
            if not stop and t > 0.9*tend:
                results[0].append(Sh)
                results[1].append(Clh0)
                results[2].append(alpha)
                results[3].append(pitch)
                plt.plot(time,pitchangle)
    if plot:
        plt.show()
    Sh = min(results[0])
    min_index = results[0].index(Sh)
    Clh0 = results[1][min_index]
    alpha_result = results[2][min_index]
    pitch_result = results[3][min_index]
    span = tail_span
    cord = Sh/span
    max_tail_force = 0.5*rho*Sh*Clhmax*33**2
    return Sh, Clh0, span, cord,lh,max_tail_force#alpha_result*180/np.pi,pitch_result*180/np.pi

#print(get_tail_size(200,30,4.635,4,0.7,2,0.05,-0.5,1,0,14,0.36,True,0.7366,1.5))
#plt.show()



