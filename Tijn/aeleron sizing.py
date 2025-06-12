import numpy as np
b = 3.15
b2 = 3.15/2
b1 = 3.14/2
max_deflection = 15
V = 15
croot = 1.3
ctip = 1
Sref = 2
tau = 0.5
Clalpha = 4.7
Ptarget = 90
P = 0
Cd0 = 0.05
rho = 1.225
max_diff_trust = 2*70
def get_Cldeltaa(Clalpha,tau,Sref,b,croot,ctip,b1,b2):
    dy = 0.0001
    integral = 0
    y = b1
    while y < b2:
        y = y + dy
        c = croot - (croot-ctip)/(b/2)*y
        integral = integral + dy*y*c
    Cldeltaa = integral*2*Clalpha*tau/(Sref*b)
    return Cldeltaa
def get_Clp(Clalpha,Cd0,Sref,b,ctip,croot):
    dy = 0.0001
    integral = 0
    y = 0
    while y < b/2:
        y = y + dy
        c = croot - (croot-ctip)/(b/2)*y
        integral = integral + dy*c*y**2
    Clp = -4*(Clalpha + Cd0)*integral/(Sref*b**2)
    return Clp
while P < Ptarget:
    b1 = b1 - 0.01
    P = -(get_Cldeltaa(Clalpha,tau,Sref,b,croot,ctip,b1,b2)/get_Clp(Clalpha,Cd0,Sref,b,ctip,croot))*max_deflection*(2*V/b)
print(P,b1,b2)

V = 3
Pe = []
Pw = []
Pt = []
velocity = []
while V < 120/3.6:
    V = V + 0.1
    P_engine = -(max_diff_trust/(0.5*rho*V**2 *Sref*b))/get_Clp(Clalpha,Cd0,Sref,b,ctip,croot)*max_deflection*(2*V/b)
    P_wing = -(get_Cldeltaa(Clalpha,tau,Sref,b,croot,ctip,b1,b2)/get_Clp(Clalpha,Cd0,Sref,b,ctip,croot))*max_deflection*(2*V/b)
    P_total = P_wing + P_engine
    Pe.append(P_engine)
    Pw.append(P_wing)
    Pt.append(P_total)
    velocity.append(V)

import matplotlib.pyplot as plt
plt.plot(velocity,Pe,label = 'Roll rate due to differential thrust')
plt.plot(velocity,Pw, label = 'Roll rate due to aeleron')
plt.plot(velocity,Pt, label = 'Total maximum roll rate')
plt.xlabel("Velocity [m/s]")
plt.ylabel("Roll rate degree/s")
plt.legend()
plt.grid()
plt.show()