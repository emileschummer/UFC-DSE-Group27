import aerosandbox as asb
import numpy as np 
from matplotlib import pyplot as plt
from aerosandbox import XFoil, Airfoil, Atmosphere, OperatingPoint
import pandas as pd

from Functions import load_airfoil_dat, Re

# Airfoli name and coordinates, 
# Place dat file as argument
coordinates = load_airfoil_dat(r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\Airfoil.dat")
name = "S1223"

my_airfoil = Airfoil(name = name, coordinates = coordinates)

#set flight conditions here
FlightVelocity = 10 #[m/s]
Altitude = 1000
alphas = np.linspace(-10, 30, 41)

atmo = Atmosphere(Altitude)  # Create an Atmosphere instance 

OpPoint = OperatingPoint(atmosphere = atmo, velocity = FlightVelocity)

# nu = atmo.kinematic_viscosity()  # Get kinematic viscosity at that altitude

# xf = XFoil(
#     airfoil=my_airfoil.repanel(n_points_per_side=100),
#     Re=1e6,
#     xfoil_command=r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe"
# )

# alphas = np.linspace(-10, 20, 31)
# AeroAnalysis = xf.alpha(alphas)
# AeroAnalysis = xf.alpha(alphas)

# plt.plot(AeroAnalysis["alpha"], AeroAnalysis["CL"], marker="o")
# plt.xlabel("Angle of Attack (deg)")
# plt.ylabel("Lift Coefficient (CL)")
# plt.title(f"{name}: CL vs Alpha")
# plt.grid(True)
# plt.show()

# polars = Airfoil.generate_polars(
#     alphas=np.linspace(-10, 20, 31),  # Angle of attack range
#     Res=[1e6],                           # Reynolds number (can be a float or array)

# )

# # Plotting CL vs Alpha
# plt.plot(polars["alpha"], polars["CL"], marker="o")
# plt.xlabel("Angle of Attack (deg)")
# plt.ylabel("Lift Coefficient (CL)")
# plt.title(f"{name}: CL vs Alpha (generate_polars)")
# plt.grid(True)
# plt.show()




my_airfoil.generate_polars(
    alphas=alphas,
    Res=np.array([200000]),
    xfoil_kwargs={
        "xfoil_command": r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe"
    }
)


CLs = [my_airfoil.CL_function(alpha, 200000) for alpha in alphas]
CDs = [my_airfoil.CD_function(alpha, 200000) for alpha in alphas]
CMs = [my_airfoil.CM_function(alpha, 200000) for alpha in alphas]
Res = [200000] * len(alphas)

# Save results to CSV
df = pd.DataFrame({
    "alpha": alphas,
    "CL": CLs,
    "CD": CDs,
    "CM": CMs,
    "Re": Res
})



plt.plot(alphas, CLs, marker="o")
plt.xlabel("Angle of Attack (deg)")
plt.ylabel("Lift Coefficient (CL)")
plt.title(f"{name}: CL vs Alpha (generate_polars)")
plt.grid(True)
# plt.show()

# # Draw the airfoil shape
# plt.figure()
# plt.plot(my_airfoil.coordinates[:, 0], my_airfoil.coordinates[:, 1], label="Airfoil Shape")
# plt.axis("equal")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title(f"{name} Airfoil Shape")
# plt.grid(True)
# plt.legend()
# # plt.show()