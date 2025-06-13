from AeroMain import run_full_aero
import numpy as np
from matplotlib import pyplot as plt
import aerosandbox as asb
import pandas as pd
# Removed setup_wing_and_airplane from this import, assuming it's no longer needed from Airfoil.py
from Airfoil import calculate_section_properties_and_reynolds, generate_2d_stall_database, interpolate_stall_data_for_sections, run_vlm_sweep_with_stall_correction, plot_aerodynamic_coefficients
from Functions import load_airfoil_dat
from AerodynamicForces import load_distribution_halfspan

# Operating parameters
airfoil_dat_path = r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\Airfoil.dat"
name = "S1223"
xfoil_path = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe"
operational_velocity = 10.0
num_spanwise_sections = 200 # For the main wing
vlm_chordwise_resolution = 6
delta_alpha_3D_correction = 1.0
alpha_range2D = np.linspace(-10, 25, 36)
alpha_range3D = np.linspace(-10, 30, 41)
r_chord = 0.91 # Main wing root chord
t_chord = 0.36 # Main wing tip chord
r_twist = 0.0  # Main wing root twist
t_twist = 0.0  # Main wing tip twist
sweep = 0.0    # Main wing sweep
operational_altitude = 0.0
Re_numbers = 2
Plot = True
csv_path = r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\aero.csv"

# Load and build Airfoil for the main wing
airfoil_coordinates = load_airfoil_dat(airfoil_dat_path)
my_airfoil = asb.Airfoil(name=name, coordinates=airfoil_coordinates)

# 1. Geometry
# Define and create the main wing
main_wing_half_span = 1.575  # Half-span for the main wing, as previously in setup_wing_and_airplane

main_wing = asb.Wing(
    name="MainWing",
    xsecs=[
        asb.WingXSec(
            xyz_le=[0, 0, 0],  # Root leading edge
            chord=r_chord,
            twist=r_twist,
            airfoil=my_airfoil,
        ),
        asb.WingXSec(
            xyz_le=[sweep, main_wing_half_span, 0],  # Tip leading edge
            chord=t_chord,
            twist=t_twist,
            airfoil=my_airfoil,
        ),
    ],
    symmetric=True,
)
main_wing = main_wing.subdivide_sections(num_spanwise_sections)

wing_geom = main_wing # Assign main_wing to wing_geom, similar to what setup_wing_and_airplane returned

# Initialize the airplane object with the main wing
airplane_geom = asb.Airplane(
    name="MyAircraft",
    wings=[main_wing]
    # Optionally, set reference values if needed, e.g.:
    # s_ref=main_wing.area(),
    # c_ref=main_wing.mean_aerodynamic_chord(),
    # b_ref=main_wing.span()
)

# Create a horizontal stabilizer wing
hstab_airfoil = asb.Airfoil("naca0012")
hstab = asb.Wing(
    name="Horizontal Stabilizer",
    xsecs=[
        asb.WingXSec(
            xyz_le=[0, 0, 0], # Define hstab root LE relative to airplane origin
            chord=1.0,
            airfoil=hstab_airfoil,
            twist=-2.0,
            control_surfaces=[
                asb.ControlSurface(
                    name="elevator",
                    symmetric=True,
                    hinge_point=0.75,
                    deflection=0.0
                )
            ]
        ),
        asb.WingXSec(
            xyz_le=[1, 0, 0], # Define hstab tip LE relative to airplane origin
            chord=0.8,
            airfoil=hstab_airfoil,
            twist=-2.0
        ),
    ],
    symmetric=True
)
airplane_geom.wings.append(hstab) # Add hstab to the airplane

# Create a fuselage
fus = asb.Fuselage(
    name="Fuselage",
    xsecs=[
        asb.FuselageXSec(xyz_c=[0, 0, 0], radius=0),
        asb.FuselageXSec(xyz_c=[0.2, 0, 0], radius=0.1),
        asb.FuselageXSec(xyz_c=[0.4, 0, 0], radius=0.2),
        asb.FuselageXSec(xyz_c=[0.6, 0, 0], radius=0.2),
        asb.FuselageXSec(xyz_c=[0.8, 0, 0], radius=0.1),
        asb.FuselageXSec(xyz_c=[1, 0, 0], radius=0)
    ]
)
airplane_geom.fuselages.append(fus) # Add fuselage to the airplane

# Create a vertical stabilizer (tail)
vstab_airfoil = asb.Airfoil("naca0012")
vstab = asb.Wing(
    name="Vertical Stabilizer",
    xsecs=[
        asb.WingXSec(
            xyz_le=[0, 0, 0], # Define vstab root LE relative to airplane origin
            chord=0.8,
            airfoil=vstab_airfoil,
            twist=0.0,
            control_surfaces=[
                asb.ControlSurface(
                    name="rudder",
                    symmetric=False,
                    hinge_point=0.75,
                    deflection=0.0
                )
            ]
        ),
        asb.WingXSec(
            xyz_le=[0, 1.0, 0], # Define vstab tip LE relative to airplane origin
            chord=0.6,
            airfoil=vstab_airfoil,
            twist=0.0
        )
    ],
    symmetric=False # Typically, a single vertical tail is not symmetric in the airplane definition
)
airplane_geom.wings.append(vstab) # Add vstab to the airplane

# %% VLM Cm and Cm_alpha Sweep
# Define a range of angles of attack (in degrees)
alpha_range = np.linspace(-5, 15, 21)
Cm_values = []

# Run VLM for each angle
for alpha in alpha_range:
    op_point = asb.OperatingPoint(
        velocity=operational_velocity, # Using the defined operational_velocity
        alpha=alpha,
        beta=0,
        atmosphere=asb.Atmosphere(altitude=operational_altitude) # Using defined operational_altitude
    )
    vlm = asb.VortexLatticeMethod(
        airplane=airplane_geom,
        op_point=op_point,
        spanwise_resolution=10, # Increased resolution for better VLM results
        chordwise_resolution=10 # Increased resolution for better VLM results
    )
    vlm_results = vlm.run()
    Cm_values.append(vlm_results["Cm"])

# Compute Cm_alpha using finite differences
Cm_alpha = np.gradient(Cm_values, alpha_range)

# Plot the Cm vs. Angle of Attack graph
plt.figure()
plt.plot(alpha_range, Cm_values, marker='o', label="Cm")
plt.xlabel("Angle of Attack (deg)")
plt.ylabel("Pitching Moment Coefficient (Cm)")
plt.title("Cm vs. Angle of Attack")
plt.grid(True)
plt.legend()
plt.show()

# Plot the Cm_alpha vs. Angle of Attack graph
plt.figure()
plt.plot(alpha_range, Cm_alpha, marker='s', color='r', label="Cm_alpha")
plt.xlabel("Angle of Attack (deg)")
plt.ylabel("dCm/dalpha (per deg)")
plt.title("Cm_alpha vs. Angle of Attack")
plt.grid(True)
plt.legend()
plt.show()

# Print the numerical Cm and Cm_alpha values
print("Cm vs. Angle of Attack:")
for alpha, Cm, dCm in zip(alpha_range, Cm_values, Cm_alpha):
    print(f"Alpha: {alpha:6.2f} deg, Cm: {Cm:8.4f}, Cm_alpha: {dCm:8.4f} per deg")