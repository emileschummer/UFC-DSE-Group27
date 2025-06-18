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
L_poles= 0.4826 #0.016
w_poles= 0.016# 0.4826
L_motor = 0.1
L_gimbal = 0.12
L_speaker = 0.1

L_n = 0.15
L_c = 0.6
L_fus = 0.8966
w_fus = S_wing / L_fus
d_fus = 0.08
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

        alpha_w = np.array([
        -4.000, -3.500, -3.000, -2.500, -2.000,
        1.000,  1.500,  2.000,  2.500,  3.000,  3.500,  4.000,  4.500,
        5.000,  5.500,  6.000,  6.500,  7.000,  7.500,  8.000,  8.500,
        9.000,  9.500, 10.000, 10.500, 11.000, 11.500, 12.000, 12.500,
        13.000, 13.500, 14.000, 14.500, 15.000, 15.500, 16.000, 16.500,
        17.000, 17.500, 18.000, 18.500, 19.000, 19.500, 20.000
        ])

        CD_wing = np.array([
        0.01043, 0.01175, 0.01245, 0.01297, 0.01342,
        0.01626, 0.01678, 0.01735, 0.01797, 0.01863, 0.01934, 0.02009, 0.02088,
        0.02173, 0.02267, 0.02371, 0.02486, 0.02614, 0.02786, 0.02964, 0.03162,
        0.03383, 0.03635, 0.03918, 0.04239, 0.04597, 0.04996, 0.05440, 0.05925,
        0.06455, 0.07028, 0.07643, 0.08295, 0.08986, 0.09706, 0.10460, 0.11243,
        0.12059, 0.12894, 0.13747, 0.14618, 0.15513, 0.16430, 0.17371
        ])
        CL = np.array([
        0.0382, 0.0959, 0.1509, 0.2039, 0.2585,
        0.5050, 0.5469, 0.5905, 0.6344, 0.6782, 0.7215, 0.7637, 0.8042,
        0.8419, 0.8787, 0.9147, 0.9494, 0.9828, 1.0097, 1.0370, 1.0627,
        1.0864, 1.1079, 1.1269, 1.1436, 1.1580, 1.1698, 1.1796, 1.1877,
        1.1936, 1.1975, 1.1998, 1.2009, 1.2002, 1.1981, 1.1951, 1.1914,
        1.1868, 1.1820, 1.1769, 1.1717, 1.1668, 1.1619, 1.1572
        ])
        ai=5

        alpha = alpha_w-ai

        # Compute UAV CD including CD_wing (vector) + components (scalars)
        CD_UAV = CD_fus + CD_wing + 4 * Cf_blade + 3 * Cf_stab + 2 * Cf_poles + 4 * CD_motor  # + CD_gimbal + CD_speaker

        # Compute reference curve
        if velocity == 15:
            CD_ref = 0.2398 + 0.0016 * alpha + 0.001496 * alpha**2
        elif velocity == 11:
            CD_ref = 0.3127 - 0.002008 * alpha + 0.001483 * alpha**2
        else:
            CD_ref = np.full_like(alpha, np.nan)
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

#alpha at 15m/s = -2.500
#alpha at 11m/s = 9