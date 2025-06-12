import numpy as np
b = 3.15
b2 = 3.15/2
b1 = 3.14/2
max_deflection = 20
V = 10
croot = 1.3
ctip = 1
Sref = 2
tau = 0.4
Clalpha = 4.7
Ptarget = 90
P = 0
Cd0 = 0.05
def get_Cldeltaa(Clalpha,tau,Sref,b,croot,ctip,b1,b2):
    dy = 0.001
    integral = 0
    y = b1
    while y < b2:
        y = y + dy
        c = croot - (croot-ctip)/(b/2)*y
        integral = integral + dy*y*c
    Cldeltaa = integral*2*Clalpha*tau/(Sref*b)
    return Cldeltaa
def get_Clp(Clalpha,Cd0,Sref,b,ctip,croot):
    dy = 0.001
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
