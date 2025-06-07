import time
import numpy as np
import aerosandbox as asb
from Airfoil import setup_wing_and_airplane, calculate_section_properties_and_reynolds, generate_2d_stall_database, interpolate_stall_data_for_sections, run_vlm_sweep_with_stall_correction, plot_aerodynamic_coefficients
from Functions import load_airfoil_dat
# --- Configuration Constants ---
V_OP = 10  # m/s, operating velocity
NUM_SECTIONS_PER_SIDE = 100  # Number of segments on one side of the symmetric wing
XFOIL_PATH = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe" # Make sure this path is correct
DELTA_ALPHA_FINITE_WING = 2  # degrees, empirical adjustment for 3D stall
ALPHAS_2D_POLAR = np.linspace(-10, 25, 36) # Alpha range for 2D polar generation
ALPHAS_OP_SWEEP = np.linspace(-10, 30, 41) # Alpha range for VLM sweep
coordinates = load_airfoil_dat(r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\Airfoil.dat")
name = "S1223"
my_airfoil = asb.Airfoil(name = name, coordinates = coordinates)
r_chord = 0.45
t_chord = 0.25
r_twist = 0
t_twist = 0
sweep = 0
altitude = 0

# --- Main Script Execution ---
if __name__ == "__main__":
    t0 = time.perf_counter()

    # 1. Setup wing and airplane
    wing_geom, airplane_geom = setup_wing_and_airplane(my_airfoil, NUM_SECTIONS_PER_SIDE, r_chord, t_chord, r_twist, t_twist, sweep)
    t1 = time.perf_counter()
    print(f"1) Wing setup:        {t1 - t0:.2f} s")

    # 2. Calculate section properties and Reynolds numbers
    section_data_list = calculate_section_properties_and_reynolds(wing_geom, V_OP, altitude)
    t2 = time.perf_counter()
    print(f"2) Section calc:      {t2 - t1:.2f} s")

    # 3. Generate 2D stall database from XFoil polars
    stall_database_df = generate_2d_stall_database(
        my_airfoil, section_data_list, ALPHAS_2D_POLAR, XFOIL_PATH
    )
    t3 = time.perf_counter()
    print(f"3) 2D stall database: {t3 - t2:.2f} s")

    # 4. Interpolate stall data for each wing section
    section_data_prepared = interpolate_stall_data_for_sections(
        section_data_list, stall_database_df, DELTA_ALPHA_FINITE_WING
    )
    t4 = time.perf_counter()
    print(f"4) Interpolation:     {t4 - t3:.2f} s")

    # 5. Perform VLM alpha sweep with stall correction
    CLs_vlm_original, CDs_vlm_original, CLs_corrected = run_vlm_sweep_with_stall_correction(
        ALPHAS_OP_SWEEP, airplane_geom, V_OP,
        section_data_prepared, NUM_SECTIONS_PER_SIDE, wing_geom, altitude
    )
    t5 = time.perf_counter()
    print(f"5) VLM sweep:         {t5 - t4:.2f} s")

    # 6. Plot results
    plot_aerodynamic_coefficients(
        ALPHAS_OP_SWEEP, CLs_vlm_original, CLs_corrected, CDs_vlm_original
    )
    t6 = time.perf_counter()
    print(f"6) Plotting:          {t6 - t5:.2f} s")

    print(f"Total runtime:        {t6 - t0:.2f} s")

    # Optional: Render the wing
    # wing_geom.draw(show=True)
