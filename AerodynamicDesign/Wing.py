import numpy as np
from matplotlib import pyplot as plt
import aerosandbox as asb
from aerosandbox import XFoil, Airfoil, Wing, WingXSec, Airplane, VortexLatticeMethod
from Functions import load_airfoil_dat
from AirfoilAnalysis import my_airfoil  


# Define your wing
wing = Wing(
    name="Demo Wing",
    xsecs=[
        WingXSec(
            xyz_le=[0, 0, 0],
            chord=0.45,
            twist=0,
            airfoil=my_airfoil,  
        ),
        WingXSec(
            xyz_le=[0, 1.5, 0],
            chord=0.25,
            twist=0,
            airfoil=my_airfoil,
        ),
    ],
    symmetric=True,
)
# Subdivide wing into sections and find MAC of each section
num_sections = 10  # You can change this number as needed
wing = wing.subdivide_sections(num_sections)  # assign the subdivided wing!

for i, (xsec_in, xsec_out) in enumerate(zip(wing.xsecs[:-1], wing.xsecs[1:])):
    taper = xsec_out.chord / xsec_in.chord
    mac = (2 / 3) * xsec_in.chord * ((1 + taper + taper**2) / (1 + taper))
    print(f"Section {i+1} Mean Aerodynamic Chord (MAC): {mac:.4f}")


# Create an airplane object (required for VLM)
airplane = Airplane(
    wings=[wing])

print("span", wing.span())
print("area", wing.area())
print("aspect ratio", wing.aspect_ratio())
print("mean geometric chord", wing.mean_geometric_chord())
print("mean aerodynamic chord", wing.mean_aerodynamic_chord())
print("aerodynamic center", wing.aerodynamic_center())
print("volume", wing.volume())

# Sweep alpha and collect CL, CD
alphas = np.linspace(-10, 30, 41)
CLs = []
CDs = []

for alpha in alphas:
    vlm = VortexLatticeMethod(
        airplane=airplane,
        op_point=asb.OperatingPoint(
            velocity=10,
            alpha=alpha,
            beta=0,
            atmosphere=asb.Atmosphere(altitude=0)
        )
    )
    results = vlm.run()
    CLs.append(results["CL"])
    CDs.append(results["CD"])

# Print results
for a, cl, cd in zip(alphas, CLs, CDs):
    print(f"Alpha: {a:5.1f} deg | CL: {cl:7.4f} | CD: {cd:8.5f}")

# Plot CL and CD vs Alpha
plt.figure()
plt.plot(alphas, CLs, label="CL")
plt.xlabel("Angle of Attack (deg)")
plt.ylabel("Coefficient")
plt.legend()
plt.grid(True)
plt.title("CL and CD vs Alpha (VLM with XFOIL polars)")
# plt.show()

# Render the wing in 3D
wing.draw(show=False)
