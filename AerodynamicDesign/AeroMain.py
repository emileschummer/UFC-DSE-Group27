import time
import numpy as np
import aerosandbox as asb
import pandas as pd
import os
from Airfoil import setup_wing_and_airplane, calculate_section_properties_and_reynolds, generate_2d_stall_database, interpolate_stall_data_for_sections, run_vlm_sweep_with_stall_correction, plot_aerodynamic_coefficients
# from Test import setup_wing_and_airplane, calculate_section_properties_and_reynolds, generate_2d_stall_database, interpolate_stall_data_for_sections, run_vlm_sweep_with_stall_correction, plot_aerodynamic_coefficients
from Functions import load_airfoil_dat, no_quarterchord_sweep, wing_geometry_calculator
from AerodynamicForces import load_distribution_halfspan



def run_full_aero( airfoil_dat_path: str = r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\S1223.dat",
    name = "S1223",
    xfoil_path: str = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe",
    operational_velocity: float = 9.16,
    num_spanwise_sections: int = 200,
    vlm_chordwise_resolution = 10,
    delta_alpha_3D_correction: float = 1.0,
    alpha_range2D: np.ndarray = np.linspace(-10, 25, 36),
    alpha_range3D: np.ndarray = np.linspace(-5, 20, 26),
    r_chord: float = 0.91,
    t_chord: float = 0.36,
    r_twist: float = 0.0,
    t_twist: float = 0.0,
    sweep: float = 0.0,
    operational_altitude: float = 0.0,
    Re_numbers: int =2,
    Plot = True,
    csv_path: str = "C:\\Users\\marco\\Documents\\GitHub\\UFC-DSE-Group27\\AerodynamicDesign\\aero.csv") -> dict:

    # Load and build Airfoil
    airfoil_coordinates = load_airfoil_dat(airfoil_dat_path)
    my_airfoil = asb.Airfoil(name, coordinates=airfoil_coordinates)
    # print(my_airfoil.max_thickness())
    # print(my_airfoil.local_thickness())

    t0 = time.perf_counter() # Initialize t0 with the current time
    # 1. Geometry
    wing_geom, airplane_geom = setup_wing_and_airplane(my_airfoil, num_spanwise_sections, r_chord, t_chord, r_twist, t_twist, no_quarterchord_sweep(r_chord, t_chord))
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

    # if Plot:
    #     import matplotlib.pyplot as plt
    #     plt.figure(figsize=(10, 7))
    #     plt.plot(stall_database_df['Re_polar'], stall_database_df['alpha_stall_2D'], marker='o', linestyle='-')
    #     plt.xlabel("Reynolds Number")
    #     plt.ylabel("2D Stall Angle")
    #     # plt.title("2D Stall Angle vs Reynolds Number")
    #     plt.grid(True)
    #     plt.show()

    #     plt.figure(figsize=(10, 7))
    #     plt.plot(stall_database_df['Re_polar'], stall_database_df['Cl_max_2D'], marker='s', linestyle='-')
    #     plt.xlabel("Reynolds Number")
    #     plt.ylabel("Max 2D Lift Coefficient")
    #     # plt.title("Max 2D Lift Coefficient vs Reynolds Number")
    #     plt.grid(True)
    #     plt.show()

    #     plt.figure(figsize=(10, 7))
    #     plt.plot(stall_database_df['Re_polar'], stall_database_df['K_post'], marker='^', linestyle='-')
    #     plt.xlabel("Reynolds Number")
    #     plt.ylabel("Post-Stall Slope")
    #     # plt.title("Post-Stall Slope vs Reynolds Number")
    #     plt.grid(True)
    #     plt.show()

    # 4. Interpolation
    section_data_prepared = interpolate_stall_data_for_sections(section_data_list, stall_database_df, delta_alpha_3D_correction)
    t4 = time.perf_counter()
    print(f"4) Interpolation:     {t4 - t3:.2f} s")

    # 5. VLM sweep + stall correction
    CLs_vlm_original, CDs_vlm_original, CLs_corrected, lift_distribution, CM_vlm = run_vlm_sweep_with_stall_correction(alpha_range3D, airplane_geom, operational_velocity, section_data_prepared, num_spanwise_sections, wing_geom, operational_altitude, vlm_chordwise_resolution)
    t5 = time.perf_counter()
    print(f"5) VLM sweep:         {t5 - t4:.2f} s")
    
    max_idx = max(range(len(CLs_corrected)), key=lambda i: CLs_corrected[i])
    alpha_at_max_cl = alpha_range3D[max_idx]
    # 6. Plot
    plot_aerodynamic_coefficients(alpha_range3D, CLs_vlm_original, CLs_corrected, CDs_vlm_original, Plot)
    t6 = time.perf_counter()
    print(f"6) Plotting:          {t6 - t5:.2f} s")
    print(f"Total runtime:        {t6 - t0:.2f} s")

    for i in range(1,30): 
    #returns distribution at angle of attack where CL is max
        distribution = load_distribution_halfspan(wing_geom, lift_distribution, i, plot = True)

    # if csv_path:
    #     df = pd.DataFrame({
    #         "alpha (deg)": alpha_range3D,
    #         "CL_corrected": CLs_corrected,
    #         "CD_vlm": CDs_vlm_original,
    #         "CM_vlm": CM_vlm
    #     })
    #     print(df.head())  # Debugging: Print the first few rows of the DataFrame
    #     try:
    #         os.makedirs(os.path.dirname(csv_path), exist_ok=True)  # Ensure directory exists
    #         df.to_csv(csv_path, index=False)
    #         print(f"Saved alpha-CL-CD sweep to '{csv_path}'")
    #     except Exception as e:
    #         print(f"Failed to save CSV: {e}")

    return {
        "wing_geom": wing_geom,
        "airplane_geom": airplane_geom,
        "CDs_vlm_original": CDs_vlm_original,
        "CLs_corrected": CLs_corrected,
        "lift_distribution": lift_distribution,
        "alphas" : alpha_range3D,
        "CM_vlm" : CM_vlm,
        "max_distribution" : distribution,
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

    

    



if __name__ == "__main__":
    for i in [r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\S8036 (16%).dat", 
            #   r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\FX 74-Cl5-140 MOD  (smoothed).txt",
            #   r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\CH10 (smoothed).txt",
            #   r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\CLARKY.dat", 
            #   r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\E423.dat", 
            #   r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\NACA4412.dat", 
            #   r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\NACA23012.dat"
            ]:
    # Run with all defaults (just adjust paths if needed):
        velocity_op = 10
        CL = 2
        altitude = 0
        taper_ratio = 0.6
        b = 1.255
        op_point_for_atmo = asb.OperatingPoint(velocity=velocity_op, atmosphere=asb.Atmosphere(altitude=altitude))
        rho = op_point_for_atmo.atmosphere.density()

        # S = 250/(0.5*rho*velocity_op**2*CL)
        S = 0.221
        
        
        # cr = 0.221
        # ct = 0.221
        cr = 2*S/(b*(1 + taper_ratio))

        ct = cr*taper_ratio
        print(S, cr,ct)
        results = run_full_aero(airfoil_dat_path = i, operational_velocity = velocity_op, r_chord = cr, t_chord= ct)
        import matplotlib.pyplot as plt

        plt.figure()
        plt.plot(results["alphas"], results["CM_vlm"], marker="o")
        plt.xlabel("Alpha (deg)")
        plt.ylabel("CM VLM")
        plt.title("CM VLM vs. Angle of Attack")
        plt.grid(True)
        plt.show()