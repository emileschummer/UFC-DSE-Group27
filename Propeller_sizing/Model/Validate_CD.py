import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pandas as pd
from Propeller_sizing.Model.UFC_FC_YEAH import *
import Propeller_sizing.Input.Strava_input_csv as sva
from statistics import mode, StatisticsError
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
L_motor = 0.1
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
        -5.0, -4.0, -3.0, -2.0, -1.0,
        0.0,  1.0,  2.0,  3.0,  4.0,
        5.0,  6.0,  7.0,  8.0,  9.0,
        10.0, 11.0, 12.0, 13.0, 14.0,
        15.0])

        CD = np.array([
        0.0079, 0.0050, 0.0027, 0.0012, 0.0003,
        0.0000, 0.0004, 0.0015, 0.0033, 0.0057,
        0.0087, 0.0124, 0.0168, 0.0217, 0.0273,
        0.0334, 0.0401, 0.0473, 0.0551, 0.0634,
        0.0721])

        CL_list = np.array([
        -0.4308, -0.3424, -0.2537, -0.1649, -0.0760,
        0.0130,  0.1020,  0.1909,  0.2797,  0.3683,
        0.4566,  0.5446,  0.6323,  0.7195,  0.8062,
        0.8924,  0.9779,  1.0628,  1.1470,  1.2304,
        1.3130])
        
        ai=5

        alpha = alpha_w-ai

        # Compute UAV CD including CD_wing (vector) + components (scalars)
        CD_UAV = CD_fus + CD + 4 * Cf_blade + 3 * Cf_stab + 2 * Cf_poles + 4 * CD_motor + Cf_wing # + CD_gimbal + CD_speaker
        # Compute reference curve
        if velocity == 15:
            CD_ref = 0.2398 + 0.0016 * alpha + 0.001496 * alpha**2
            alpha_fly= 2
        else:
            CD_ref = 0.3127 - 0.002008 * alpha + 0.001483 * alpha**2
            alpha_fly= 8
        mask = (alpha >= 0) & (alpha <= 10)
        alpha_filtered = alpha[mask]
        CD_UAV_filtered = CD_UAV[mask]
        CD_ref_filtered = CD_ref[mask]

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