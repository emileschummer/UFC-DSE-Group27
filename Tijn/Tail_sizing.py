import numpy as np
import matplotlib.pyplot as plt
stability_margin = 0.05
Clalpha = 4.635
Clhalpha = 4.158
Clmax = 2.2
Clhmax = 1.5
Cmac = -0.5
S = 1
c = 0.36
lh = 0.5
ARh = 6
show = True
def get_tail(show,Clalpha,Clhalpha,Clmax,Clhmax,Cmac,S,c,lh,ARh):
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
        
    if show:
        plt.plot(stab,surface)
        plt.plot(contr,surface)
        plt.xlabel('(Xcg - Xac)/c')       # X-axis label
        plt.ylabel('Sh/S')   # Y-axis label
        plt.show()
    for i in range(len(surface)):
        margin = stab[i] - contr[i]
        if margin > 0:
            break
    bh = (ARh*surface[i])**0.5
    ch = surface[i]/bh
    max_tail_load = 0.5*surface[i]*rho*Vmax**2*Clhmax
    return margin*c, surface[i], bh, ch, max_tail_load
print(get_tail(True,Clalpha,Clhalpha,Clmax,Clhmax,Cmac,S,c,lh,ARh))
