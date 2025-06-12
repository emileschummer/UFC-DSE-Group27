import numpy as np
import matplotlib as plt
import pandas as pd
from scipy.integrate import quad


def Max_Force(l, F1_eq, F2_eq):
    steps = l/0.001
    Max = 0
    for i in range(steps):
        F1 = F1_eq*(i*0.001)
        F2 = F2_eq*(i*0.001)
        if (F1+F2)>Max:
            Max = F1+F2
    return Max


def Bending_Simple(M,Y,I):
    Stress = (M*Y)/I
    return Stress


def Bending(Mx,Ix,X,My,Iy,Y):
    Stress = ((Mx*Iy*Y)+(My*Ix*X) )/(Ix*Iy)
    return Stress


def Shear_Circle_Torsion(T,r,J):
    Shear = (T*r)/J
    return Shear


def Shear_Torsion(T,t,A):
    Shear = T/(2*t*A)
    return Shear


def Torsion_Open(T,l,t): #Assuming plate theory, see SAD
    Shear = (3*T)/(l*t**2)
    return Shear


def Shear_Transverse_General(F,Q,I,t):
    Shear = (F*Q)/(I*t)
    return Shear


def Shear_Transverse_Rectangle(F,B,H):
    Shear = 1.5*(F/(B*H)) #See MOM textbook, specifically page 394
    return Shear 


def Shear_Transverse_Circle(R_in,R_out,F):
    Shear = (4/3)*F*( (R_out**2 + R_in**2 + R_in*R_out) / (np.pi*(R_out**4-R_in**4)) )
    return Shear


def Buckling_Stress(E,L,I,A,K):  #K=1 for pin ends, 2 for fixed and free combo, 0.5 for both fixed, 0.7 for pinned and fixed. SEE P693 OF MOM
    r = np.sqrt(I/A) #called radius of gyration. used in buckling
    Stress = (E*np.pi**2)/((K*L/r)**2)
    return Stress


def Shear_Torsional(T,A_m,t):
    Shear = T/(2*A_m*t)
    return Shear


def Tip_Deflection(F,L,E,I):
    V_tip = (F*L**4)/(8*E*I)
    print(V_tip)
    return V_tip

def Twist(T,L,G,J):
    angle = np.rad2deg( (T*L)/(G*J) )
    print(angle)
    return angle

#TRESCA AND VON MISES

def Tresca(Stress1, Stress2, Shear):# Give biggest stress at Stress1
    Stress_Avg = (Stress1+Stress2)/2
    R = np.sqrt( Shear**2 + (Stress1-Stress_Avg)**2 )
    Theta1 = Stress_Avg+R
    Theta2 = Stress_Avg-R
    Shear_Max = np.absolute( (Theta1-Theta2)/2 )
    return 2*Shear_Max


def Von_Mises(Stress_X,Stress_Y,Stress_Z,Shear_XY,Shear_YZ,Shear_ZX):
    Temp1 = (Stress_X-Stress_Y)**2 + (Stress_Y-Stress_Z)**2 + (Stress_Z-Stress_X)**2
    Temp2 = 6*(Shear_XY**2 + Shear_YZ**2 + Shear_ZX**2)
    Stress_Von_Mises = 1/np.sqrt(2) * np.sqrt(Temp1+Temp2)
    Shear_Von_Mises = Stress_Von_Mises/np.sqrt(3)
    return Stress_Von_Mises , Shear_Von_Mises


def Cut_Out_Corrections(Diamater, Width):#Diameter= Entire hole diameter, Width = panel width
    K_t = 2+(1 + (Diamater/Width))**3
    return K_t


def Compute_Total_Lift_and_Centroid(Y_func, a, b):
    total_lift, _ = quad(Y_func, a, b)
    moment, _ = quad(lambda x: x * Y_func(x), a, b)
    x_centroid = moment / total_lift 

    return total_lift, x_centroid

# lift, centroid = Compute_Total_Lift_and_Centroid(Y, 0, 10)
# print(f"Total Lift: {lift:.2f} N")
# print(f"Centroid (spanwise): {centroid:.2f} m")
