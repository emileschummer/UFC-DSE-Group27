from AeroMain import run_full_aero
import numpy as np
from matplotlib import pyplot as plt
import aerosandbox as asb
import pandas as pd
from Functions import load_airfoil_dat, no_quarterchord_sweep

# Operating parameters
airfoil_dat_path = r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\S1223.dat"
name = "S1223"
xfoil_path = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe" # Kept as it might be used if XFOIL functionality is added
num_spanwise_sections = 200 # For the main wing geometry definition
num_spanwise_sections_h = 50

# Load and build Airfoil for the main wing
airfoil_coordinates = load_airfoil_dat(airfoil_dat_path)
my_airfoil = asb.Airfoil(name=name, coordinates=airfoil_coordinates)

# 1. Geometry Definition
# Define Main Wing
main_wing_half_span = 1.575
r_chord = 0.91 # Main wing root chord
t_chord = 0.36 # Main wing tip chord
r_twist = 0.0  # Main wing root twist
t_twist = 0.0  # Main wing tip twist
sweep = no_quarterchord_sweep(r_chord, t_chord)    # Main wing sweep

main_wing = asb.Wing(
    name="MainWing",
    xsecs=[
        asb.WingXSec(
            xyz_le=[0, 0, 0],  # Root leading edge at aircraft origin
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
).subdivide_sections(num_spanwise_sections) # Subdivide for detailed geometry for VLM

# Define Fuselage
fuselage_length = 0.6
fuselage_max_radius = 0.1
fuselage_x_start = 0 
fuselage = asb.Fuselage(
    name="Fuselage",
    xsecs=[
        asb.FuselageXSec(xyz_c=[fuselage_x_start, 0, 0], radius=0),
        asb.FuselageXSec(xyz_c=[fuselage_x_start + 0.1 * fuselage_length, 0, 0], radius=fuselage_max_radius * 0.5),
        asb.FuselageXSec(xyz_c=[fuselage_x_start + 0.4 * fuselage_length, 0, 0], radius=fuselage_max_radius),
        asb.FuselageXSec(xyz_c=[fuselage_x_start + 0.7 * fuselage_length, 0, 0], radius=fuselage_max_radius * 0.8),
        asb.FuselageXSec(xyz_c=[fuselage_x_start + fuselage_length, 0, 0], radius=0),
    ]
)

# Define Horizontal Stabilizer
h_stab_airfoil = asb.Airfoil("naca0012")
h_stab_x_le_root = 3 # Positioned aft of the main wing
h_stab_half_span = 1
h_stab_root_chord = 0.3
h_stab_tip_chord = 0.3
h_stab_twist = -3 # Typical for stability
h_stab_sweep = 0 # Slight sweep for the H-stab

h_stab = asb.Wing(
    name="HorizontalStabilizer",
    xsecs=[
        asb.WingXSec(
            xyz_le=[h_stab_x_le_root, 0, 0.05],  # Slightly above fuselage centerline
            chord=h_stab_root_chord,
            twist=h_stab_twist,
            airfoil=h_stab_airfoil,
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
            xyz_le=[
                h_stab_x_le_root + h_stab_half_span * np.tan(np.deg2rad(h_stab_sweep)),
                h_stab_half_span,
                0.05
            ],
            chord=h_stab_tip_chord,
            twist=h_stab_twist,
            airfoil=h_stab_airfoil,
        ),
    ],
    symmetric=True,
).subdivide_sections(num_spanwise_sections_h)


cg_location = [0.33 * r_chord, 0, 0]

# Assemble the Airplane
airplane_geom = asb.Airplane(
    name="CompleteAircraft",
    xyz_ref=cg_location,
    wings=[main_wing, h_stab],
    fuselages=[fuselage],
    s_ref=main_wing.area(), # Explicitly set reference values
    c_ref=main_wing.mean_aerodynamic_chord(),
    b_ref=main_wing.span()
)

# Optional: Draw the airplane to verify geometry
# airplane_geom.draw_three_view()
airplane_geom.draw() # This will render the aircraft


# Removed redundant VLM Cm and Cm_alpha Sweep block for the full aircraft.
# The analysis is now handled by the run_full_plane_analysis_with_corrections
# function and the subsequent plotting in the if __name__ == "__main__": block.

def run_full_plane_analysis( # Renamed and simplified parameters
    full_airplane: asb.Airplane,
    alpha_range: list, # Changed from alpha_range3D
    operational_velocity: float = 10.0,
    operational_altitude: float = 0.0,
    vlm_spanwise_resolution: int = 1, # Added for clarity, was hardcoded
    vlm_chordwise_resolution: int = 8,
    draw_vlm_at_alpha: float = None
):
    """
    Run the full airplane VLM analysis.
    Parameters:
        full_airplane: The complete airplane object
        alpha_range: Angle of attack range for analysis
        operational_velocity: Flight velocity
        operational_altitude: Flight altitude
        vlm_spanwise_resolution: VLM spanwise resolution per wing section
        vlm_chordwise_resolution: VLM chordwise resolution
        draw_vlm_at_alpha: Specific angle of attack to draw VLM results
    Returns:
        results_summary: Summary of results including CL, CD, Cm, and Cm_alpha
    """
    # Initialize results storage
    results_summary = {
        "alpha": [],
        "CL": [],
        "CD": [],
        "Cm": [],
        "Cm_alpha": [] # Cm_alpha will be calculated per degree
    }
    
    # Iterate over the alpha range
    for alpha_val in alpha_range:
        op_point = asb.OperatingPoint(
            velocity=operational_velocity, alpha=alpha_val, beta=0, 
            atmosphere=asb.Atmosphere(altitude=operational_altitude)
        )
        
        vlm_instance = asb.VortexLatticeMethod(
            airplane=full_airplane,
            op_point=op_point,
            spanwise_resolution=vlm_spanwise_resolution, 
            chordwise_resolution=vlm_chordwise_resolution 
        )
        vlm_results_plane = vlm_instance.run()

        # Draw VLM results if the current alpha matches the specified one
        if draw_vlm_at_alpha is not None and np.isclose(alpha_val, draw_vlm_at_alpha):
            print(f"\nDrawing VLM analysis for alpha = {alpha_val:.2f} deg...")
            vlm_instance.draw(
                show=True,
                draw_streamlines=True,
            )
            print("VLM drawing displayed. Close the window to continue analysis.")

        CL_vlm_plane_total = vlm_results_plane.get("CL", np.nan)
        CD_vlm_plane_total = vlm_results_plane.get("CD", np.nan)
        Cm_vlm_plane_total = vlm_results_plane.get("Cm", np.nan)
        
        results_summary["alpha"].append(alpha_val)
        results_summary["CL"].append(CL_vlm_plane_total)
        results_summary["CD"].append(CD_vlm_plane_total)
        results_summary["Cm"].append(Cm_vlm_plane_total)
        
        print(f"Alpha: {alpha_val:6.2f} deg, CL: {CL_vlm_plane_total:.4f}, CD: {CD_vlm_plane_total:.4f}, Cm: {Cm_vlm_plane_total:.4f}")

    # Compute Cm_alpha using finite differences (numerical derivative over degrees)
    if len(results_summary["alpha"]) > 1:
        # Ensure alphas are sorted for correct gradient calculation if not already
        sorted_indices = np.argsort(results_summary["alpha"])
        sorted_alphas = np.array(results_summary["alpha"])[sorted_indices]
        sorted_Cm = np.array(results_summary["Cm"])[sorted_indices]
        
        cm_alpha_values_rad = np.gradient(sorted_Cm, np.deg2rad(sorted_alphas)) # dCm/dalpha_rad
        cm_alpha_values_deg = np.gradient(sorted_Cm, sorted_alphas) # dCm/dalpha_deg

        # Store Cm_alpha (per degree) in the original order
        # Create a temporary mapping from sorted alpha back to original index if needed,
        # or just fill based on sorted_alphas if results_summary["alpha"] was already sorted.
        # Assuming alpha_range was monotonic, so results_summary["alpha"] is also.
        results_summary["Cm_alpha"] = list(cm_alpha_values_deg)
    elif len(results_summary["alpha"]) == 1:
         results_summary["Cm_alpha"].append(np.nan) # Cannot compute gradient for a single point
    # else Cm_alpha remains empty

    return results_summary

if __name__ == "__main__":
    # 1. Geometry and Airfoil Setup is done above

    # 2. Define analysis parameters
    analysis_alphas = np.linspace(-5, 15, 21) # Define AoA range for the analysis
    analysis_velocity = 10.0
    analysis_altitude = 0.0
    analysis_vlm_span_res = 1 # Spanwise panels per pre-defined wing section
    analysis_vlm_chord_res = 6
    analysis_draw_vlm_at_alpha = 10.0 # Example: Draw VLM when alpha is 5.0 degrees

    # 3. Run the full analysis
    print("Starting Full Plane Analysis...")
    analysis_results = run_full_plane_analysis(
        full_airplane=airplane_geom, # Use the defined airplane_geom
        alpha_range=analysis_alphas,
        operational_velocity=analysis_velocity, 
        operational_altitude=analysis_altitude,
        vlm_spanwise_resolution=analysis_vlm_span_res,
        vlm_chordwise_resolution=analysis_vlm_chord_res,
        draw_vlm_at_alpha=analysis_draw_vlm_at_alpha
    )

    # 4. Plot aerodynamic coefficients
    plt.figure(figsize=(10, 8))
    plt.suptitle("Full Aircraft Aerodynamic Coefficients (VLM)", fontsize=16)

    plt.subplot(2, 2, 1)
    plt.plot(analysis_results["alpha"], analysis_results["CL"], label="CL")
    plt.xlabel("Angle of Attack (deg)")
    plt.ylabel("Lift Coefficient (CL)")
    plt.title("CL vs. Angle of Attack")
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(analysis_results["alpha"], analysis_results["CD"], label="CD", color="red")
    plt.xlabel("Angle of Attack (deg)")
    plt.ylabel("Drag Coefficient (CD)")
    plt.title("CD vs. Angle of Attack")
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(analysis_results["alpha"], analysis_results["Cm"], label="Cm", color="green")
    plt.xlabel("Angle of Attack (deg)")
    plt.ylabel("Pitching Moment Coefficient (Cm)")
    plt.title("Cm vs. Angle of Attack")
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(analysis_results["alpha"], analysis_results["Cm_alpha"], label="Cm_alpha", color="orange")
    plt.xlabel("Angle of Attack (deg)")
    plt.ylabel("dCm/dalpha (per deg)")
    plt.title("Cm_alpha vs. Angle of Attack")
    plt.grid(True)
    plt.legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust layout to make space for suptitle
    plt.show()

    # Print numerical results
    print("\nFull Aircraft Analysis Results:")
    print("Alpha (deg) |    CL    |    CD    |    Cm    | Cm_alpha (1/deg)")
    print("-----------------------------------------------------------------")
    for i in range(len(analysis_results["alpha"])):
        alpha = analysis_results["alpha"][i]
        cl = analysis_results["CL"][i]
        cd = analysis_results["CD"][i]
        cm = analysis_results["Cm"][i]
        cm_alpha = analysis_results["Cm_alpha"][i] if i < len(analysis_results["Cm_alpha"]) else np.nan
        print(f"{alpha:11.2f} | {cl:8.4f} | {cd:8.4f} | {cm:8.4f} | {cm_alpha:8.4f}")