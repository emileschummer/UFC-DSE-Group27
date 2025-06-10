import numpy as np
from matplotlib import pyplot as plt
import aerosandbox as asb
import pandas as pd
# --- Helper Functions ---

def setup_wing_and_airplane(base_airfoil, num_spanwise_sections, r_chord, t_chord, r_twist, t_twist, sweep):
    """Define wing geometry and create an airplane object."""
    wing = asb.Wing(
        name="Wing",
        xsecs=[
            asb.WingXSec(
                xyz_le=[0, 0, 0], chord=r_chord, twist=r_twist, airfoil=base_airfoil,
            ),
            asb.WingXSec(
                xyz_le=[sweep, 1.5, 0], chord=t_chord, twist=t_twist, airfoil=base_airfoil,
            ),
        ],
        symmetric=True,
    )
    wing = wing.subdivide_sections(num_spanwise_sections)
    airplane = asb.Airplane(wings=[wing])
    # print(f"Wing Setup: Span={wing.span():.2f}m, Area={wing.area():.2f}m^2, AR={wing.aspect_ratio():.2f}")
    return wing, airplane

def calculate_section_properties_and_reynolds(wing_obj, velocity_op, altitude):
    """Calculate geometric properties and Reynolds numbers for each wing section."""
    section_data_list = []
    #flow properties
    op_point_for_atmo = asb.OperatingPoint(velocity=velocity_op, atmosphere=asb.Atmosphere(altitude=altitude))
    rho = op_point_for_atmo.atmosphere.density()
    mu = op_point_for_atmo.atmosphere.dynamic_viscosity()
    nu = mu / rho

    for i, (xsec_in, xsec_out) in enumerate(zip(wing_obj.xsecs[:-1], wing_obj.xsecs[1:])):
        chord_in = xsec_in.chord
        chord_out = xsec_out.chord
        y_in = xsec_in.xyz_le[1]
        y_out = xsec_out.xyz_le[1]

        c_j = (chord_in + chord_out) / 2 #take mid point chords and distances because vlm solves on N panels 
        y_j_mid = (y_in + y_out) / 2
        delta_y_j = y_out - y_in
        area_j = c_j * delta_y_j
        Re_j = (velocity_op * c_j) / nu

        section_data_list.append({
            'id': i, 'y_mid': y_j_mid, 'chord': c_j, 'span_segment': delta_y_j,
            'area': area_j, 'xsec_in_xyz_le_y': y_in, 'xsec_out_xyz_le_y': y_out,
            'Re': Re_j
        })
        # print(f"Section {i}: y_mid={y_j_mid:.2f}m, chord={c_j:.3f}m, Re={Re_j:.2e}")
    return section_data_list

def generate_2d_stall_database(airfoil_profile, section_data, alphas_polar, xfoil_exe_path, ReNumbers):
    """Generate 2D airfoil polars across a range of Reynolds numbers using XFoil."""
    min_Re_section = min(s['Re'] for s in section_data)
    max_Re_section = max(s['Re'] for s in section_data)
    # print(f"Min/Max section Re for polars: {min_Re_section:.2e} / {max_Re_section:.2e}")

    discrete_Res_polar = np.array(sorted(list(set(
        np.round(np.geomspace(max(5e4, min_Re_section * 0.8), min(1e7, max_Re_section * 1.2), ReNumbers) / 1e4) * 1e4
    )))) #lower Re numbers more significant changes so log scale used
    print(f"Discrete Re for polars: {discrete_Res_polar}")

    stall_data_lookup = []
    airfoil_for_polars = asb.Airfoil(name=airfoil_profile.name, coordinates=airfoil_profile.coordinates)

    for Re_val in discrete_Res_polar:
        print(f"Generating 2D polar for Re = {Re_val:.2e}...")
        airfoil_for_polars.generate_polars(
            alphas=alphas_polar, Res=np.array([Re_val]),
            xfoil_kwargs={"xfoil_command": xfoil_exe_path, "max_iter": 20, "verbose": False, "timeout": 60},
            include_compressibility_effects=False
        )
        cls_2d = np.array([airfoil_for_polars.CL_function(alpha, Re_val) for alpha in alphas_polar])

        #identify stall cl and angle per airfoil analysis
        idx_stall = np.nanargmax(cls_2d)
        Cl_max_2D = cls_2d[idx_stall]
        alpha_stall_2D = alphas_polar[idx_stall]

        # Estimate K_post (post-stall slope) from the airfoils to them use on vlm
        K_post = -0.05  # Default
        valid_post_stall_alphas = []
        valid_post_stall_cls = []
        for i in range(1, 4):
            idx_after_stall = idx_stall + i
            if idx_after_stall < len(alphas_polar) and not np.isnan(cls_2d[idx_after_stall]): #if stall angle index+i is not longer than the remaining indexes and is not a nan
                valid_post_stall_alphas.append(alphas_polar[idx_after_stall])#then these are valid post stall points
                valid_post_stall_cls.append(cls_2d[idx_after_stall])
        
        if len(valid_post_stall_alphas) >= 2: #at least 2 points to get a slope
            try:
                unique_alphas, indices = np.unique(valid_post_stall_alphas, return_index=True) #makes sure values are unique and that duplicates are removed
                if len(unique_alphas) >= 2: #if still there are 2 or more points after duplicates removed
                    unique_cls = np.array(valid_post_stall_cls)[indices] #keeps indexes where alpha was unique
                    coeffs = np.polyfit(unique_alphas, unique_cls, 1) #perform regression
                    K_post = coeffs[0] #take slope as K
                elif abs(valid_post_stall_alphas[1] - valid_post_stall_alphas[0]) > 1e-6: #if there is only one unique point manually compute slope between stall point and single unique point
                    K_post = (valid_post_stall_cls[1] - valid_post_stall_cls[0]) / \
                                (valid_post_stall_alphas[1] - valid_post_stall_alphas[0])
            except (np.linalg.LinAlgError, ValueError):
                if abs(valid_post_stall_alphas[1] - valid_post_stall_alphas[0]) > 1e-6:
                    K_post = (valid_post_stall_cls[1] - valid_post_stall_cls[0]) / \
                                (valid_post_stall_alphas[1] - valid_post_stall_alphas[0])
        elif len(valid_post_stall_alphas) == 1:
            if abs(valid_post_stall_alphas[0] - alpha_stall_2D) > 1e-6:
                K_post = (valid_post_stall_cls[0] - Cl_max_2D) / \
                            (valid_post_stall_alphas[0] - alpha_stall_2D)

        stall_data_lookup.append({
            'Re_polar': Re_val, 'alpha_stall_2D': alpha_stall_2D,
            'Cl_max_2D': Cl_max_2D, 'K_post': K_post
        })
        # print(f"  Re={Re_val:.2e}: alpha_stall_2D={alpha_stall_2D:.2f} deg, Cl_max_2D={Cl_max_2D:.3f}, K_post={K_post:.4f}")

    if not stall_data_lookup:
        raise RuntimeError("Failed to generate any 2D polar data. Check XFoil setup and Re range.")
    return pd.DataFrame(stall_data_lookup)

def interpolate_stall_data_for_sections(section_data, stall_df, delta_alpha_3d_correction):
    """Interpolates 2D stall data for each section's Re and calculates 3D stall angle."""
    for section in section_data:
        Re_j = section['Re']
        #find two closest Re numbers that bracket Re_j and linerly interpolate between corresponding other parameter es// stall angle
        section['alpha_stall_2D_interp'] = np.interp(Re_j, stall_df['Re_polar'], stall_df['alpha_stall_2D'])#Interpolate and add to the section disctionary the interpolation as an entry with key section["blabla"]
        section['Cl_max_2D_interp'] = np.interp(Re_j, stall_df['Re_polar'], stall_df['Cl_max_2D'])
        section['K_post_interp'] = np.interp(Re_j, stall_df['Re_polar'], stall_df['K_post'])
        section['alpha_stall_3D'] = section['alpha_stall_2D_interp'] - delta_alpha_3d_correction #interpolated 2d stall angle minus delta 
        # print(f"Section {section['id']}: Re={Re_j:.2e}, alpha_stall_3D={section['alpha_stall_3D']:.2f} deg, Cl_max_2D_interp={section['Cl_max_2D_interp']:.3f}")
    return section_data

def run_vlm_sweep_with_stall_correction(alphas_to_sweep, vlm_airplane, velocity_op, 
                                        section_data_list_prepared, num_wing_sections, wing_geom, altitude):
    """Performs VLM alpha sweep and applies stall correction."""
    CLs_vlm, CDs_vlm, CLs_corrected_list = [], [], []
    result_collection = []
    lift_distribution = {"alpha": [], "CLs": []}

    for alpha_val in alphas_to_sweep:
        lift_distribution["alpha"].append(alpha_val)
        op_point = asb.OperatingPoint(
            velocity=velocity_op, alpha=alpha_val, beta=0, atmosphere=asb.Atmosphere(altitude=altitude)
        )
        vlm = asb.VortexLatticeMethod( #change spanwise and cordwise resolution for  better distribution approx
            airplane=vlm_airplane, op_point=op_point, spanwise_resolution=1, chordwise_resolution=1 #must keep chord at 1 beacuse only want one vortex per spanwise segment
        )

        results = vlm.run()
        result_collection.append({"alpha": alpha_val, "results": results})

        CLs_vlm.append(results.get("CL", np.nan))
        CDs_vlm.append(results.get("CD", np.nan))

        current_CL_corrected_for_this_alpha = np.nan
        can_correct_this_alpha = False
        Cl_loc_VLM_sections = []
        gamma_values_full_wing = vlm.vortex_strengths #compute cisrculation strength per panel, used to calculate sectional lift per panel
        gamma_values_one_side = None

        if gamma_values_full_wing is not None: #to account for symmetry
            if wing_geom.symmetric and len(gamma_values_full_wing) == 2 * num_wing_sections:
                gamma_values_one_side = gamma_values_full_wing[:num_wing_sections]
            elif len(gamma_values_full_wing) == num_wing_sections:
                gamma_values_one_side = gamma_values_full_wing
            else:
                print(f"Info @ alpha={alpha_val:.1f} deg: Gamma values length ({len(gamma_values_full_wing)}) unexpected. Fallback.")

            if gamma_values_one_side is not None: #if vlm did calculate circulation
                for j in range(num_wing_sections):
                    section_chord_j = section_data_list_prepared[j]['chord'] #extracts chord length per section
                    Cl_j = (2 * gamma_values_one_side[j]) / (velocity_op * section_chord_j) if velocity_op * section_chord_j != 0 else np.nan #compute cl per panel
                    Cl_loc_VLM_sections.append(Cl_j)
                if len(Cl_loc_VLM_sections) == num_wing_sections: #if number of computed lift coefficient matches number of sections then stall correction can be applied
                    can_correct_this_alpha = True
                else:
                    print(f"Error @ alpha={alpha_val:.1f} deg: Mismatch in Cl_loc_VLM_sections population.")
        else:
            print(f"Info @ alpha={alpha_val:.1f} deg: No 'vortex_strengths' on VLM object. Fallback.")
        
        #build up lift per section
        if can_correct_this_alpha:
            numerator_sum_cl_c_dy = 0 #sum of total lift
            all_sections_valid_for_sum = True
            for j in range(num_wing_sections): #per section
                section = section_data_list_prepared[j]
                Cl_vlm_j = Cl_loc_VLM_sections[j] #sectional lift from vlm
                if np.isnan(Cl_vlm_j):
                    all_sections_valid_for_sum = False; break
                
                corrected_Cl_j = Cl_vlm_j #set corrected sectional lift to VLM result as default
                if alpha_val >= section['alpha_stall_3D']: #if current alpha > 3d stall angle for section section is stalled
                    delta_alpha = alpha_val - section['alpha_stall_3D']
                    #create downwards slope equation
                    cl_2D_model = section['Cl_max_2D_interp'] + section['K_post_interp'] * delta_alpha
                    cl_2D_model = max(0, cl_2D_model)#limit lift to a min of 0
                    corrected_Cl_j = min(Cl_vlm_j, cl_2D_model)#takes smallest between corrected lift and post stall model
                    Cl_loc_VLM_sections[j] = corrected_Cl_j
                numerator_sum_cl_c_dy += corrected_Cl_j * section['area'] #adds contribution of corrected sectional lift coeff times area
            
            if all_sections_valid_for_sum:
                S_wing = wing_geom.area()
                current_CL_corrected_for_this_alpha = (2 * numerator_sum_cl_c_dy) / S_wing if S_wing > 1e-9 else np.nan #twice for symmetry
            else:
                print(f"Warning @ alpha={alpha_val:.1f} deg: Sectional Cl (from gamma) is NaN. Corrected CL for this alpha will be NaN.")
        lift_distribution['CLs'].append(Cl_loc_VLM_sections)
        if np.isnan(current_CL_corrected_for_this_alpha) and not can_correct_this_alpha:
            print(f"Info @ alpha={alpha_val:.1f} deg: Sectional correction could not be applied. Result for corrected CL is NaN.")
        
        CLs_corrected_list.append(current_CL_corrected_for_this_alpha)
        # print(f"Number of VLM panels: {len(vlm.vortex_strengths)}")
    # print(f"Number of VLM panels: {len(vlm.vortex_strengths)}")

    return CLs_vlm, CDs_vlm, CLs_corrected_list, result_collection, lift_distribution

def plot_aerodynamic_coefficients(alphas, CLs_vlm, CLs_corrected, CDs_vlm):
    """Plots the CL and CD curves."""
    print("\nAlpha Sweep Results (Original VLM vs. Corrected CL):")
    print("----------------------------------------------------------")
    print("Alpha (deg) | CL (VLM) | CD (VLM) | CL (Corrected)")
    print("----------------------------------   ------------------------")
    for i in range(len(alphas)):
        print(f"{alphas[i]:11.1f} | {CLs_vlm[i]:8.4f} | {CDs_vlm[i]:8.5f} | {CLs_corrected[i]:12.4f}")
    print("----------------------------------------------------------")

    plt.figure(figsize=(10, 7))
    plt.plot(alphas, CLs_vlm, label="CL (VLM Original)", marker='o', linestyle='--')
    plt.plot(alphas, CLs_corrected, label="CL (Corrected with Re Effects)", marker='x')
    plt.xlabel("Angle of Attack (deg)")
    plt.ylabel("Lift Coefficient (CL)")
    plt.legend(); plt.grid(True); plt.title("CL vs Alpha (VLM with Multi-Re Stall Correction)")
    plt.show()

    plt.figure(figsize=(10,7))
    plt.plot(alphas, CDs_vlm, label="CD (VLM Original)", marker='s')
    plt.xlabel("Angle of Attack (deg)")
    plt.ylabel("Drag Coefficient (CD)")
    plt.legend(); plt.grid(True); plt.title("CD vs Alpha (VLM)")
    plt.show()

