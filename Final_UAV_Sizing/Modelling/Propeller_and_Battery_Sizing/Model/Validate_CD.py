import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import *
import numpy as np

#Values from reference paper
W= 1.684*9.81
CLmax = 2
V_vert_prop = 11
numberengines_vertical = 4
numberengines_horizontal = 1
propeller_wake_efficiency = 0.7
L_blade = 0.2413
w_blade = 0.025
L_stab= 0.1016
w_stab= 0.1778
L_poles= 0.4826 
w_poles= 0.016 
L_motor = 0.09
L_gimbal = 0.12
L_speaker = 0.1
L_wing= 0.1524
w_wing = 1.2192
S_wing = 0.1858

L_n = 0
L_c = 0.8966
L_fus = 0.8966
w_fus = S_wing / L_fus
d_fus = 0.15
import matplotlib.pyplot as plt
def CD_alpha():
    velocity_smooth = [15, 11]
    rho, altitude = 1.225, 0

    for velocity in velocity_smooth:
        Cf_blade = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_blade, w_blade)
        Cf_stab = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_stab, w_stab)
        Cf_poles = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_poles, w_poles)
        Cf_fus = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_fus, w_fus)
        CD_motor = cube_drag_coefficient(velocity, rho, altitude, S_wing, L_motor)
        CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)
        Cf_wing = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_wing, w_wing)

        alpha_w = np.array([
        -5.00, -4.00, -3.00, -2.00, -1.00,
        0.00,  1.00,  2.00,  3.00,  4.00,
        5.00,  6.00,  7.00,  8.00,  9.00,
        10.00, 11.00, 12.00, 13.00, 14.00,
        15.00, 16.00, 17.00, 18.00, 19.00,
        20.00, 21.00, 22.00, 23.00, 24.00,
        25.00])

        CD = np.array([
        0.0054, 0.0071, 0.0095, 0.0127, 0.0165,
        0.0211, 0.0263, 0.0322, 0.0388, 0.0460,
        0.0538, 0.0623, 0.0713, 0.0809, 0.0910,
        0.1017, 0.1128, 0.1244, 0.1364, 0.1488,
        0.1615, 0.1746, 0.1880, 0.2016, 0.2154,
        0.2294, 0.2435, 0.2577, 0.2719, 0.2862,
        0.3004])

        CL_list = np.array([
        0.2379, 0.3298, 0.4215, 0.5131, 0.6043,
        0.6953, 0.7859, 0.8760, 0.9657, 1.0547,
        1.1432, 1.2309, 1.3179, 1.4041, 1.4894,
        1.5738, 1.6572, 1.7396, 1.8209, 1.9011,
        1.9801, 2.0580, 2.1345, 2.2098, 2.2837,
        2.3563, 2.4274, 2.4971, 2.5654, 2.6322,
        2.6974])
        
        ai=5

        alpha = alpha_w-ai

        # Compute UAV CD including CD_wing (vector) + components (scalars)
        CD_UAV = CD_fus + CD + 4 * Cf_blade + 3 * Cf_stab + 2 * Cf_poles + 4 * CD_motor + Cf_wing # + CD_gimbal + CD_speaker
        # Compute reference curve
        if velocity == 15:
            CD_ref = 0.2398 + 0.0016 * alpha + 0.001496 * alpha**2
            CL_fly = (2* W) / (rho * velocity**2 * S_wing)
            alpha_fly = 0
        else:
            CD_ref = 0.3127 - 0.002008 * alpha + 0.001483 * alpha**2
            CL_fly = (2* W) / (rho * velocity**2 * S_wing)
            alpha_fly= 6
        mask = (alpha >= 0) & (alpha <= 10)
        alpha_filtered = alpha[mask]
        CD_UAV_filtered = CD_UAV[mask]
        CD_ref_filtered = CD_ref[mask]
        print(CL_fly)
        plt.figure(figsize=(10, 6))
        plt.plot(alpha_filtered, CD_UAV_filtered, label=f'UAV CD at V = {velocity} m/s')
        plt.plot(alpha_filtered, CD_ref_filtered, linestyle='--', label=f'Reference CD at V = {velocity} m/s')
        plt.xlabel('Angle of Attack (degrees)')
        plt.ylabel('Drag Coefficient (CD)')
        plt.title('Drag Coefficient vs Angle of Attack')
        plt.grid(True)
        plt.axvline(x=alpha_fly, color='r', linestyle=':', label=f'alpha_fly = {alpha_fly}°')

        averag_difference = np.mean(np.abs(CD_UAV_filtered - CD_ref_filtered))
        # Find the difference at alpha_fly
        
        idx = np.where(alpha_filtered == alpha_fly)[0][0]
        diff_at_alpha_fly = np.abs(CD_UAV_filtered[idx] - CD_ref_filtered[idx])
        plt.text(0.02, 0.98, f'Average Difference: {averag_difference:.4f}', transform=plt.gca().transAxes, verticalalignment='top')
        plt.text(0.02, 0.92, f'Difference at alpha_fly: {diff_at_alpha_fly:.4f}', transform=plt.gca().transAxes, verticalalignment='top')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right')
        plt.tight_layout()
        plt.show()

print(CD_alpha())