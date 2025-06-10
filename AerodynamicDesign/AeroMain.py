# import time
import numpy as np
import aerosandbox as asb
import pandas as pd
import os
from Airfoil import setup_wing_and_airplane, calculate_section_properties_and_reynolds, generate_2d_stall_database, interpolate_stall_data_for_sections, run_vlm_sweep_with_stall_correction, plot_aerodynamic_coefficients
from Functions import load_airfoil_dat
from AerodynamicForces import load_distribution_halfspan



def run_full_aero( airfoil_dat_path: str = r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\Airfoil.dat",
    name = "S1223",
    xfoil_path: str = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe",
    velocity_op: float = 10.0,
    NUM_SECTIONS_PER_SIDE: int = 200,
    DELTA_ALPHA_FINITE_WING: float = 2.0,
    ALPHAS_2D_POLAR: np.ndarray = np.linspace(-10, 25, 36),
    ALPHAS_OP_SWEEP: np.ndarray = np.linspace(-10, 30, 41),
    r_chord: float = 0.45,
    t_chord: float = 0.25,
    r_twist: float = 0.0,
    t_twist: float = 0.0,
    sweep: float = 0.0,
    altitude: float = 0.0,
    ReNumbers: int = 2,
    Plot = False,
    csv_path: str = "C:\\Users\\marco\\Documents\\GitHub\\UFC-DSE-Group27\\AerodynamicDesign\\aero.csv") -> dict:

    # Load and build Airfoil
    coords = load_airfoil_dat(airfoil_dat_path)
    my_airfoil = asb.Airfoil(name, coordinates=coords)

    # 1. Geometry
    wing_geom, airplane_geom = setup_wing_and_airplane(my_airfoil, NUM_SECTIONS_PER_SIDE, r_chord, t_chord, r_twist, t_twist, sweep)
    # t1 = time.perf_counter()
    # print(f"1) Wing setup:        {t1 - t0:.2f} s")

    # 2. Section and Reynolds
    section_data_list = calculate_section_properties_and_reynolds(wing_geom, velocity_op, altitude)
    # t2 = time.perf_counter()
    # print(f"2) Section calc:      {t2 - t1:.2f} s")

    # 3. 2D stall database
    stall_database_df = generate_2d_stall_database(my_airfoil, section_data_list, ALPHAS_2D_POLAR, xfoil_path, ReNumbers)
    # t3 = time.perf_counter()
    # print(f"3) 2D stall database: {t3 - t2:.2f} s")

    # 4. Interpolation
    section_data_prepared = interpolate_stall_data_for_sections(section_data_list, stall_database_df, DELTA_ALPHA_FINITE_WING)
    # t4 = time.perf_counter()
    # print(f"4) Interpolation:     {t4 - t3:.2f} s")

    # 5. VLM sweep + stall correction
    CLs_vlm_original, CDs_vlm_original, CLs_corrected, lift_distribution, = run_vlm_sweep_with_stall_correction(ALPHAS_OP_SWEEP, airplane_geom, velocity_op, section_data_prepared, NUM_SECTIONS_PER_SIDE, wing_geom, altitude)
    # t5 = time.perf_counter()
    # print(f"5) VLM sweep:         {t5 - t4:.2f} s")

    # 6. Plot
    plot_aerodynamic_coefficients(ALPHAS_OP_SWEEP, CLs_vlm_original, CLs_corrected, CDs_vlm_original, Plot)
    # t6 = time.perf_counter()
    # print(f"6) Plotting:          {t6 - t5:.2f} s")
    # print(f"Total runtime:        {t6 - t0:.2f} s")

    if csv_path:
        df = pd.DataFrame({
            "alpha (deg)": ALPHAS_OP_SWEEP,
            "CL_corrected": CLs_corrected,
            "CD_vlm": CDs_vlm_original,
        })
        print(df.head())  # Debugging: Print the first few rows of the DataFrame
        try:
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)  # Ensure directory exists
            df.to_csv(csv_path, index=False)
            print(f"Saved α–CL–CD sweep to '{csv_path}'")
        except Exception as e:
            print(f"Failed to save CSV: {e}")

    return {
        "wing_geom": wing_geom,
        "airplane_geom": airplane_geom,
        "CDs_vlm_original": CDs_vlm_original,
        "CLs_corrected": CLs_corrected,
        "lift_distribution": lift_distribution,
        "alphas" : ALPHAS_OP_SWEEP
        # "timings": {
        #     "wing_setup": t1 - t0,
        #     "section_calc": t2 - t1,
        #     "stall_db": t3 - t2,
        #     "interpolation": t4 - t3,
        #     "vlm_sweep": t5 - t4,
        #     "plotting": t6 - t5,
        #     "total": t6 - t0,
        # },
    }


# # --- Main Script Execution ---
# if __name__ == "__main__":
#     t0 = time.perf_counter()

#     # 1. Setup wing and airplane
#     wing_geom, airplane_geom = setup_wing_and_airplane(my_airfoil, NUM_SECTIONS_PER_SIDE, r_chord, t_chord, r_twist, t_twist, sweep)
#     t1 = time.perf_counter()
#     print(f"1) Wing setup:        {t1 - t0:.2f} s")

#     # 2. Calculate section properties and Reynolds numbers
#     section_data_list = calculate_section_properties_and_reynolds(wing_geom, velocity_op, altitude)
#     t2 = time.perf_counter()
#     print(f"2) Section calc:      {t2 - t1:.2f} s")

#     # 3. Generate 2D stall database from XFoil polars
#     stall_database_df = generate_2d_stall_database(
#         my_airfoil, section_data_list, ALPHAS_2D_POLAR, XFOIL_PATH, ReNumbers
#     )
#     t3 = time.perf_counter()
#     print(f"3) 2D stall database: {t3 - t2:.2f} s")

#     # 4. Interpolate stall data for each wing section
#     section_data_prepared = interpolate_stall_data_for_sections(
#         section_data_list, stall_database_df, DELTA_ALPHA_FINITE_WING
#     )
#     t4 = time.perf_counter()
#     print(f"4) Interpolation:     {t4 - t3:.2f} s")

#     # 5. Perform VLM alpha sweep with stall correction
#     CLs_vlm_original, CDs_vlm_original, CLs_corrected, result_collection, lift_distribution = run_vlm_sweep_with_stall_correction(
#         ALPHAS_OP_SWEEP, airplane_geom, velocity_op,
#         section_data_prepared, NUM_SECTIONS_PER_SIDE, wing_geom, altitude
#     )
#     t5 = time.perf_counter()
#     print(f"5) VLM sweep:         {t5 - t4:.2f} s")

#     # 6. Plot results
#     plot_aerodynamic_coefficients(
#         ALPHAS_OP_SWEEP, CLs_vlm_original, CLs_corrected, CDs_vlm_original
#     )
#     t6 = time.perf_counter()
#     print(f"6) Plotting:          {t6 - t5:.2f} s")

#     print(f"Total runtime:        {t6 - t0:.2f} s")

#     # Optional: Render the wing
#     # wing_geom.draw(show=True)

#     distribution = load_distribution_halfspan(wing_geom, lift_distribution, 20, half_span=1.5, plot = False)

    



if __name__ == "__main__":
    # Run with all defaults (just adjust paths if needed):
    results = run_full_aero()
    # ‘results’ now holds everything if you want to inspect or post‐process further