import numpy as np
import matplotlib as plt
import pandas as pd
from InertiaCalcs import *
from ForceAndStressCals import *
from Materials import *


#------------------------------------------------------
#TODO: ADD TRUSS STRUCTURE ANALYSIS FOR MAIN FRAME
#TODO: FIGURE OUT THE HINGE :(
#TODO: ASK DANIEL ABOUT WINGBOX ANALYSIS
#------------------------------------------------------
#Things to run
Big_Owie_VTOL = False
Big_Owie_Tail = False
Big_owie_WingBox = True


#Create the material
Material = DogshitTestMaterial()
Yield_shear= Material.Yield_Shear
Yield_Stress = Material.Yield_Stress


#Loads
F_Vtol = 25*9.81/4 #Newtons
F_prop = 100 #Newtons
T_Vtol = 10 #Newtons/Meter
T_prop = 1 #Newtons /Meter
Wing_loading = 1 #Newtons per meter
Tail_loading_horizontal_Distributed = 20 #Newtons per meter
Tail_loading_Vertical_Distributed = 30 #Newtons per meter


#I beam
t1 = 2
t2 = 2
t3 = 2
H = 2
B = 2
L = 3

#Wing Box
t = 2
H = 1
B = 1
L = 1


#Solid block
B = 2
H = 2
L = 0.5


#VTOL poles
R_in_VTOL = 0.05
R_out_VTOL = 0.06
L = 0.5
M_x = T_Vtol
M_y = F_Vtol*L


while Big_Owie_VTOL:
    print(R_out_VTOL)
    Ix = Circle_Moment_of_Inertia(R_out_VTOL,R_in_VTOL)
    Iy=Ix
    B_stress = Bending(M_x, Ix, R_out_VTOL, M_y, Iy, R_out_VTOL)
    Trans_Shear = Shear_Transverse_Circle(R_in_VTOL,R_out_VTOL,F_Vtol)


    print("----------------------------------------------------")
    print("the Yield Stress is:",Yield_Stress)
    print("the current stress is:",B_stress)
    print("the Yield Shear is:",Yield_shear)
    print("the current Shear is:",Trans_Shear)
    print("IS SHE THICCC THO:",R_out_VTOL)

    if B_stress <= Yield_Stress and Trans_Shear <=Yield_shear:
        Big_Owie_VTOL = False
    else:
        R_out_VTOL +=0.01



#TAIL
Tail_Length = 0.3 #Meters
Entire_Tail_Length = 0.8 #meters

Tail_Horizontal = Tail_loading_horizontal_Distributed*Tail_Length
Tail_Vertical = Tail_loading_Vertical_Distributed*Tail_Length

R_in_Tail = 0.05
R_out_Tail = 0.06

M_x_Tail = Tail_Horizontal*Entire_Tail_Length
M_y_Tail = Tail_Vertical*Entire_Tail_Length

while Big_Owie_Tail:
    TheSuperSecretFunction()
    Ix = Circle_Moment_of_Inertia(R_out_Tail,R_in_Tail)
    Iy = Ix

    Bending_Stress = Bending(M_x_Tail,Ix,R_out_Tail,M_y_Tail,Iy,R_out_Tail)
    Trans_Shear_Y = Shear_Transverse_Circle(R_in_Tail,R_out_Tail,Tail_Vertical)
    Trans_Shear_x = Shear_Transverse_Circle(R_in_Tail,R_out_Tail,Tail_Horizontal)


    print("----------------------------------------------------")
    print("the Yield Stress is:",Yield_Stress)
    print("the current stress is:",Bending_Stress)
    print("the Yield Shear is:",Yield_shear)
    print("the current Shear is:",Trans_Shear_Y,Trans_Shear_x)
    print("IS SHE THICCC THO:",R_out_Tail)

    if Bending_Stress <= Yield_Stress and Trans_Shear_x <=Yield_shear and Trans_Shear_Y <=Yield_shear:
        Big_Owie_Tail = False
    else:
        R_out_Tail +=0.01


WingBox_Torque = 1000
WingBox_Lift_Distribution = 10 #Should be an elliptical func, we will figure it out later
WingBox_B = 0.8
WingBox_H = 0.4
WingBox_t = 0.01




while Big_owie_WingBox:

    #Y-X plane
    WingBox_Torsion_Shear = Shear_Torsion(T=WingBox_Torque , t=WingBox_t , A=(WingBox_B*WingBox_H))
    
    print("----------------------------------------------------")
    print(Yield_shear,"---",WingBox_Torsion_Shear)


    if WingBox_Torsion_Shear <= Yield_shear:
        Big_owie_WingBox = False
    else:
        WingBox_t +=0.01


