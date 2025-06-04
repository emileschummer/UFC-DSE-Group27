import aerosandbox as asb
import numpy as np 
from matplotlib import pyplot as plt
from aerosandbox import XFoil, Airfoil, Wing, WingXSec
from Functions import load_airfoil_dat
from AirfoilAnalysis import my_airfoil

wing = Wing(
    name="Demo Wing",
    xsecs=[
        WingXSec(
            xyz_le=[0, 0, 0],         # Root leading edge
            chord=0.45,                # Root chord
            twist=0,                  # Root twist
            airfoil=my_airfoil,     # Root airfoil
        ),
        WingXSec(
            xyz_le=[0, 1.5, 0],        # Tip leading edge
            chord=0.25,                # Tip chord
            twist=0,                 # Tip twist
            airfoil=my_airfoil,      # Tip airfoil
        ),
    ],
    symmetric=True,                   # Mirror across y=0
)

print("span", wing.span())
print("area", wing.area())
print("aspect ratio", wing.aspect_ratio())
print("mean geometric chord", wing.mean_geometric_chord())
print("mean aerodynamic wing", wing.mean_aerodynamic_chord())
print("aerodynamic center", wing.aerodynamic_center())
print("volume", wing.volume())