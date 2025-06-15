import numpy as np
import matplotlib as plt
import pandas as pd

#I dunno where to put this yet but to record:
# r = np.sqrt(I/A) called radius of gyration. used in buckling


#-----------------------------------------------------------------------
#AREA MOMENT OF INERTIA 
#-----------------------------------------------------------------------
def Circle_Moment_of_Inertia(R_Out,R_in):
    I = (np.pi)/4 * (R_Out**4 - R_in**4)
    return I


def Solid_Circle_moment_of_Inertia(R):
    d = 2*R
    I = (np.pi*d**4)/64
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
    I = ( (B*t**3)/12 + B*t*(H/2 - t/2)**2 + (t*(H-2*t)**3)/12 )*2#symmetry
    return I


def Circle_Polar_Moment_of_Inertia(R_out,R_in):
    J = (np.pi/2)*(R_out**4 - R_in**4)
    return J

def Circle_Polar_Moment_of_Inertia2(t,R_out):
    d = R_out*2
    J = (np.pi*t*d**3)/4
    return J


def Semi_Circle_Moment_of_Inertia_Fuselage(R_out,R_in,B,H,t_Ibeam):
    #I = (np.pi/2 - 4/np.pi)*t*R_out**3
    I_Semi = (np.pi/8)*(R_out**4 - R_in**4)
    Centre = (2*R_out/np.pi)
    I_Beam = I_Beam_Moment_of_Inertia(t1=t_Ibeam,t2=t_Ibeam,t3=t_Ibeam,B=B,H=H)
    I_Semi_parallel = I_Semi + 0.5*Tube_Area(R_out=R_out,R_in=R_in)*(Centre)**2
    I_Beam_parallel = I_Beam + I_beam_Area(t1=t_Ibeam,t2=t_Ibeam,t3=t_Ibeam,B=B,H=H)*(R_out-Centre-0.5*H)**2
    I_total = I_Beam_parallel+I_Semi_parallel
    return I_total


def Semi_Circle_Moment_of_Inertia(R_in,R_out):
    I_Base = (np.pi/8)*(R_out**4 - R_in**4)
    Centre = (2*R_out/np.pi)
    I = I_Base + 0.5*Tube_Area(R_out=R_out,R_in=R_in)*(Centre)**2
    return I

#-----------------------------------------------------------------------
#FIRST MOMENT AREA (Q)
#-----------------------------------------------------------------------
def First_Area_Q_WingBox(H,B,t): #Fuck u, uniform thickness only >:(
    X1 = 0.5*B*t*(H-t)
    X2 = (0.5*H*t-t**2)*(0.25*H - 0.5*t)
    Q = X1+X2
    return Q


def First_Area_Q_IBeam(B,H,t1,t2):
    X1 = (0.5*H+0.5*t1)*(B*H)
    X2 = (0.25*H)*(0.25*H*t2)
    Shear = X1+X2
    return Shear


def First_Area_Q_Circle(R_out,R_in,t):
    Y = np.pi*(4/3)*( (R_out**3-R_in**3)/(R_out**2-R_in**2) ) #Source: ChatGPT
    A = 0.5*np.pi*(R_out**2 - R_in**2)
    Q = Y*A
    return Q


def First_Area_Q_SemiCircle(t,R_in,R_out):
    Q = 2*t*(0.5*(R_in+R_out))**2
    return Q


#-----------------------------------------------------------------------
#OTHER
#-----------------------------------------------------------------------
def Spring_Constant(E,A,L):
    K = (E*A)/L
    return K


def TheSuperSecretFunction():
    import time
    import webbrowser
    ImportantStressThing = "https://youtube.com/shorts/41iWg91yFv0?si=3yS7CuMoRXtxr3bn"
    webbrowser.open(ImportantStressThing)
    time.sleep(1.5) 


def SummonTheCouncil():
    import time
    import webbrowser
    Member1 = "https://chat.deepseek.com/"
    Member2 = "https://chat.mistral.ai/chat?q="
    Member3 = "https://gemini.google.com/app"
    Member4 = "https://chatgpt.com/?model=gpt-4o"
    webbrowser.open(Member1)
    webbrowser.open(Member2)
    webbrowser.open(Member3)
    webbrowser.open(Member4)



#-----------------------------------------------------------------------
#AREA AND VOLUME
#-----------------------------------------------------------------------
def Tube_Area(R_out,R_in):
    A = np.pi*(R_out**2 - R_in**2)
    return A


def I_beam_Area(H,B,t1,t2,t3):
    A = H*t2+B*t1+B*t3
    return A


def WingBox_Area(B,H,t):
    A = H*B-( (B-2*t)*(H-2*t) )
    return A


def Volume(A,L):
    return A*L


X1 = (Semi_Circle_Moment_of_Inertia(R_out=0.2,R_in=0.19))
X2 = (Semi_Circle_Moment_of_Inertia_Fuselage(R_out=0.2,R_in=0.19,t_Ibeam=0.002,H=0.02,B=0.01))
print(X2,X1,X2-X1)
if X1 > X2:
    print("hm, le feck")