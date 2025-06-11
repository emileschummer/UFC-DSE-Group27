import numpy as np
import matplotlib as plt
import pandas as pd
from InertiaCalcs import *
from ForceAndStressCals import *
from Materials import *
from AirFoilDataExtraction import *


#------------------------------------------------------
#TODO ADD A SAFETY FACTOR 1.5
#TODO VIBRATIONS --> FLUTTER !!!!
#TODO ASK ALEX FOR FEEDBACK
#TODO DRAG AND TORQUE FORCES FROM PAYLOAD---> TORQUE 0 APPARAENTLY
#TODO gps location
#TODO INCLUDE TAIL IN ENGINE FORCE
#TODO NEST THE FUSELAGE IF'S
#TODO CHECK VON MISES OF SEC 2
#------------------------------------------------------

#Things to run
# Airfoil_Data = load_airfoil_dat("Structural Sizing\AirfoilData\Airfoil.dat")
# Airfoil_Data_Rotated = Rotate_for_Inertia(coordinates=Airfoil_Data, name= "s1223", angle= np.deg2rad(10))

# print(Airfoil_Moment_of_Inertia(Airfoil_Data,))
# print(Airfoil_Moment_of_Inertia(Airfoil_Data_Rotated))

Big_Owie_VTOL = False
Big_Owie_Tail = False
Big_owie_WingBox = False
Big_Owie_VTOL_front = False
Big_Owie_VTOL_back = False
MAC = 1


#Create the material
Material_Tail = DogshitTestMaterial()
Yield_shear_Tail= Material_Tail.Yield_Shear
Yield_Stress_Tail = Material_Tail.Yield_Stress
Density_Tail = Material_Tail.Density

Material_VTOL = DogshitTestMaterial()
Yield_shear_VTOL= Material_VTOL.Yield_Shear
Yield_Stress_VTOL = Material_VTOL.Yield_Stress
Density_VTOL = Material_VTOL.Density

Material_WingBox = DogshitTestMaterial()
Yield_shear_WingBox= Material_WingBox.Yield_Shear
Yield_Stress_WingBox = Material_WingBox.Yield_Stress
Density_WingBox = Material_WingBox.Density

Material_Leg = DogshitTestMaterial()
Yield_shear_Leg = Material_Leg.Yield_Shear
Yield_Stress_Leg = Material_Leg.Yield_Stress
Density_Leg = Material_Leg.Density

Material_Fuselage = DogshitTestMaterial()
Yield_shear_Fuselage = Material_Fuselage.Yield_Shear
Yield_Stress_Fuselage = Material_Fuselage.Yield_Stress
Density_Fuselage = Material_Fuselage.Density



#Loads
F_Vtol = 70.6 #25*9.81/4 #Newtons
F_prop = 100 #Newtons
T_Vtol = 2.28 #Newtons/Meter
T_prop = 1 #Newtons /Meter

Tail_loading_horizontal_Distributed = 20 #Newtons per meter
Tail_loading_Vertical_Distributed = 30 #Newtons per meter

WingBox_Torque = 100
WingBox_Lift_Distribution = 10 #Should be an elliptical func, we will figure it out later REMEMBER -WL^2/2
WingBox_Max_Lift = 100
WingBox_Lift_at_VTOL = 75

Leg_Force = (25*9.81)/4

Main_Engine_Thrust = 25
Main_Engine_Torque = 5


#VTOL poles front
R_in_VTOL_front = 0.17
R_out_VTOL_front = 0.1705
d_prop= 0.7366
R_prop = d_prop/2	
MAC= 0.35
Vtol_Pole_Length_front = 1.1*R_prop+ 0.12*MAC
M_y = F_Vtol*Vtol_Pole_Length_front
M_z = T_Vtol


#VTOL poles back
R_in_VTOL_back = 0.17
R_out_VTOL_back = 0.1705
d_prop= 0.7366
R_prop = d_prop/2	
MAC= 0.35
Vtol_Pole_Length_back = 1.1*R_prop+ 0.24*MAC
M_y = F_Vtol*Vtol_Pole_Length_front
M_z = T_Vtol





#Loads
F_Vtol = 61.3125 #25*9.81/4 #Newtons
F_prop = 100 #Newtons
T_Vtol = 2 #Newtons/Meter
T_prop = 1 #Newtons /Meter




#TAIL
Tail_Length = 0.11 #Meters
Entire_Tail_Length = 1 #meters
Momenent_Acting_Point_Tail = Entire_Tail_Length - (Tail_Length*0.5)

Tail_Horizontal_Force = Tail_loading_horizontal_Distributed*Tail_Length
Tail_Vertical_Force = Tail_loading_Vertical_Distributed*Tail_Length

R_in_Tail = 0.01
R_out_Tail = 0.015

M_x_Tail = Tail_Horizontal_Force*Momenent_Acting_Point_Tail
M_y_Tail = Tail_Vertical_Force*Momenent_Acting_Point_Tail


#WINGBOX
Vtol_Location = 0.5 #along the wingbox
WingBox_length = 1.5
M_x_WingBox = Vtol_Location*F_Vtol
M_y_WingBox = Vtol_Location*WingBox_Lift_at_VTOL
R_in_WingBox = 0.1
R_out_WingBox = 0.11






while Big_Owie_Tail:
    Ix = Circle_Moment_of_Inertia(R_out_Tail,R_in_Tail)
    Iy = Ix

    Bending_Stress_Tail = Bending(M_x_Tail,Ix,R_out_Tail,M_y_Tail,Iy,R_out_Tail)
    Trans_Shear_Y_Tail = Shear_Transverse_Circle(R_in_Tail,R_out_Tail,Tail_Vertical_Force)
    Trans_Shear_x_Tail= Shear_Transverse_Circle(R_in_Tail,R_out_Tail,Tail_Horizontal_Force)

    Tail_Total_Shear = np.sqrt(Trans_Shear_x_Tail**2 + Trans_Shear_Y_Tail**2)

    print("----------------------------------------------------")
    print("The Max Shear WingBox:",Tail_Total_Shear, "The Yield Shear:", Yield_shear_Tail)
    print("The Max Stress Wingbox:",Bending_Stress_Tail,"The yield stress", Yield_Stress_Tail)
    print("Thickness Tail:",R_out_Tail-R_in_Tail)

    if Bending_Stress_Tail <= Yield_Stress_Tail and Tail_Total_Shear <=Yield_shear_Tail:
        Big_Owie_Tail = False
    else:
        R_out_Tail +=0.001



while Big_owie_WingBox:
    WingBox_t = R_out_WingBox - R_in_WingBox

    WingBox_Ix = Circle_Moment_of_Inertia(R_Out=R_out_WingBox,R_in=R_in_WingBox)
    WingBox_Iy = WingBox_Ix
    WingBox_Q = First_Area_Q_Circle(R_out=R_out_WingBox,R_in=R_in_WingBox,t=WingBox_t)
    WingBox_J = Circle_Polar_Moment_of_Inertia(R_out=R_out_WingBox,R_in=R_in_WingBox)

    WingBox_Transverse_Shear_lift = Shear_Transverse_General(F = WingBox_Max_Lift, Q= WingBox_Q, I= WingBox_Ix, t=WingBox_t) #modelling for max shear, where force transfered from VTOl
    WingBox_Torsion_Shear = Shear_Circle_Torsion(T=WingBox_Torque, r=R_out_WingBox, J= WingBox_J)

    WingBox_Stress = Bending(Mx=M_x_WingBox ,Ix=WingBox_Ix, X= R_out_WingBox,My=M_y_WingBox ,Iy=WingBox_Iy,Y=R_out_WingBox) 
    WingBox_Total_Shear = WingBox_Torsion_Shear+WingBox_Transverse_Shear_lift

    Tresca_Stress_Wingbox = Tresca(Stress1=WingBox_Stress,Stress2=0,Shear=WingBox_Total_Shear)
    Von_Mises_Wingbox_Stress, Von_Mises_Wingbox_Shear = Von_Mises(Stress_X=WingBox_Stress,Stress_Y=0,Stress_Z=0,Shear_XY=WingBox_Total_Shear,Shear_YZ=0,Shear_ZX=0)
    
    WingBox_Deflection = Tip_Deflection(F=WingBox_Lift_Distribution,L=WingBox_length,E=Material_WingBox.E,I=WingBox_Ix)
    WingBox_Twist_Angle = Twist(T = WingBox_Torque,  L= WingBox_length, G=Material_WingBox.G, J=WingBox_J)


    print("----------------------------------------------------")
    print("The Tresca Stress WingBox:",Tresca_Stress_Wingbox, "The Yield Shear:",Yield_Stress_WingBox)
    print("The Von Mises Stress Wingbox:",Von_Mises_Wingbox_Stress,"The yield stress", Yield_Stress_WingBox)
    print("The Von Mises Shear Wingbox:",Von_Mises_Wingbox_Shear,"The yield stress", Yield_shear_WingBox )
    print("The Wingbox Thickness:",WingBox_t)


    if Tresca_Stress_Wingbox < Yield_Stress_WingBox and Von_Mises_Wingbox_Stress < Yield_Stress_WingBox and Von_Mises_Wingbox_Shear < Yield_Stress_WingBox and WingBox_Deflection < 0.05*WingBox_length:
        Big_owie_WingBox = False
    else:
        R_out_WingBox +=0.001



Big_Owie_Leg = False
Leg_Length = 0.5
R_in_Leg= 1/1000
R_out_Leg = 2/1000
Leg_Angle = np.deg2rad(30) #deg
Leg_Force_X = Leg_Force*np.sin(Leg_Angle)
Leg_Force_Y = Leg_Force*np.cos(Leg_Angle)



while Big_Owie_Leg:
    Leg_Ix = Circle_Moment_of_Inertia(R_Out=R_out_Leg,R_in=R_in_Leg)

    Leg_Bending = Bending_Simple(M=(Leg_Length*Leg_Force_X), Y=R_out_Leg, I=Leg_Ix)
    Leg_Transverse_Shear = Shear_Transverse_Circle(R_in=R_in_Leg,R_out=R_out_Leg,F=Leg_Force_X)

    Leg_Buckle = Buckling_Stress(E=Material_Leg.E, L=Leg_Length,I=Leg_Ix,A=Tube_Area(R_out=R_out_Leg,R_in=R_in_Leg),K=2)

    Leg_Von_Mises_Stress, Leg_Von_Mises_Shear = Von_Mises(Stress_X=Leg_Bending,Stress_Y=(Leg_Force_Y/Tube_Area(R_in=R_in_Leg,R_out=R_out_Leg)),Stress_Z=0,Shear_XY=Leg_Transverse_Shear,Shear_YZ=0,Shear_ZX=0)

    
    print("----------------------------------------------------")
    print("The Von Mises Stress Leg:",Leg_Von_Mises_Stress,"The yield stress", Yield_Stress_Leg)
    print("The Von Mises Shear Leg:",Leg_Von_Mises_Shear,"The yield stress", Yield_shear_Leg)
    print("The Wingbox Leg:",R_out_Leg-R_in_Leg)

    if Leg_Von_Mises_Stress < Yield_Stress_Leg and Leg_Von_Mises_Shear < Yield_shear_Leg and Leg_Buckle < Yield_Stress_Leg:
        Big_Owie_Leg = False
    else:
        R_out_Leg +=(1/1000)



while Big_Owie_VTOL_front:
    Iy = Circle_Moment_of_Inertia(R_out_VTOL_front,R_in_VTOL_front)
    Iz=Iy
    VTOL_stress = Bending(M_y, Iy, R_out_VTOL_front, M_z, Iz, R_out_VTOL_front)
    VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL_front,R_out_VTOL_front,F_Vtol)


    print("----------------------------------------------------")
    print("The Max Shear FRONT VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress FRONT VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The FRONT VTOL Thickness:",R_out_VTOL_front-R_in_VTOL_front)

    if VTOL_stress <= Yield_Stress_VTOL and VTOL_Trans_Shear <=Yield_shear_VTOL:
        Big_Owie_VTOL_front = False
    else:
        R_out_VTOL_front +=0.001



while Big_Owie_VTOL_back:
    Iy = Circle_Moment_of_Inertia(R_out_VTOL_back,R_in_VTOL_back)
    Iz=Iy
    VTOL_stress = Bending(M_y, Iy, R_out_VTOL_back, M_z, Iz, R_out_VTOL_back)
    VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL_back,R_out_VTOL_back,F_Vtol)


    print("----------------------------------------------------")
    print("The Max Shear BACK VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress BACK VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The BACK VTOL Thickness:",R_out_VTOL_back-R_in_VTOL_back)

    if VTOL_stress <= Yield_Stress_VTOL and VTOL_Trans_Shear <=Yield_shear_VTOL:
        Big_Owie_VTOL_back = False
    else:
        R_out_VTOL_back +=0.001



Big_Owie_Fuselage_Flying = True

R_out_fuselage = 0.3+1/1000 
R_in_fuselage = 0.3

Fuselage_length_sec1 = 0.2
Fuselage_length_sec2 = 0.4
Fuselage_length_sec3 = 0.3

Payload_Location = 0.6-Fuselage_length_sec1 #edit the o.6 to the location, starting from the back of the fuselage

#fUSELAGE lOADS
Fuselage_Sec1_Load = 10 #N*m distributed load
Fuselage_sec2_load = 15 #Battery
Payload_Force = 9.81*0.7 #Newtons, includes Gimbal and Camera
Payload_Drag = 10


while Big_Owie_Fuselage_Flying:
    #SECTION 1:
    Fuselage_t = R_out_fuselage-R_in_fuselage

    Fuselage_J_sec1 = Circle_Polar_Moment_of_Inertia(R_out=R_out_fuselage,R_in=R_in_fuselage)
    Fuselage_I_sec1 = Circle_Moment_of_Inertia(R_Out=R_out_fuselage , R_in=R_in_fuselage)

    Fuselage_Torsion_Sec1 = Shear_Circle_Torsion(J=Fuselage_J_sec1, T= Main_Engine_Torque, r=R_out_fuselage)
    Fuselage_Buckle_sec1 = Buckling_Stress(E=Material_Fuselage.E, L= Fuselage_length_sec1, I=Fuselage_I_sec1, A=Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage), K=2)
    Fuselage_Transverse_Shear_sec1 = Shear_Transverse_Circle(R_in=R_in_fuselage,R_out=R_out_fuselage,F=(Fuselage_Sec1_Load*Fuselage_length_sec1) ) #shear and therefore thickness would vary over the length of the beam, but modelling for worst case at joint where shear is max
    Fuselage_Bending_Stress_sec1 = Bending_Simple( M=(-0.5*Fuselage_Sec1_Load*(Fuselage_length_sec1**2)), Y=R_out_fuselage, I=Fuselage_I_sec1 )

    Fuselage_VonMises_Sec1_Stress, Fuselage_VonMises_Sec1_Shear = Von_Mises(Stress_X=(Main_Engine_Thrust/Tube_Area(R_in=R_in_fuselage,R_out=R_out_fuselage)),Stress_Y=0,Stress_Z=Fuselage_Bending_Stress_sec1,Shear_XY=(Fuselage_Transverse_Shear_sec1+Fuselage_Torsion_Sec1),Shear_YZ=0, Shear_ZX=0)

    if Fuselage_VonMises_Sec1_Stress < Yield_Stress_Fuselage and Fuselage_VonMises_Sec1_Stress < Fuselage_Buckle_sec1 and Fuselage_VonMises_Sec1_Shear < Yield_shear_Fuselage:
        print("Passes Section 1")
        Big_Owie_Fuselage_Flying = False 
    else:
        R_out_fuselage +=1/1000
        Big_Owie_Fuselage_Flying = True 
        

    #SECTION 2:
    Fuselage_t = R_out_fuselage-R_in_fuselage
    Fuselage_Sec1_Load_Total = Fuselage_Sec1_Load*Fuselage_length_sec1
    Fuselage_I_sec2 = Semi_Circle_Moment_of_Inertia(R_out=(R_out_fuselage-0.5*Fuselage_t), t=Fuselage_t)

    Fuselage_Torsion_Sec2 = Torsion_Open(T=Main_Engine_Torque, l= Fuselage_length_sec2, t=Fuselage_t)
    Fuselage_Buckle_sec2 = Buckling_Stress(E=Material_Fuselage.E, L=Fuselage_length_sec2, I=Fuselage_I_sec2, A=0.5*Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage), K=0.5)
    Fuselage_Transverse_Shear_sec2 = Shear_Transverse_General(F=(Fuselage_Sec1_Load_Total+Fuselage_length_sec2*Fuselage_Sec1_Load+Payload_Force*Payload_Location),Q=First_Area_Q_SemiCircle(R_in=R_in_fuselage,R_out=R_out_fuselage,t=Fuselage_t), I=Fuselage_I_sec2,t=Fuselage_t)  
    Fuselage_Bending_Stress_sec2 = Bending_Simple(M=-(Fuselage_Sec1_Load_Total+0.5*Fuselage_sec2_load*(Fuselage_length_sec2**2)), Y=R_out_fuselage,I=Fuselage_I_sec2)

    Fuselage_VonMises_Sec2_Stress, Fuselage_VonMises_Sec2_Shear = Von_Mises(Stress_X=(Main_Engine_Thrust/0.5*Tube_Area(R_in=R_in_fuselage,R_out=R_out_fuselage)),Stress_Y=0,Stress_Z=Fuselage_Bending_Stress_sec2,Shear_XY=(Fuselage_Transverse_Shear_sec2+Fuselage_Torsion_Sec2),Shear_YZ=0, Shear_ZX=0)

    if Fuselage_VonMises_Sec2_Stress < Yield_Stress_Fuselage and Fuselage_VonMises_Sec2_Stress < Fuselage_Buckle_sec2 and Fuselage_VonMises_Sec2_Shear < Yield_shear_Fuselage:
        Big_Owie_Fuselage_Flying = False 
        print("Passes Section 2")
    else:
        R_out_fuselage +=1/1000
        Big_Owie_Fuselage_Flying = False 


    #SECTION 3:
    Fuselage_t = R_out_fuselage-R_in_fuselage
    Fuselage_Sec2_Load_Total = Fuselage_Sec1_Load*Fuselage_length_sec1+Payload_Force+Fuselage_length_sec2*Fuselage_sec2_load

    Fuselage_J_sec3 = Circle_Polar_Moment_of_Inertia(R_out=R_out_fuselage,R_in=R_in_fuselage)
    Fuselage_I_sec3 = Circle_Moment_of_Inertia(R_Out=R_out_fuselage , R_in=R_in_fuselage)

    Fuselage_Torsion_Sec3 = Shear_Circle_Torsion(T=Main_Engine_Torque,r=R_out_fuselage,J=Fuselage_J_sec3)
    Fuselage_Buckle_sec2 = Buckling_Stress(E=Material_Fuselage.E, L=Fuselage_length_sec3, I= Fuselage_I_sec3, A=Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage), K=2)
    Fuselage_Transverse_Shear_sec3 = Shear_Transverse_Circle(R_in=R_in_fuselage,R_out=R_out_fuselage,F=(Main_Engine_Thrust-Payload_Drag))






#Calculate Mass
Tail_pole_mass = Volume(A=Tube_Area(R_out=R_out_Tail,R_in=R_in_Tail), L=Entire_Tail_Length)*Density_Tail
WingBox_Mass = Volume(A=Tube_Area(R_out=R_out_WingBox,R_in=R_in_WingBox), L=WingBox_length)*Density_WingBox

Vtol_Pole_Mass_front = Volume(A=Tube_Area(R_out=R_out_VTOL_front,R_in=R_in_VTOL_front), L=Vtol_Pole_Length_front)*Density_VTOL
Vtol_Pole_Mass_back = Volume(A=Tube_Area(R_out=R_out_VTOL_back,R_in=R_in_VTOL_back), L=Vtol_Pole_Length_back)*Density_VTOL

Vtol_Pole_Mass = Vtol_Pole_Mass_front + Vtol_Pole_Mass_back
print("VTOL Pole Mass:", Vtol_Pole_Mass)

TOTAL_MASS = 2*WingBox_Mass + 4*Vtol_Pole_Mass + 2*Tail_pole_mass
print("Yippee")
print("Yippee")
print("Yippee")
print("Yippee")
print("Yippee")
print(Tail_pole_mass)
print(Vtol_Pole_Mass)
print(WingBox_Mass)
print(TOTAL_MASS)
print("-------------------------------------------")


