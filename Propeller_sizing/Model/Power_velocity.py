import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.interpolate import interp1d

from Propeller_sizing.Model.UFC_FC_YEAH import calculate_power_FC
import Propeller_sizing.Input.Strava_input_csv as sva
from Final_UAV_Sizing.Input.fixed_input_values import *

W= 25*g

aero_df = pd.read_csv('Propeller_sizing/Model/aero.csv')

# Load race and propeller data
races = sva.make_race_dictionnary()
df_vertical = pd.read_csv('Propeller_sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv')
df_vertical['Thrust_N'] = df_vertical[' Thrust_g '] * g / 1000
df_horizontal = pd.read_csv('Propeller_sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv')
df_horizontal['Thrust_N'] = df_horizontal[' Thrust_g '] * g / 1000


def power_V():
    """
    Compute and plot the baseline mean power vs velocity (range shaded).
    """
    all_power_curves = []
    for race_data in races.values():
        P_list, v_list = [], []
        t_prev = v_prev = g_prev = 0
        for _, row in race_data.iterrows():
            t = row[' time']
            v = row[' velocity_smooth']
            g_smooth = np.arctan(row[' grade_smooth'] / 100)
            rho = sva.air_density_isa(row[' altitude'])

            dt = t - t_prev
            if t_prev > 0 and dt > 0:
                accel = (v - v_prev) / dt
                pitch_rate = (g_smooth - g_prev) / dt
            else:
                accel = pitch_rate = 0

            P = calculate_power_FC(df_vertical,df_horizontal,g_smooth,v,rho, accel, pitch_rate, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, w_fus, d_fus,L_blade,L_stab, L_poles, w_poles,L_speaker, L_gimbal, L_motor)
            v_list.append(v)
            P_list.append(P)
            t_prev, v_prev, g_prev = t, v, g_smooth

        df_pv = pd.DataFrame({'Velocity': v_list, 'Power': P_list})
        all_power_curves.append(df_pv.groupby('Velocity')['Power'].mean().sort_index())

    grid = sorted(set().union(*(c.index for c in all_power_curves)))
    aligned = [c.reindex(grid).interpolate() for c in all_power_curves]
    data = np.vstack([c.values for c in aligned])

    plt.fill_between(grid, data.min(axis=0), data.max(axis=0), color='#00BFFF', alpha=0.3)
    plt.plot(grid, data.mean(axis=0), color='#FF4500', linewidth=2)
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Power (W)')
    # leave title to __main__


def power_V_sensitivity(n_iters=5, variation_pct=0.10, random_seed=None):
    """
    Perform sensitivity analysis by varying velocity_smooth, grade_smooth, and altitude
    by ±variation_pct and computing mean power vs velocity across races over n_iters.

    Parameters:
        races: dict of DataFrames, keyed by race name
        df_vertical, df_horizontal, W, V_vert_prop, CLmax, S_wing, aero_df,
        numberengines_vertical, numberengines_horizontal, propeller_wake_efficiency,
        L_fus, L_n, L_c, w_fus, d_fus, L_blade, L_stab, L_poles,
        w_poles, L_speaker, L_gimbal, L_motor: inputs passed to calculate_power_FC
        n_iters: int, number of random perturbation iterations
        variation_pct: float, max fractional variation (e.g., 0.1 = 10%)
        random_seed: int or None, seed for reproducibility

    Returns:
        None. Shows a plot of mean power vs velocity for each iteration.
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    all_iter_mean = []

    # Iterate sensitivity runs
    for it in range(n_iters):
        per_iter_power = []

        for race_name, race_data in races.items():
            P_list = []
            velocity_list = []
            t = 0
            prev_velocity = 0
            prev_grade = 0

            # Generate random variation factors for each signal
            v_factor = 1 + np.random.uniform(-variation_pct, variation_pct, size=len(race_data))
            g_factor = 1 + np.random.uniform(-variation_pct, variation_pct, size=len(race_data))
            a_factor = 1 + np.random.uniform(-variation_pct, variation_pct, size=len(race_data))

            for idx, row in race_data.iterrows():
                time = row[' time']
                velocity_smooth = row[' velocity_smooth'] * v_factor[idx]
                grade_smooth = np.arctan((row[' grade_smooth'] * g_factor[idx]) / 100)
                altitude = row[' altitude'] * a_factor[idx]
                rho = sva.air_density_isa(altitude)

                dt = time - t
                if t > 0 and dt > 0:
                    acceleration = (velocity_smooth - prev_velocity) / dt
                    pitch_rate = (grade_smooth - prev_grade) / dt
                else:
                    acceleration = pitch_rate = 0

                prev_velocity, prev_grade, t = velocity_smooth, grade_smooth, time

                P = calculate_power_FC(df_vertical,df_horizontal,grade_smooth,velocity_smooth,rho, acceleration, pitch_rate, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, w_fus, d_fus,L_blade,L_stab, L_poles, w_poles,L_speaker, L_gimbal, L_motor)
                velocity_list.append(velocity_smooth)
                P_list.append(P)

            df_power_vel = pd.DataFrame({'Power': P_list, 'Velocity': velocity_list})
            mean_curve = df_power_vel.groupby('Velocity')['Power'].mean().sort_index()
            per_iter_power.append(mean_curve)

        common_idx = sorted(set().union(*[df.index for df in per_iter_power]))
        aligned = [df.reindex(common_idx).interpolate() for df in per_iter_power]
        mean_power = np.mean([df.values for df in aligned], axis=0).flatten()
        all_iter_mean.append((common_idx, mean_power))

    all_velocities = sorted(set().union(*[vel for vel, _ in all_iter_mean]))
    aligned_powers = [interp1d(vel, power, kind='linear', bounds_error=False, fill_value='extrapolate')(all_velocities) for vel, power in all_iter_mean]
    aligned_powers = np.array(aligned_powers)
    min_power = aligned_powers.min(axis=0)
    mean_power = aligned_powers.mean(axis=0)
    max_power = aligned_powers.max(axis=0)

    # Plot on current axes
    plt.fill_between(all_velocities, min_power, max_power, color='#00BFFF', alpha=0.3, label='Range')
    plt.plot(all_velocities, mean_power, color='#FF4500', linewidth=2, label='Mean')
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Power (W)')
    # leave title to __main__
    plt.legend()


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    plt.sca(axes[0])
    power_V()
    axes[0].set_title('Baseline: Mean & Range')

    plt.sca(axes[1])
    power_V_sensitivity(n_iters=5, variation_pct=0.10, random_seed=42)
    axes[1].set_title('Sensitivity: 5 runs ±10%')

    plt.tight_layout()
    plt.show()

