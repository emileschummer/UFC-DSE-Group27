import aerosandbox as asb
import numpy as np 
from matplotlib import pyplot as plt
from aerosandbox import XFoil, Airfoil
from Functions import load_airfoil_dat

# Airfoli name and coordinates, 
# Place dat file as argument
coordinates = load_airfoil_dat(r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\Airfoil.dat")
name = "S1223"

my_airfoil = Airfoil(name = name, coordinates = coordinates)

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
    alphas=np.linspace(-10, 20, 31),
    Res=np.array([1e6]),
    xfoil_kwargs={
        "xfoil_command": r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe"
    }
)

alphas = np.linspace(-10, 20, 31)
CLs = [my_airfoil.CL_function(alpha, 1e6) for alpha in alphas]

plt.plot(alphas, CLs, marker="o")
plt.xlabel("Angle of Attack (deg)")
plt.ylabel("Lift Coefficient (CL)")
plt.title(f"{name}: CL vs Alpha (generate_polars)")
plt.grid(True)
plt.show()