import numpy as np
import matplotlib as plt
import pandas as pd


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


def Shear_Transverse_General(F,Q,I,t):
    Shear = (F*Q)/(I*t)
    return Shear


def Shear_Transverse_Rectangle(F,B,H):
    Shear = 1.5*(F/(B*H)) #See MOM textbook, specifically page 394
    return Shear 


def Shear_Transverse_Circle(R_in,R_out,F):
    Shear = (4/3)*F*( (R_out**2 + R_in**2 + R_in*R_out) / (np.pi*(R_out**4-R_in**4)) )
    return Shear


def Buckling_Stress(E,L,r,K):  #K=1 for pin ends, 2 for fixed and free combo, 0.5 for both fixed, 0.7 for pinned and fixed. SEE P693 OF MOM
    Stress = (E*np.pi**2)/((K*L/r)**2)
    return Stress


def Shear_Torsional(T,A_m,t):
    Shear = T/(2*A_m*t)
    return Shear


def Tip_Deflection(F,L,E,I):
    V_tip = (F*L**4)/(8*E*I)
    return V_tip