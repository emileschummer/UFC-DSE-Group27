import numpy as np
import matplotlib as plt
import pandas as pd
from InertiaCalcs import *
from ForceAndStressCals import *
from Materials import *
from AirFoilDataExtraction import *
from scipy.integrate import quad

#------------------------------------------------------
#TODO ADD A SAFETY FACTOR 1.5
#TODO VIBRATIONS --> FLUTTER !!!!---->no, just,no >:(
#TODO ASK ALEX FOR FEEDBACK
#TODO INCLUDE TAIL IN ENGINE FORCE
#TODO CHECK VON MISES FO ALL, ITS FOR CROSS SECTION POINT, NOT ENTIRE CROSS SECTION FFFFFFUUUUUUUUUUUCCCCCCCCCKKKKKKKKKK
#------------------------------------------------------

#FUNCTIONS TO RUN
Big_owie_WingBox = False #UNDER RENOVATIONS
Big_Owie_VTOL_front = True
Big_Owie_VTOL_back = True
Big_Owie_Fuselage_Flying = True
Big_Owie_Leg = True


#Create the material
Material_Tail = PLA3DPrintMaterial() # DogshitTestMaterial() #
Yield_shear_Tail= Material_Tail.Yield_Shear
Yield_Stress_Tail = Material_Tail.Yield_Stress
Density_Tail = Material_Tail.Density

Material_VTOL = PLA3DPrintMaterial()# DogshitTestMaterial() #
Yield_shear_VTOL= Material_VTOL.Yield_Shear
Yield_Stress_VTOL = Material_VTOL.Yield_Stress
Density_VTOL = Material_VTOL.Density

Material_WingBox = PLA3DPrintMaterial() #DogshitTestMaterial() #
Yield_shear_WingBox= Material_WingBox.Yield_Shear
Yield_Stress_WingBox = Material_WingBox.Yield_Stress
Density_WingBox = Material_WingBox.Density

Material_Leg = PLA3DPrintMaterial() #DogshitTestMaterial() #
Yield_shear_Leg = Material_Leg.Yield_Shear
Yield_Stress_Leg = Material_Leg.Yield_Stress
Density_Leg = Material_Leg.Density

Material_Fuselage = PLA3DPrintMaterial() #DogshitTestMaterial() #
Yield_shear_Fuselage = Material_Fuselage.Yield_Shear
Yield_Stress_Fuselage = Material_Fuselage.Yield_Stress
Density_Fuselage = Material_Fuselage.Density


#VTOL POLES FRONT GEOMETRY
R_in_VTOL_front = 0.17 
R_out_VTOL_front = 0.1705
d_prop= 0.7366
R_prop = d_prop/2	
MAC= 0.35
Vtol_Pole_Length_front = 1.1*R_prop+ 0.12*MAC

#VTOL POLES BACK GEOMETRY
R_in_VTOL_back = 0.17
R_out_VTOL_back = 0.1705
d_prop= 0.7366
R_prop = d_prop/2	
MAC= 0.35
Vtol_Pole_Length_back = 1.1*R_prop+ 0.24*MAC


#FUSELAGE GEOMETRY
R_out_fuselage = 0.3+1/1000 
R_in_fuselage = 0.3

Fuselage_length_sec1 = 0.2
Fuselage_length_sec2 = 0.4
Fuselage_length_sec3 = 0.3

Payload_Location = 0.6-Fuselage_length_sec1 #edit the o.6 to the location, starting from the back of the fuselage
Wing_Hole_location = 0.8-Fuselage_length_sec1-Fuselage_length_sec2 #edit the 0.8, again measurong from the start of the back of the plane

#TAIL GEOMETRY
Tail_Effective_Length = 0.11 #Meters
Entire_Tail_Length = 1 #meters
# Momenent_Acting_Point_Tail = Entire_Tail_Length - (Tail_Length*0.5)

R_in_Tail = 0.01
R_out_Tail = 0.015

#LEG GEOMETRY
Leg_Length = 0.5
R_in_Leg= 1/1000
R_out_Leg = 2/1000
Leg_Angle = np.deg2rad(30) #deg

#VTOL LOADS
F_Vtol = 70.6 #25*9.81/4 #Newtons
T_Vtol = 2.28 #Newtons/Meter

#MAIN ENGINE LOADS (I GOOFED THE NAMING CONVENTION SO IT HAS 2 NAMES)
F_prop = 100 #Newtons
T_prop = 1 #Newtons /Meter
Main_Engine_Thrust = F_prop
Main_Engine_Torque = T_prop

#TAIL LOADS
Tail_loading_horizontal_Distributed = 20 #Newtons per meter
Tail_loading_Vertical_Distributed = 30 #Newtons per meter

#FUSELAGE lOADS
Fuselage_Sec1_Load = 10 #N*m SENSORS+COMSS+MAIN MOTOR (distributed load)
Fuselage_sec2_load = 15 #N*m BATTERY+PARACHUTE
Payload_Force = 9.81*0.7 #N includes Gimbal and Camera weight
Payload_Drag = 10 #N includes Gimbal and Camera drag


#LEG LOADS
Leg_Force = (25*9.81)/4
Leg_Force_X = Leg_Force*np.sin(Leg_Angle)
Leg_Force_Y = Leg_Force*np.cos(Leg_Angle)


#THE SIMULATION
while Big_Owie_VTOL_front:
    VTOL_I_Front = Circle_Moment_of_Inertia(R_out_VTOL_front,R_in_VTOL_front)

    VTOL_stress_Front = Bending(Mx=(T_Vtol),Ix=VTOL_I_Front,X=R_out_VTOL_front,My=(F_Vtol*Vtol_Pole_Length_front),Iy=VTOL_I_Front,Y=R_out_VTOL_front)
    VTOL_Trans_Shear_Front = Shear_Transverse_Circle(R_in=R_in_VTOL_front,R_out=R_out_VTOL_front, F=F_Vtol)

    VTOL_VonMises_Front_Stress,VTOL_VonMises_Front_Shear = Von_Mises(Stress_X=0,Stress_Y=0,Stress_Z=VTOL_stress_Front,Shear_XY=(VTOL_Trans_Shear_Front),Shear_YZ=0,Shear_ZX=0)

    print("----------------------------------------------------")
    print("The Max Shear FRONT VTOL:",VTOL_VonMises_Front_Stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress FRONT VTOL:",VTOL_VonMises_Front_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The FRONT VTOL Thickness:",R_out_VTOL_front-R_in_VTOL_front)

    if VTOL_VonMises_Front_Stress < Yield_Stress_VTOL and VTOL_VonMises_Front_Shear <Yield_shear_VTOL:
        Big_Owie_VTOL_front = False
    else:
        R_out_VTOL_front +=0.001



while Big_Owie_VTOL_back:
    VTOL_I_Back = Circle_Moment_of_Inertia(R_out_VTOL_back,R_in_VTOL_back)
    VTOL_J_Back = Circle_Polar_Moment_of_Inertia(R_out=R_out_VTOL_back,R_in=R_in_VTOL_back)

    #VTOL_stress_Front = Bending_Simple(M=F_Vtol*Vtol_Pole_Length_front , Y=R_out_VTOL_front, I=VTOL_I_Front) #Bending(M_y, Iy, R_out_VTOL_front, M_z, Iz, R_out_VTOL_front)
    VTOL_Trans_Shear_Back_Y = Shear_Transverse_Circle(R_in=R_in_VTOL_back,R_out=R_out_VTOL_back,F=(F_Vtol+Tail_loading_Vertical_Distributed*Tail_Effective_Length))
    VTOL_Trans_Shear_Back_Z = Shear_Transverse_Circle(R_in=R_in_VTOL_back,R_out=R_out_VTOL_back,F=Tail_Effective_Length*Tail_loading_horizontal_Distributed)
    VTOL_stress_Back = Bending(Mx=(T_Vtol+Tail_loading_horizontal_Distributed*Tail_Effective_Length*(Entire_Tail_Length-0.5*Tail_Effective_Length)) ,Ix=VTOL_I_Back,X=R_out_VTOL_back,My=(F_Vtol*Vtol_Pole_Length_back+Tail_loading_Vertical_Distributed*Tail_Effective_Length*(Entire_Tail_Length-0.5*Tail_Effective_Length)) ,Iy=VTOL_I_Back,Y=R_out_VTOL_back)

    VTOL_VonMises_Back_Stress,VTOL_VonMises_Back_Shear = Von_Mises(Stress_X=0,Stress_Y=0,Stress_Z=VTOL_stress_Back,Shear_XY=VTOL_Trans_Shear_Back_Y,Shear_YZ=VTOL_Trans_Shear_Back_Z,Shear_ZX=0)

    print("----------------------------------------------------")
    print("The Max Shear BACK VTOL:",VTOL_VonMises_Back_Stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress BACK VTOL:",VTOL_VonMises_Back_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The BACK VTOL Thickness:",R_out_VTOL_back-R_in_VTOL_back)

    if VTOL_VonMises_Back_Stress < Yield_Stress_VTOL and VTOL_VonMises_Back_Shear <Yield_shear_VTOL:
        Big_Owie_VTOL_back = False
    else:
        R_out_VTOL_back +=0.001


#WINGBOX GEOMETRY
Vtol_Location = 0.5 #along the wingbox
WingBox_length = 1.5
R_in_WingBox = 0.1
R_out_WingBox = 0.11

#WING LOADS
Wing_Torque = 100 #MAX WING TORQUE
Wing_Lift_Distribution = 10 #Should be an elliptical func, we will figure it out later REMEMBER -WL^2/2
Wing_Max_Lift = 100

#NEWLY DEFINED FROM VTOL
Wing_MY=Tail_Effective_Length*Tail_loading_horizontal_Distributed*(Entire_Tail_Length-0.5*Tail_Effective_Length)
Wing_MZ=( Wing_Torque -
            (F_Vtol*Vtol_Pole_Length_back+Tail_loading_Vertical_Distributed*Tail_Effective_Length*(Entire_Tail_Length-0.5*Tail_Effective_Length))
            + ( F_Vtol*Vtol_Pole_Length_front))

while Big_owie_WingBox:
    WingBox_t = R_out_WingBox - R_in_WingBox
    WingBox_I = Circle_Moment_of_Inertia(R_Out=R_out_WingBox,R_in=R_in_WingBox)
    WingBox_Q = First_Area_Q_Circle(R_out=R_out_WingBox,R_in=R_in_WingBox,t=WingBox_t)
    WingBox_J = Circle_Polar_Moment_of_Inertia(R_out=R_out_WingBox,R_in=R_in_WingBox)

    WingBox_Transverse_Shear_lift = Shear_Transverse_Circle(R_in=R_in_WingBox,R_out=R_out_WingBox,F=(Wing_Max_Lift-2*F_Vtol))
    WingBox_Transverse_Shear_Tail = Shear_Transverse_Circle(R_in=R_in_WingBox,R_out=R_out_WingBox,F=(Tail_Effective_Length*Tail_loading_horizontal_Distributed))

    WingBox_Torsion_Shear_Z = Shear_Circle_Torsion(T=(Wing_MZ),r=R_out_WingBox,J=WingBox_J)
    WingBox_Torsion_Shear_Y = Shear_Circle_Torsion(T=(Wing_MY),r=R_out_WingBox,J=WingBox_J)

    WingBox_Bending = Bending(Mx=(),
                              My=(),
                              Ix=WingBox_I,Iy=WingBox_I,X=R_out_WingBox,Y=R_out_WingBox)
    


    # WingBox_Transverse_Shear_lift = Shear_Transverse_General(F = WingBox_Max_Lift, Q= WingBox_Q, I= WingBox_Ix, t=WingBox_t) #modelling for max shear, where force transfered from VTOl
    # WingBox_Torsion_Shear = Shear_Circle_Torsion(T=WingBox_Torque, r=R_out_WingBox, J= WingBox_J)

    # WingBox_Stress = Bending(Mx=M_x_WingBox ,Ix=WingBox_Ix, X= R_out_WingBox,My=M_y_WingBox ,Iy=WingBox_Iy,Y=R_out_WingBox) 
    # WingBox_Total_Shear = WingBox_Torsion_Shear+WingBox_Transverse_Shear_lift

    # Tresca_Stress_Wingbox = Tresca(Stress1=WingBox_Stress,Stress2=0,Shear=WingBox_Total_Shear)
    # Von_Mises_Wingbox_Stress, Von_Mises_Wingbox_Shear = Von_Mises(Stress_X=WingBox_Stress,Stress_Y=0,Stress_Z=0,Shear_XY=WingBox_Total_Shear,Shear_YZ=0,Shear_ZX=0)
    
    # WingBox_Deflection = Tip_Deflection(F=WingBox_Lift_Distribution,L=WingBox_length,E=Material_WingBox.E,I=WingBox_Ix)
    # WingBox_Twist_Angle = Twist(T = WingBox_Torque,  L= WingBox_length, G=Material_WingBox.G, J=WingBox_J)


    print("----------------------------------------------------")
    print("The Tresca Stress WingBox:",Tresca_Stress_Wingbox, "The Yield Shear:",Yield_Stress_WingBox)
    print("The Von Mises Stress Wingbox:",Von_Mises_Wingbox_Stress,"The yield stress", Yield_Stress_WingBox)
    print("The Von Mises Shear Wingbox:",Von_Mises_Wingbox_Shear,"The yield stress", Yield_shear_WingBox )
    print("The Wingbox Thickness:",WingBox_t)


    if Tresca_Stress_Wingbox < Yield_Stress_WingBox and Von_Mises_Wingbox_Stress < Yield_Stress_WingBox and Von_Mises_Wingbox_Shear < Yield_Stress_WingBox and WingBox_Deflection < 0.05*WingBox_length:
        Big_owie_WingBox = False
    else:
        R_out_WingBox +=0.001



while Big_Owie_Leg:
    Leg_Ix = Circle_Moment_of_Inertia(R_Out=R_out_Leg,R_in=R_in_Leg)

    Leg_Bending = Bending_Simple(M=(Leg_Length*Leg_Force_X), Y=R_out_Leg, I=Leg_Ix)
    Leg_Transverse_Shear = Shear_Transverse_Circle(R_in=R_in_Leg,R_out=R_out_Leg,F=Leg_Force_X)

    Leg_Buckle = Buckling_Stress(E=Material_Leg.E, L=Leg_Length,I=Leg_Ix,A=Tube_Area(R_out=R_out_Leg,R_in=R_in_Leg),K=2)

    Leg_Von_Mises_Stress, Leg_Von_Mises_Shear = Von_Mises(Stress_X=Leg_Bending,Stress_Y=(Leg_Force_Y/Tube_Area(R_in=R_in_Leg,R_out=R_out_Leg)),Stress_Z=0,Shear_XY=Leg_Transverse_Shear,Shear_YZ=0,Shear_ZX=0)

    print("----------------------------------------------------")
    print("The Von Mises Stress Leg:",Leg_Von_Mises_Stress,"The yield stress", Yield_Stress_Leg)
    print("The Von Mises Shear Leg:",Leg_Von_Mises_Shear,"The yield stress", Yield_shear_Leg)
    print("The Leg:",R_out_Leg-R_in_Leg)

    if Leg_Von_Mises_Stress < Yield_Stress_Leg and Leg_Von_Mises_Shear < Yield_shear_Leg and Leg_Buckle > Yield_Stress_Leg:
        Big_Owie_Leg = False
    else:
        R_out_Leg +=(1/1000)



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


    #SECTION 2:
    Fuselage_Sec1_Load_Total = Fuselage_Sec1_Load*Fuselage_length_sec1
    Fuselage_I_sec2 = Semi_Circle_Moment_of_Inertia(R_out=(R_out_fuselage-0.5*Fuselage_t), t=Fuselage_t)

    Fuselage_Torsion_Sec2 = Torsion_Open(T=Main_Engine_Torque, l= Fuselage_length_sec2, t=Fuselage_t)
    Fuselage_Buckle_sec2 = Buckling_Stress(E=Material_Fuselage.E, L=Fuselage_length_sec2, I=Fuselage_I_sec2, A=0.5*Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage), K=0.5)
    Fuselage_Transverse_Shear_sec2 = Shear_Transverse_General(F=(Fuselage_Sec1_Load_Total+Fuselage_length_sec2*Fuselage_Sec1_Load+Payload_Force*Payload_Location),Q=First_Area_Q_SemiCircle(R_in=R_in_fuselage,R_out=R_out_fuselage,t=Fuselage_t), I=Fuselage_I_sec2,t=Fuselage_t)  
    Fuselage_Bending_Stress_sec2 = Bending_Simple(M=-(Fuselage_Sec1_Load_Total+0.5*Fuselage_sec2_load*(Fuselage_length_sec2**2)), Y=R_out_fuselage,I=Fuselage_I_sec2)

    Fuselage_VonMises_Sec2_Stress, Fuselage_VonMises_Sec2_Shear = Von_Mises(Stress_X=(Main_Engine_Thrust/0.5*Tube_Area(R_in=R_in_fuselage,R_out=R_out_fuselage)),Stress_Y=0,Stress_Z=Fuselage_Bending_Stress_sec2,Shear_XY=(Fuselage_Transverse_Shear_sec2+Fuselage_Torsion_Sec2),Shear_YZ=0, Shear_ZX=0)


    #SECTION 3:
    Fuselage_Sec2_Load_Total = Fuselage_Sec1_Load*Fuselage_length_sec1+Payload_Force+Fuselage_length_sec2*Fuselage_sec2_load
    Fuselage_Sec3_X_Load = Main_Engine_Thrust-Payload_Drag

    Fuselage_J_sec3 = Circle_Polar_Moment_of_Inertia(R_out=R_out_fuselage,R_in=R_in_fuselage)
    Fuselage_I_sec3 = Circle_Moment_of_Inertia(R_Out=R_out_fuselage , R_in=R_in_fuselage)
    Cutout_Correction = Cut_Out_Corrections(Diamater=R_out_WingBox,Width=Fuselage_length_sec3)

    Fuselage_Torsion_Sec3 = Shear_Circle_Torsion(T=Main_Engine_Torque,r=R_out_fuselage,J=Fuselage_J_sec3)
    Fuselage_Buckle_sec3 = Buckling_Stress(E=Material_Fuselage.E, L=Fuselage_length_sec3, I= Fuselage_I_sec3, A=Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage), K=2)
    Fuselage_Transverse_Shear_sec3 = Shear_Transverse_Circle(R_in=R_in_fuselage,R_out=R_out_fuselage,F=(Main_Engine_Thrust-Payload_Drag))
    Fuselage_Bending_Stress_sec3 = Bending_Simple(M=(Fuselage_Sec2_Load_Total*Wing_Hole_location),Y=R_out_fuselage,I=Fuselage_I_sec3) #Bending(Mx=(),Ix=Fuselage_I_sec3,X=R_out_fuselage,My=(),Iy=Fuselage_I_sec3,Y=R_out_fuselage)

    Fuselage_VonMises_Sec3_Stress, Fuselage_VonMises_Sec3_Shear = Von_Mises(Stress_X=Cutout_Correction*(Fuselage_Sec3_X_Load*Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage)),Stress_Y=0, Stress_Z=Cutout_Correction*Fuselage_Bending_Stress_sec3, Shear_XY=Cutout_Correction*(Fuselage_Torsion_Sec3+Fuselage_Transverse_Shear_sec3),Shear_YZ=0,Shear_ZX=0 )

    #COMPARING
    if Fuselage_VonMises_Sec1_Stress < Yield_Stress_Fuselage and Fuselage_VonMises_Sec1_Stress < Fuselage_Buckle_sec1 and Fuselage_VonMises_Sec1_Shear < Yield_shear_Fuselage:
        print("Passes Section 1")
        if Fuselage_VonMises_Sec2_Stress < Yield_Stress_Fuselage and Fuselage_VonMises_Sec2_Stress < Fuselage_Buckle_sec2 and Fuselage_VonMises_Sec2_Shear < Yield_shear_Fuselage:
            print("Passes Section 2")
            if Fuselage_VonMises_Sec3_Stress < Yield_Stress_Fuselage and Fuselage_VonMises_Sec3_Stress < Fuselage_Buckle_sec3 and Fuselage_VonMises_Sec3_Shear < Yield_shear_Fuselage:
                print("Passes Section 3")
                Big_Owie_Fuselage_Flying = False 
            else:
                R_out_fuselage +=1/1000
                Big_Owie_Fuselage_Flying = True 
        else:
            R_out_fuselage +=1/1000
            Big_Owie_Fuselage_Flying = True 
    else:
        R_out_fuselage +=1/1000
        Big_Owie_Fuselage_Flying = True 





#Calculate Mass
print("-------------------------------------------")
Vtol_Pole_Mass_front = Volume(A=Tube_Area(R_out=R_out_VTOL_front,R_in=R_in_VTOL_front), L=Vtol_Pole_Length_front)*Density_VTOL
Vtol_Pole_Mass_back = Volume(A=Tube_Area(R_out=R_out_VTOL_back,R_in=R_in_VTOL_back), L=Entire_Tail_Length)*Density_VTOL
Vtol_Pole_Mass = 2*(Vtol_Pole_Mass_front + Vtol_Pole_Mass_back)
print("VTOL POLE MASS:", Vtol_Pole_Mass)

Fuselage_Mass = Volume(A=Tube_Area(R_in=R_in_fuselage,R_out=R_out_fuselage), L=(Fuselage_length_sec2+Fuselage_length_sec1+Fuselage_length_sec3))*Density_Fuselage
print('FUSELAGE MASS:', Fuselage_Mass)

Leg_Mass = 4*( Volume(A=Tube_Area(R_out=R_out_Leg,R_in=R_in_Leg) ,L=Leg_Length) )
print("LEG MASS:", Leg_Mass)

Total_Mass = Leg_Mass+Vtol_Pole_Mass+Fuselage_Mass
print("-------------------------------------------")
print("THE FINAL FUCKING MASS:", Total_Mass)
print("-------------------------------------------")


