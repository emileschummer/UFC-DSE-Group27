import numpy as np
def get_Cy(beta,Clvbeta,lv,yawrate,V,Sv,S):
    Clv = -beta*Clvbeta*(Sv/S) + (lv*yawrate/V)*Clvbeta*(Sv/S)  #rudder due to sidelip and yaw rotation

    Cy = np.cos(beta)*Clv

    return Cy

def Vertical_tail_sizing(vertical_distance_tail_boom_to_ground, fusolage_length,fusolage_with,c,S,Clvalpha,lv):
    span = 2*vertical_distance_tail_boom_to_ground
    CMalphaf = 1/(36.5*c*S)*fusolage_with**2 * fusolage_length
    ARv = 6
    Sv = span**2 / ARv
    cord = Sv/span
    print(Sv,span,cord)
Vertical_tail_sizing(0.3,1,0.3,0.36,2,4.3,1)
t = 0
tend = 20
dt = 0.01
V = 10
Vy = 1
S = 2
rho = 1.225
yawrate = 0
Clvbeta = 4.3
Sv = 0.12
lv = 1
m = 200/9.81
Iz = 15
sideslip = []
time = []
yawing = []
while t < tend:
    t = t +dt
    beta = np.sin(Vy/V)
    Fy = 0.5*rho*S*V**2 *get_Cy(beta,Clvbeta,lv,yawrate,V,Sv,S)
    Mz = Fy*lv
    Vy = Vy + dt*Fy/m
    yawrate = yawrate - dt*Mz/Iz
    time.append(t)
    sideslip.append(beta*180/np.pi)
    yawing.append(yawrate*180/np.pi)

import matplotlib.pyplot as plt
plt.plot(time,sideslip)
plt.plot(time,yawing)
plt.show()
def Jorge():
    for i in range(0,1000):
        print('Pistachio Man Señor Executive')
Jorge()


