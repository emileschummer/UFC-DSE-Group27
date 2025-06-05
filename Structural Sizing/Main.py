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
Big_Owie_VTOL = True
Big_Owie_Tail = True
Big_owie_WingBox = True


#Create the material
Material = DogshitTestMaterial()
Yield_shear= Material.Yield_Shear
Yield_Stress = Material.Yield_Stress


#Loads
F_Vtol = 70.6 #25*9.81/4 #Newtons
F_prop = 100 #Newtons
T_Vtol = 2.28 #Newtons/Meter
T_prop = 1 #Newtons /Meter

Tail_loading_horizontal_Distributed = 20 #Newtons per meter
Tail_loading_Vertical_Distributed = 30 #Newtons per meter

WingBox_Torque = 100
WingBox_Lift_Distribution = 10 #Should be an elliptical func, we will figure it out later
WingBox_Max_Lift = 100
WingBox_Lift_at_VTOL = 75


#VTOL poles
R_in_VTOL = 0.05
R_out_VTOL = 0.06
L = 0.5
M_x = T_Vtol
M_y = F_Vtol*L


#TAIL
Tail_Length = 0.3 #Meters
Entire_Tail_Length = 0.8 #meters
Momenent_Acting_Point_Tail = Entire_Tail_Length - (Tail_Length*0.5)

Tail_Horizontal_Force = Tail_loading_horizontal_Distributed*Tail_Length
Tail_Vertical_Force = Tail_loading_Vertical_Distributed*Tail_Length

R_in_Tail = 0.05
R_out_Tail = 0.06

M_x_Tail = Tail_Horizontal_Force*Momenent_Acting_Point_Tail
M_y_Tail = Tail_Vertical_Force*Momenent_Acting_Point_Tail


#WINGBOX
Vtol_Location = 0.5
WingBox_B = 0.8
WingBox_H = 0.4
WingBox_t = 0.01


#Sizing Time
while Big_Owie_VTOL:
    Ix = Circle_Moment_of_Inertia(R_out_VTOL,R_in_VTOL)
    Iy=Ix
    VTOL_stress = Bending(M_x, Ix, R_out_VTOL, M_y, Iy, R_out_VTOL)
    VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL,R_out_VTOL,F_Vtol)


    print("----------------------------------------------------")
    print("The Max Shear VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear)
    print("The Max Stress VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress)
    print("The VTOL Thickness:",R_out_VTOL-R_in_VTOL)

    if VTOL_stress <= Yield_Stress and VTOL_Trans_Shear <=Yield_shear:
        Big_Owie_VTOL = False
    else:
        R_out_VTOL +=0.01



while Big_Owie_Tail:
    Ix = Circle_Moment_of_Inertia(R_out_Tail,R_in_Tail)
    Iy = Ix

    Bending_Stress_Tail = Bending(M_x_Tail,Ix,R_out_Tail,M_y_Tail,Iy,R_out_Tail)
    Trans_Shear_Y_Tail = Shear_Transverse_Circle(R_in_Tail,R_out_Tail,Tail_Vertical_Force)
    Trans_Shear_x_Tail= Shear_Transverse_Circle(R_in_Tail,R_out_Tail,Tail_Horizontal_Force)

    Tail_Total_Shear = np.sqrt(Trans_Shear_x_Tail**2 + Trans_Shear_Y_Tail**2)

    print("----------------------------------------------------")
    print("The Max Shear WingBox:",Tail_Total_Shear, "The Yield Shear:", Yield_shear)
    print("The Max Stress Wingbox:",Bending_Stress_Tail,"The yield stress", Yield_Stress)
    print("Thickness Tail:",R_out_Tail-R_in_Tail)

    if Bending_Stress_Tail <= Yield_Stress and Tail_Total_Shear <=Yield_shear:
        Big_Owie_Tail = False
    else:
        R_out_Tail +=0.01



while Big_owie_WingBox:
    WingBox_Ix = WingBox_Moment_of_inertia(B=WingBox_B,H=WingBox_H,t=WingBox_t)
    WingBox_Iy = WingBox_Moment_of_inertia(B=WingBox_H,H=WingBox_B,t=WingBox_t)
    WingBox_Q_x = First_Area_Q_WingBox(H=WingBox_H,B= WingBox_B, t= WingBox_t)
    WingBox_Q_y = First_Area_Q_WingBox(H=WingBox_B,B= WingBox_H, t= WingBox_t)

    WingBox_Torsion_Shear = Shear_Torsion(T=WingBox_Torque , t=WingBox_t , A=(WingBox_B*WingBox_H))

    WingBox_Transverse_Shear_lift = Shear_Transverse_General(F = WingBox_Max_Lift, Q= WingBox_Q_x, I= WingBox_Ix, t=WingBox_t) #modelling for max shear, where force transfered from VTOl
    WingBox_Transverse_Shear_VTOL = Shear_Transverse_General(F = F_Vtol, Q= WingBox_Q_y, I= WingBox_Iy, t=WingBox_t)

    WingBox_Stress = Bending(Mx=(F_Vtol*Vtol_Location), Ix=WingBox_Ix, X=WingBox_B*0.5, My= (WingBox_Lift_at_VTOL*Vtol_Location), Iy=WingBox_Iy, Y=WingBox_H*0.5)

    WingBox_Total_Shear = np.sqrt(WingBox_Torsion_Shear**2 + WingBox_Transverse_Shear_lift**2 + WingBox_Transverse_Shear_VTOL**2 )

    print("----------------------------------------------------")
    print("The Max Shear WingBox:",WingBox_Total_Shear, "The Yield Shear:", Yield_shear)
    print("The Max Stress Wingbox:",WingBox_Stress,"The yield stress", Yield_Stress)
    print("The Wingbox Thickness:",WingBox_t)


    if WingBox_Total_Shear <= Yield_shear and WingBox_Stress <= Yield_Stress:
        Big_owie_WingBox = False
    else:
        WingBox_t +=0.01



