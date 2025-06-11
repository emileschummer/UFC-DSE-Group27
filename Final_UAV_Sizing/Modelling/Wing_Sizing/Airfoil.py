import numpy as np
from matplotlib import pyplot as plt
import aerosandbox as asb
import pandas as pd

#put span in inputs, line 15 here
def setup_wing_and_airplane(chosen_airfoil, num_spanwise_sections, r_chord, t_chord, r_twist, t_twist, sweep):
    """Define wing geometry and create an airplane object."""
    wing = asb.Wing(
        name="Wing",
        xsecs=[
            asb.WingXSec(
                xyz_le=[0, 0, 0], chord=r_chord, twist=r_twist, airfoil=chosen_airfoil,
            ),
            asb.WingXSec(
                xyz_le=[sweep, 1.5, 0], chord=t_chord, twist=t_twist, airfoil=chosen_airfoil,
            ),
        ],
        symmetric=True,
    )
    wing = wing.subdivide_sections(num_spanwise_sections)
    airplane = asb.Airplane(wings=[wing])
    # print(f"Wing Setup: Span={wing.span():.2f}m, Area={wing.area():.2f}m^2, AR={wing.aspect_ratio():.2f}")
    return wing, airplane

def calculate_section_properties_and_reynolds(wing_object, operational_velocity, operational_altitude):
    """Calculate geometric properties and Reynolds numbers for each wing section."""
    section_data_list = []
    #flow properties
    operational_point_data = asb.OperatingPoint(velocity=operational_velocity, atmosphere=asb.Atmosphere(altitude=operational_altitude))
    rho = operational_point_data.atmosphere.density()
    mu = operational_point_data.atmosphere.dynamic_viscosity()
    nu = mu / rho

    for i, (xsec_in, xsec_out) in enumerate(zip(wing_object.xsecs[:-1], wing_object.xsecs[1:])):
        chord_in = xsec_in.chord
        chord_out = xsec_out.chord
        y_in = xsec_in.xyz_le[1]
        y_out = xsec_out.xyz_le[1]

        c_j = (chord_in + chord_out) / 2 #take mid point chords and distances because vlm solves on N panels 
        y_j_mid = (y_in + y_out) / 2
        delta_y_j = y_out - y_in
        area_j = c_j * delta_y_j
        Re_j = (operational_velocity * c_j) / nu

        section_data_list.append({
            'id': i, 'y_mid': y_j_mid, 'chord': c_j, 'span_segment': delta_y_j,
            'area': area_j, 'xsec_in_xyz_le_y': y_in, 'xsec_out_xyz_le_y': y_out,
            'Re': Re_j
        })
        # print(f"Section {i}: y_mid={y_j_mid:.2f}m, chord={c_j:.3f}m, Re={Re_j:.2e}")
    return section_data_list

def generate_2d_stall_database(airfoil_profile, section_data, alpha_range2D, xfoil_path, Re_numbers):
    """Generate 2D airfoil polars across a range of Reynolds numbers using XFoil."""
    min_Re_section = min(s['Re'] for s in section_data)
    max_Re_section = max(s['Re'] for s in section_data)
    # print(f"Min/Max section Re for polars: {min_Re_section:.2e} / {max_Re_section:.2e}")

    discrete_Re_values = np.array(sorted(list(set(
        np.round(np.geomspace(max(5e4, min_Re_section * 0.8), min(1e7, max_Re_section * 1.2), Re_numbers) / 1e4) * 1e4
    )))) #lower Re numbers more significant changes so log scale used
    # print(f"Discrete Re for polars: {discrete_Re_values}")

    stall_data_dictionary = []
    airfoil_for_polars = asb.Airfoil(name=airfoil_profile.name, coordinates=airfoil_profile.coordinates)

    for Re_value in discrete_Re_values:
        # print(f"Generating 2D polar for Re = {Re_value:.2e}...")
        airfoil_for_polars.generate_polars(
            alphas=alpha_range2D, Res=np.array([Re_value]),
            xfoil_kwargs={"xfoil_command": xfoil_path, "max_iter": 20, "verbose": False, "timeout": 60},
            include_compressibility_effects=False
        )
        cl_2D_array = np.array([airfoil_for_polars.CL_function(alpha, Re_value) for alpha in alpha_range2D])

        #identify stall cl and angle per airfoil analysis
        idx_stall = np.nanargmax(cl_2D_array)
        Cl_max_2D = cl_2D_array[idx_stall]
        alpha_stall_2D = alpha_range2D[idx_stall]

        # Estimate K_post (post-stall slope) from the airfoils to them use on vlm
        K_post = -0.05  # Default
        valid_post_stall_alphas = []
        valid_post_stall_cls = []
        for i in range(1, 4):
            idx_after_stall = idx_stall + i
            if idx_after_stall < len(alpha_range2D) and not np.isnan(cl_2D_array[idx_after_stall]): #if stall angle index+i is not longer than the remaining indexes and is not a nan
                valid_post_stall_alphas.append(alpha_range2D[idx_after_stall])#then these are valid post stall points
                valid_post_stall_cls.append(cl_2D_array[idx_after_stall])
        
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

        stall_data_dictionary.append({
            'Re_polar': Re_value, 'alpha_stall_2D': alpha_stall_2D,
            'Cl_max_2D': Cl_max_2D, 'K_post': K_post
        })
        # print(f"  Re={Re_value:.2e}: alpha_stall_2D={alpha_stall_2D:.2f} deg, Cl_max_2D={Cl_max_2D:.3f}, K_post={K_post:.4f}")

    if not stall_data_dictionary:
        raise RuntimeError("Failed to generate any 2D polar data. Check XFoil setup and Re range.")
    return pd.DataFrame(stall_data_dictionary)

def interpolate_stall_data_for_sections(section_data, stall_df, delta_alpha_3D_correction):
    """Interpolates 2D stall data for each section's Re and calculates 3D stall angle."""
    for section in section_data:
        Re_j = section['Re']
        #find two closest Re numbers that bracket Re_j and linerly interpolate between corresponding other parameter es// stall angle
        section['alpha_stall_2D_interp'] = np.interp(Re_j, stall_df['Re_polar'], stall_df['alpha_stall_2D'])#Interpolate and add to the section disctionary the interpolation as an entry with key section["blabla"]
        section['Cl_max_2D_interp'] = np.interp(Re_j, stall_df['Re_polar'], stall_df['Cl_max_2D'])
        section['K_post_interp'] = np.interp(Re_j, stall_df['Re_polar'], stall_df['K_post'])
        section['alpha_stall_3D'] = section['alpha_stall_2D_interp'] - delta_alpha_3D_correction #interpolated 2d stall angle minus delta 
        # print(f"Section {section['id']}: Re={Re_j:.2e}, alpha_stall_3D={section['alpha_stall_3D']:.2f} deg, Cl_max_2D_interp={section['Cl_max_2D_interp']:.3f}")
    return section_data

def run_vlm_sweep_with_stall_correction(alpha_range3D, vlm_airplane, operational_velocity, 
                                        section_data_list, num_spanwise_sections, wing, operational_altitude,
                                        vlm_chordwise_resolution=6): # Added vlm_chordwise_resolution
    """Performs VLM alpha sweep and applies stall correction."""
    CLs_vlm, CDs_vlm, CLs_corrected_list, Cm = [], [], [], []
    lift_distribution = {"alpha": [], "CLs": []}

    for alpha_value in alpha_range3D: #per alpha
        lift_distribution["alpha"].append(alpha_value) #save for lift distribution
        op_point = asb.OperatingPoint(
            velocity=operational_velocity, alpha=alpha_value, beta=0, atmosphere=asb.Atmosphere(altitude=operational_altitude)
        )
        vlm = asb.VortexLatticeMethod( 
            airplane=vlm_airplane, op_point=op_point, 
            spanwise_resolution=1, # Keeps one VLM "strip" per subdivided wing section
            chordwise_resolution=vlm_chordwise_resolution)

        results = vlm.run()

        CLs_vlm.append(results.get("CL", np.nan))
        CDs_vlm.append(results.get("CD", np.nan))
        Cm.append(results.get("Cm", np.nan))


        current_CL_corrected_for_this_alpha = np.nan #lift coefficent for current angle of attack after correctio for stall
        can_correct_this_alpha = False
        CL_local_VLM_section = [] #local sectional lift coefficeint list of each spanwise section
        gamma_values_full_wing = vlm.vortex_strengths #compute cisrculation strength per panel, used to calculate sectional lift per panel
        gamma_values_one_side = None #needed for symmetric analysis

        if gamma_values_full_wing is not None: #if contain data, VLM did't fail
            expected_gamma_len_one_side = num_spanwise_sections * vlm_chordwise_resolution #expected number of vortexes for one side of wing
            if wing.symmetric and len(gamma_values_full_wing) == 2 * expected_gamma_len_one_side: #check if wing symmetric and returned values form VLM is double the expecetd amount per wing 
                gamma_values_one_side = gamma_values_full_wing[:expected_gamma_len_one_side] #extract vortex strength for just one side, slice from beginning to end for one side
            elif not wing.symmetric and len(gamma_values_full_wing) == expected_gamma_len_one_side:
                gamma_values_one_side = gamma_values_full_wing
            else:
                print(f"Info @ alpha={alpha_value:.1f} deg: Gamma values length ({len(gamma_values_full_wing)}) unexpected for {num_spanwise_sections} sections and {vlm_chordwise_resolution} chordwise panels. Expected {2*expected_gamma_len_one_side if wing.symmetric else expected_gamma_len_one_side}. Fallback.")

            if gamma_values_one_side is not None: #if vlm did calculate circulation and are of the expected array size
                for j in range(num_spanwise_sections): #per spanwise section of half wing
                    section_chord_j = section_data_list[j]['chord'] #chord legth of current spanwise section
                    
                    # Sum gammas for all chordwise panels in this spanwise section
                    start_idx = j * vlm_chordwise_resolution
                    end_idx = (j + 1) * vlm_chordwise_resolution
                    gamma_list_for_section_j_panels = gamma_values_one_side[start_idx:end_idx] #slice array to extract all vortices of chorwise panels corresponding to a spanwise section
                    
                    if len(gamma_list_for_section_j_panels) != vlm_chordwise_resolution: #check if extracted vortices corresponds to expected number
                        print(f"Error @ alpha={alpha_value:.1f} deg, section {j}: Incorrect number of gamma values found for chordwise sum. Expected {vlm_chordwise_resolution}, got {len(gamma_list_for_section_j_panels)}.")
                        CL_local_VLM_section.append(np.nan) #if check fails append nan to local sectional lift coefficeint of spanwise sectio
                        continue

                    total_gamma_for_section_j = np.sum(gamma_list_for_section_j_panels) #sum of all vortex strengths for chordwise panels in corrent spanwise section. It is the total circulation around that 2D strip.
                    
                    #calculate sectional lift coefficient for spanwise section
                    CL_j = (2 * total_gamma_for_section_j) / (operational_velocity * section_chord_j) if operational_velocity * section_chord_j != 0 else np.nan #safety check to prevent division by zero
                    CL_local_VLM_section.append(CL_j) #append calculated CL per spanwise section
                
                if len(CL_local_VLM_section) == num_spanwise_sections: #check if have one lift coefficient per spanwise section
                    can_correct_this_alpha = True #then can correct vlm
                else:
                    print(f"Error @ alpha={alpha_value:.1f} deg: Mismatch in CL_local_VLM_section population after processing gammas.")
        else: #if the VLM didn't run at the beginning so returned no vortex strengths
            print(f"Info @ alpha={alpha_value:.1f} deg: No 'vortex_strengths' on VLM object. Fallback.")
        
        #build up lift per section
        if can_correct_this_alpha:
            numerator_weightedaverage_CL = 0 #sum of local CL*area of panel
            all_sections_valid_for_sum = True #set to true for later
            for j in range(num_spanwise_sections): #sweep through number of wing sections
                section = section_data_list[j]
                Cl_vlm_j = CL_local_VLM_section[j] 
                if np.isnan(Cl_vlm_j): #check if CL per spanwise section found from vortix is not nan
                    all_sections_valid_for_sum = False; break
                
                corrected_CL_j = Cl_vlm_j 
                if alpha_value >= section['alpha_stall_3D']: #if above stall angle
                    delta_alpha = alpha_value - section['alpha_stall_3D'] #how far ahead
                    
                    CL_2D_correction = section['Cl_max_2D_interp'] + section['K_post_interp'] * delta_alpha #perform correction using slope approximated earlier
                    CL_2D_correction = max(0, CL_2D_correction) #limit to not be below zero
                    corrected_CL_j = min(Cl_vlm_j, CL_2D_correction) #take the smallest of the two
                    CL_local_VLM_section[j] = corrected_CL_j # Store corrected CL for this section
                numerator_weightedaverage_CL += corrected_CL_j * section['area'] #weigh CL by sectional area and add to total
            
            if all_sections_valid_for_sum:
                S_wing = wing.area()#find total wing area
                current_CL_corrected_for_this_alpha = (2 * numerator_weightedaverage_CL) / S_wing if S_wing > 1e-9 else np.nan #finish weighted average by deviding all summed CL*sectional area by total area
            else:
                print(f"Warning @ alpha={alpha_value:.1f} deg: Sectional Cl (from gamma) is NaN for one or more sections. Corrected CL for this alpha will be NaN.")
        lift_distribution['CLs'].append(CL_local_VLM_section if can_correct_this_alpha and len(CL_local_VLM_section) == num_spanwise_sections else [np.nan]*num_spanwise_sections) # Appends only if could correct and of appropriate length
        if np.isnan(current_CL_corrected_for_this_alpha) and not can_correct_this_alpha:
            print(f"Info @ alpha={alpha_value:.1f} deg: Sectional correction could not be applied. Result for corrected CL is NaN.")
        
        CLs_corrected_list.append(current_CL_corrected_for_this_alpha)
        
    return CLs_vlm, CDs_vlm, CLs_corrected_list, lift_distribution, Cm

def plot_aerodynamic_coefficients(alphas, CLs_vlm, CLs_corrected, CDs_vlm, Plot = False):
    """Plots the CL and CD curves."""
    # print("\nAlpha Sweep Results (Original VLM vs. Corrected CL):")
    # print("----------------------------------------------------------")
    # print("Alpha (deg) | CL (VLM) | CD (VLM) | CL (Corrected)")
    # print("----------------------------------   ------------------------")
    # for i in range(len(alphas)):
    #     print(f"{alphas[i]:11.1f} | {CLs_vlm[i]:8.4f} | {CDs_vlm[i]:8.5f} | {CLs_corrected[i]:12.4f}")
    # print("----------------------------------------------------------")
    if Plot == True:
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