import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#initial conditions

W = 200
m = W/9.81
piAe = 30
Clalpha = 4.635
Clhalpha = 4

Clmax = 2.4
Clmaxh = 1.8

Cl0 = 0.9
Clh0 = 0.1
stall_alpha = (Clmax- Cl0)/Clalpha
b = 3
bh = 0.3

S = 1
Sh = 0.0607

rho = 1.2
Cd0 = 0.05
Cmac = -0.5
stall_speed = (Clmax - Cl0)/Clalpha


q = 0

lh = 2

l = 0.1
c = 0.36

Iy = 14

Cmalpha = 0
Tz = 0
Tx = 0
diff_thrust_pitch = 0

elevator_delta = 0

Cldelta = 0.5
Clhdelta = 0.5

def get_Cx(alpha, pitch, V, Tx, W):
    Cl = alpha * Clalpha + Cl0
    Cd = Cd0 + Cl**2 / piAe
    Ct = np.cos(alpha) * Cd - np.sin(alpha) * Cl
    Cx = Tx / (0.5 * rho * S * V**2) - np.sin(pitch) * W / (0.5 * rho * S * V**2) - Ct
    return Cx


def get_Cz(alpha, pitch, V, Vz, q, Clh0, elevator_delta, Sh, Tz, W):
    Cl = alpha * Clalpha + Cl0
    Cd = Cd0 + Cl**2 / piAe
    Clh = np.arcsin((lh * q + Vz) / V) * Clhalpha * (Sh / S) + Clh0 * (Sh / S) + Clhdelta * elevator_delta * (Sh / S)
    Cn = np.cos(alpha) * Cl + np.sin(alpha) * Cd
    Cnh = np.cos(alpha) * Clh
    Cz = np.cos(pitch) * W / (0.5 * rho * S * V**2) - Tz / (0.5 * rho * S * V**2) - Cn - Cnh
    return Cz


def get_Cmy(alpha, V, Vz, q, Clh0, elevator_delta, Sh):
    Cl = alpha * Clalpha + Cl0
    Cd = Cd0 + Cl**2 / piAe
    Clh = ((Vz + lh * q) / V) * Clhalpha * (Sh / S) + Clh0 * (Sh / S) + Clhdelta * elevator_delta * (Sh / S)
    Cn = np.cos(alpha) * Cl + np.sin(alpha) * Cd
    Cnh = np.cos(alpha) * Clh
    Cm = Cn * l / c + Cmac
    Cmh = -Cnh * lh / c
    Cmy = diff_thrust_pitch / (0.5 * rho * S * c * V**2) + Cm + Cmh
    return Cmy

def get_tail_size():
    results = [[],[],[],[]]
    progress = 0
    iteration = 20
    for Clh0 in np.linspace(-0.5,0.5,iteration):
        progress = progress + 1
        for Sh in np.linspace(0,1,iteration):
            V = 34
            Vx = np.cos(stall_speed)*V
            Vz = np.sin(stall_speed)*V
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

                    Fx = 0.5*rho*S*V**2 * get_Cx(alpha,pitch,V,Tx,W)

                    Fz = 0.5*rho*S*V**2 * get_Cz(alpha, pitch, V, Vz, q, Clh0, elevator_delta, Sh, Tz, W)

                    My = 0.5*rho*S*c*V**2 * get_Cmy(alpha, V, Vz, q, Clh0, elevator_delta, Sh)
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

    min_val = min(results[0])
    min_index = results[0].index(min_val)
    corresponding_val = results[1][min_index]
    alpha_result = results[2][min_index]
    pitch_result = results[3][min_index]
    return min_val, corresponding_val,alpha_result*180/np.pi,pitch_result*180/np.pi

print(get_tail_size())
plt.show()



