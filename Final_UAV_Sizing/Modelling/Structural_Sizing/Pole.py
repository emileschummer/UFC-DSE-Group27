import numpy as np
import matplotlib as plt
import pandas as pd
from InertiaCalcs import *
from ForceAndStressCals import *
from Materials import *

VTOL_front_Failure = True
VTOL_back_Failure = False

Material_VTOL = AL()
Yield_shear_VTOL= Material_VTOL.Yield_Shear
Yield_Stress_VTOL = Material_VTOL.Yield_Stress
Density_VTOL = Material_VTOL.Density

#Loads
F_Vtol = 61.3125 #25*9.81/4 #Newtons
F_prop = 100 #Newtons
T_Vtol = 2 #Newtons/Meter
T_prop = 1 #Newtons /Meter


#VTOL poles front
R_in_VTOL_front = 0.17
R_out_VTOL_front = 0.1705
d_prop= 0.7366
R_prop = d_prop/2	
MAC= 0.35
Vtol_Pole_Length_front = 1.1*R_prop+ 0.12*MAC
M_y = F_Vtol*Vtol_Pole_Length_front
M_z = T_Vtol


while VTOL_front_Failure:
    Iy = Circle_Moment_of_Inertia(R_out_VTOL_front,R_in_VTOL_front)
    Iz=Iy
    VTOL_stress = Bending(M_y, Iy, R_out_VTOL_front, M_z, Iz, R_out_VTOL_front)
    VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL_front,R_out_VTOL_front,F_Vtol)


    print("----------------------------------------------------")
    print("The Max Shear VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The VTOL Thickness:",R_out_VTOL_front-R_in_VTOL_front)

    if VTOL_stress <= Yield_Stress_VTOL and VTOL_Trans_Shear <=Yield_shear_VTOL:
        VTOL_front_Failure = False
    else:
        R_out_VTOL_front +=0.001


#VTOL poles back
R_in_VTOL_back = 0.17
R_out_VTOL_back = 0.1705
d_prop= 0.7366
R_prop = d_prop/2	
MAC= 0.35
Vtol_Pole_Length_back = 1.1*R_prop+ 0.24*MAC
M_y = F_Vtol*Vtol_Pole_Length_front
M_z = T_Vtol

while VTOL_back_Failure:
    Iy = Circle_Moment_of_Inertia(R_out_VTOL_back,R_in_VTOL_back)
    Iz=Iy
    VTOL_stress = Bending(M_y, Iy, R_out_VTOL_back, M_z, Iz, R_out_VTOL_back)
    VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL_back,R_out_VTOL_back,F_Vtol)


    print("----------------------------------------------------")
    print("The Max Shear VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The VTOL Thickness:",R_out_VTOL_back-R_in_VTOL_back)

    if VTOL_stress <= Yield_Stress_VTOL and VTOL_Trans_Shear <=Yield_shear_VTOL:
        VTOL_front_Failure = False
    else:
        R_out_VTOL_back +=0.001


Vtol_Pole_Mass_front = Volume(A=Tube_Area(R_out=R_out_VTOL_front,R_in=R_in_VTOL_front), L=Vtol_Pole_Length_front)*Density_VTOL
Vtol_Pole_Mass_back = Volume(A=Tube_Area(R_out=R_out_VTOL_back,R_in=R_in_VTOL_back), L=Vtol_Pole_Length_back)*Density_VTOL

Vtol_Pole_Mass = Vtol_Pole_Mass_front + Vtol_Pole_Mass_back
print("VTOL Pole Mass:", Vtol_Pole_Mass)