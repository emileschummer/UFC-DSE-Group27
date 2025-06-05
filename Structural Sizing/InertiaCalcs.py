import numpy as np
import matplotlib as plt
import pandas as pd


#I dunno where to put this yet but to record:
# r = np.sqrt(I/A) called radius of gyration. used in buckling

def I_beam_Area(H,B,t1,t2,t3):
    A = H*t2+B*t1+B*t3
    return A


def Tube_Area(R_out,R_in):
    A = np.pi*(R_out**2 - R_in**2)
    return A


def Circle_Moment_of_Inertia(R_Out,R_in):
    I = (np.pi)/4 * (R_Out**4 - R_in**4)
    return I


def Rectangle_Moment_of_Inertia(B,H):
    I_x = (B*H**3)/12
    return I_x


def I_Beam_Moment_of_Inertia(t1,t2,t3,B,H):
    X1 = (t2*H**3)/12
    X2 = (B*t3**3)/12 + B*t3*(0.5*H*t3)**2
    X3 = (B*t1**3)/12 + B*t1*(0.5*H*t1)**2
    I = X1+X2+X3
    return I


def WingBox_Moment_of_inertia(B,H,t):
    I = ( (B*t**3)/12 + B*t*(H/2 - t/2)**2 + t*H**3/12 )*2#symmetry
    return I


def Circle_Polar_Moment_of_Inertia(R_out,R_in):
    J = (np.pi/2)*(R_out**2 - R_in**4)
    return J


def First_Area_Q_WingBox(H,B,t): #Fuck u, uniform thickness only
    X1 = 0.5*B*t*(H-t)
    X2 = (0.5*H*t-t**2)*(0.25*H - 0.5*t)
    Q = X1+X2
    return Q


def First_Area_Q_IBeam(B,H,t1,t2):
    X1 = (0.5*H+0.5*t1)*(B*H)
    X2 = (0.25*H)*(0.25*H*t2)
    Shear = X1+X2
    return Shear


def Spring_Constant(E,A,L):
    K = (E*A)/L
    return K



def TheSuperSecretFunction():
    import time
    import webbrowser
    ImportantStressThing = "https://youtube.com/shorts/41iWg91yFv0?si=3yS7CuMoRXtxr3bn"
    webbrowser.open(ImportantStressThing)
    time.sleep(1.5) 