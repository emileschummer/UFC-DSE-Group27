import aerosandbox as asb
import numpy as np
from matplotlib import pyplot as plt
from aerosandbox import Airfoil
from Functions import load_airfoil_dat

# Airfoil name and coordinates
coordinates = load_airfoil_dat(r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\Airfoil.dat")
name = "S1223"

my_airfoil = Airfoil(name=name, coordinates=coordinates)

my_airfoil = my_airfoil.rotate( angle = -0.174533)
print("this", my_airfoil.coordinates)

# Display airfoil information
print(f"Airfoil Name: {my_airfoil.name}")
print(f"Maximum Camber: {my_airfoil.max_camber():.4f}")
print(f"Maximum Thickness: {my_airfoil.max_thickness():.4f}")
print(f"Leading Edge Radius: {my_airfoil.LE_radius():.4f}")
print(f"Trailing Edge Thickness: {my_airfoil.TE_thickness():.4f}")

# Plot airfoil shape and additional information
plt.figure()
plt.plot(my_airfoil.coordinates[:, 0], my_airfoil.coordinates[:, 1], label="Airfoil Shape")
plt.axis("equal")
plt.xlabel("x/c")
plt.ylabel("y/c")
plt.title(f"{my_airfoil.name} Airfoil Shape")
plt.grid(True)
plt.legend()

# Plot camber and thickness distributions
# x_over_c = np.linspace(0, 1, 101)
# plt.figure()
# plt.plot(x_over_c, my_airfoil.local_camber(x_over_c), label="Local Camber")
# plt.plot(x_over_c, my_airfoil.local_thickness(x_over_c), label="Local Thickness")
# plt.xlabel("x/c")
# plt.ylabel("y/c")
# plt.title(f"{my_airfoil.name} Camber and Thickness Distributions")
# plt.grid(True)
# plt.legend()

plt.show()