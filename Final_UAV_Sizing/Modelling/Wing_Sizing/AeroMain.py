import time
import numpy as np
import aerosandbox as asb
import pandas as pd
import os
from Modelling.Wing_Sizing.Airfoil import setup_wing_and_airplane, calculate_section_properties_and_reynolds, generate_2d_stall_database, interpolate_stall_data_for_sections, run_vlm_sweep_with_stall_correction, plot_aerodynamic_coefficients
# from Test import setup_wing_and_airplane, calculate_section_properties_and_reynolds, generate_2d_stall_database, interpolate_stall_data_for_sections, run_vlm_sweep_with_stall_correction, plot_aerodynamic_coefficients
from Modelling.Wing_Sizing.Functions import load_airfoil_dat
from Modelling.Wing_Sizing.AerodynamicForces import load_distribution_halfspan



def run_full_aero( airfoil_dat_path: str = r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\Airfoil.dat",
    name = "S1223",
    xfoil_path: str = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe",
    operational_velocity: float = 10.0,
    num_spanwise_sections: int = 200,
    vlm_chordwise_resolution = 6,
    delta_alpha_3D_correction: float = 1.0,
    alpha_range2D: np.ndarray = np.linspace(-10, 25, 36),
    alpha_range3D: np.ndarray = np.linspace(-10, 30, 41),
    r_chord: float = 0.35,
    t_chord: float = 0.35,
    r_twist: float = 0.0,
    t_twist: float = 0.0,
    sweep: float = 0.0,
    operational_altitude: float = 0.0,
    Re_numbers: int = 8,
    Plot = True,
    csv_path: str = "C:\\Users\\marco\\Documents\\GitHub\\UFC-DSE-Group27\\AerodynamicDesign\\aero.csv",
    output_folder: str = "Final_UAV_Sizing/Output") -> dict:

    # Load and build Airfoil
    airfoil_coordinates = load_airfoil_dat(airfoil_dat_path)
    my_airfoil = asb.Airfoil(name, coordinates=airfoil_coordinates)
    t0 = time.perf_counter() # Initialize t0 with the current time
    # 1. Geometry
    wing_geom, airplane_geom = setup_wing_and_airplane(my_airfoil, num_spanwise_sections, r_chord, t_chord, r_twist, t_twist, sweep)
    t1 = time.perf_counter()
    print(f"1) Wing setup:        {t1 - t0:.2f} s")

    # 2. Section and Reynolds
    section_data_list = calculate_section_properties_and_reynolds(wing_geom, operational_velocity, operational_altitude)
    t2 = time.perf_counter()
    print(f"2) Section calc:      {t2 - t1:.2f} s")

    # 3. 2D stall database
    stall_database_df = generate_2d_stall_database(my_airfoil, section_data_list, alpha_range2D, xfoil_path, Re_numbers)
    t3 = time.perf_counter()
    print(f"3) 2D stall database: {t3 - t2:.2f} s")

    # 4. Interpolation
    section_data_prepared = interpolate_stall_data_for_sections(section_data_list, stall_database_df, delta_alpha_3D_correction)
    t4 = time.perf_counter()
    print(f"4) Interpolation:     {t4 - t3:.2f} s")

    # 5. VLM sweep + stall correction
    CLs_vlm_original, CDs_vlm_original, CLs_corrected, lift_distribution, Cm = run_vlm_sweep_with_stall_correction(alpha_range3D, airplane_geom, operational_velocity, section_data_prepared, num_spanwise_sections, wing_geom, operational_altitude, vlm_chordwise_resolution)
    t5 = time.perf_counter()
    print(f"5) VLM sweep:         {t5 - t4:.2f} s")

    # 6. Plot
    output_folder = os.path.join(output_folder, "Wing_Sizing")
    os.makedirs(output_folder, exist_ok=True)

    plot_aerodynamic_coefficients(alpha_range3D, CLs_vlm_original, CLs_corrected, CDs_vlm_original, Plot,output_folder)
    t6 = time.perf_counter()
    print(f"6) Plotting:          {t6 - t5:.2f} s")
    print(f"Total runtime:        {t6 - t0:.2f} s")

    # distribution = load_distribution_halfspan(wing_geom, lift_distribution, 10, half_span=1.5, plot = True)
    # Always save output to Final_UAV_Sizing/Output regardless of csv_path argument
    # Always save output to Final_UAV_Sizing/Output, using the filename from csv_path
    df = pd.DataFrame({
        "alpha (deg)": alpha_range3D,
        "CL_corrected": CLs_corrected,
        "CD_vlm": CDs_vlm_original,
        "Cm_vlm": Cm
    })
    try:
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
        "alphas" : alpha_range3D
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
#     wing_geom, airplane_geom = setup_wing_and_airplane(my_airfoil, num_spanwise_sections, r_chord, t_chord, r_twist, t_twist, sweep)
#     t1 = time.perf_counter()
#     print(f"1) Wing setup:        {t1 - t0:.2f} s")

#     # 2. Calculate section properties and Reynolds numbers
#     section_data_list = calculate_section_properties_and_reynolds(wing_geom, operational_velocity, operational_altitude)
#     t2 = time.perf_counter()
#     print(f"2) Section calc:      {t2 - t1:.2f} s")

#     # 3. Generate 2D stall database from XFoil polars
#     stall_database_df = generate_2d_stall_database(
#         my_airfoil, section_data_list, alpha_range2D, XFOIL_PATH, Re_numbers
#     )
#     t3 = time.perf_counter()
#     print(f"3) 2D stall database: {t3 - t2:.2f} s")

#     # 4. Interpolate stall data for each wing section
#     section_data_prepared = interpolate_stall_data_for_sections(
#         section_data_list, stall_database_df, delta_alpha_3D_correction
#     )
#     t4 = time.perf_counter()
#     print(f"4) Interpolation:     {t4 - t3:.2f} s")

#     # 5. Perform VLM alpha sweep with stall correction
#     CLs_vlm_original, CDs_vlm_original, CLs_corrected, result_collection, lift_distribution = run_vlm_sweep_with_stall_correction(
#         alpha_range3D, airplane_geom, operational_velocity,
#         section_data_prepared, num_spanwise_sections, wing_geom, operational_altitude
#     )
#     t5 = time.perf_counter()
#     print(f"5) VLM sweep:         {t5 - t4:.2f} s")

#     # 6. Plot results
#     plot_aerodynamic_coefficients(
#         alpha_range3D, CLs_vlm_original, CLs_corrected, CDs_vlm_original
#     )
#     t6 = time.perf_counter()
#     print(f"6) Plotting:          {t6 - t5:.2f} s")

#     print(f"Total runtime:        {t6 - t0:.2f} s")

#     # Optional: Render the wing
#     # wing_geom.draw(show=True)