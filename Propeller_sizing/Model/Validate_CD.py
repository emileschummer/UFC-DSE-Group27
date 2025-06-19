import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pandas as pd
from Propeller_sizing.Model.UFC_FC_YEAH import *
import Propeller_sizing.Input.Strava_input_csv as sva
from statistics import mode, StatisticsError
import numpy as np


W= 1.684*9.81
S_wing = 0.1858
CLmax = 2
V_vert_prop = 11
numberengines_vertical = 4
numberengines_horizontal = 1
propeller_wake_efficiency = 0.7
L_blade = 0.2413
w_blade = 0.025
L_stab= 0.1016
w_stab= 0.1778
L_poles=0.4826 
w_poles= 0.016 
L_motor = 0.1
L_gimbal = 0.12
L_speaker = 0.1
L_wing= 0.1524
w_wing = 1.2192

L_n = 0
L_c = 0.8966
L_fus = 0.8966
w_fus = S_wing / L_fus
d_fus = 0.15
import matplotlib.pyplot as plt

aero_df = pd.read_csv('Propeller_sizing/Input/Validation_data.csv')
aero_df.columns = aero_df.columns.str.strip()
#print(aero_df.columns.tolist())
def CD_alpha():
    velocity_smooth = [15, 11]
    rho, altitude = 1.225, 0

    for velocity in velocity_smooth:
        Cf_blade = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_blade, w_blade)
        Cf_stab = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_stab, w_stab)
        Cf_poles = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_poles, w_poles)
        Cf_fus = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_fus, w_fus)
        CD_speaker = cube_drag_coefficient(velocity, rho, altitude, S_wing, L_speaker)
        CD_gimbal = cube_drag_coefficient(velocity, rho, altitude, S_wing, L_gimbal)
        CD_motor = cube_drag_coefficient(velocity, rho, altitude, S_wing, L_motor)
        CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)
        Cf_wing = flat_plate_drag_coefficient(velocity, rho, altitude, S_wing, L_wing, w_wing)

        alpha_w = np.array([
        -5.0, -4.0, -3.0, -2.0, -1.0,
        0.0,  1.0,  2.0,  3.0,  4.0,
        5.0,  6.0,  7.0,  8.0,  9.0,
        10.0, 11.0, 12.0, 13.0, 14.0,
        15.0])

        CD_wing = np.array([
        0.0079, 0.0050, 0.0027, 0.0012, 0.0003,
        0.0000, 0.0004, 0.0015, 0.0033, 0.0057,
        0.0087, 0.0124, 0.0168, 0.0217, 0.0273,
        0.0334, 0.0401, 0.0473, 0.0551, 0.0634,
        0.0721])
        
        ai=5

        alpha = alpha_w-ai

        # Compute UAV CD including CD_wing (vector) + components (scalars)
        CD_UAV = CD_fus + CD_wing + 4 * Cf_blade + 3 * Cf_stab + 2 * Cf_poles + 4 * CD_motor + Cf_wing # + CD_gimbal + CD_speaker

        # Compute reference curve
        if velocity == 15:
            CD_ref = 0.2398 + 0.0016 * alpha + 0.001496 * alpha**2
        else:
            CD_ref = 0.3127 - 0.002008 * alpha + 0.001483 * alpha**2
        d_CD= CD_ref-CD_UAV
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

        error = np.mean(np.abs(CD_UAV_filtered - CD_ref_filtered))
        plt.text(0.02, 0.98, f'Average Error: {error:.4f}', transform=plt.gca().transAxes, verticalalignment='top')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right')
        plt.tight_layout()
        plt.show()

print(CD_alpha())