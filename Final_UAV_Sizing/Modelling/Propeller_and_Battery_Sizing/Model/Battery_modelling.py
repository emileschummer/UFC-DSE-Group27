import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import matplotlib.pyplot as plt
from math import ceil
import os
from datetime import datetime
from Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import calculate_power_FC
from Input.RaceData import Strava_input_csv as sva
import numpy as np
import pandas as pd

def Battery_Model(input_folder,output_folder,aero_df,data_folder="Final_UAV_Sizing/Input/RaceData", V_vert_prop=5, W=250, CLmax=2.2, S_wing=1.5, numberengines_vertical=4, numberengines_horizontal=1, propeller_wake_efficiency=0.8, number_relay_stations=3, UAV_off_for_recharge_time_min =15,battery_recharge_time_min =5,PL_power = 189,  show=False,L_fus = 0.8,L_n = 0.2,L_c= 0.6,L_blade=0.7366,L_stab=0.6, d_fus = 0.25, w_fus = 2.5, w_blade = 0.075, w_stab = 0.5, L_poles = 1.5, w_poles = 0.34, L_motor = 0.3, L_gimbal = 0.12, L_speaker = 0.1):
    print("---------Plot Race Results---------")
    races = sva.make_race_dictionnary(data_folder)
    race_results = {}
    for race_name, race_data in races.items():
        necessary_battery_capacity = 0
        print(f"---------{race_name}---------")
        """ change this for power"""
        # Vertical Propeller 
        csv_path = os.path.join(input_folder,'UAV_Propellers_and_Motor_Specs_Vertical.csv')
        df_vertical = pd.read_csv(csv_path)
        df_vertical['Thrust_N'] = df_vertical[' Thrust (g) '] * 9.81 / 1000

        # Horizontal Propeller 
        csv_path = os.path.join(input_folder,'UAV_Propellers_and_Motor_Specs_Horizontal.csv')
        df_horizontal = pd.read_csv(csv_path)
        df_horizontal['Thrust_N'] = df_horizontal[' Thrust (g) '] * 9.81 / 1000

        calculate_power = calculate_power_FC
        # 1. Follow a cyclist with 1 battery, no relay station
        time_plot, distance_plot, power_plot, speed_plot, gradient_plot, acceleration_plot, pitch_rate_plot, rho_plot, battery_energy_plot, altitude_plot = simulate_1_battery(df_vertical,df_horizontal,race_data, calculate_power, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,PL_power,L_fus,L_n,L_c,L_blade,L_stab, d_fus, w_fus, w_blade, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker)
        
        # 2. Calculate battery capacity and threshold
        total_battery_energy = battery_energy_plot[-1]
        battery_usable_capacity = total_battery_energy / (number_relay_stations + 1)

        # 3. Simulate battery switches
        # We'll build new arrays as we go
        new_time, new_distance, new_power, new_speed = [], [], [], []
        new_gradient, new_acceleration, new_pitch_rate = [], [], []
        new_rho, new_altitude, new_battery_energy = [], [], []

        idx = 0
        last_battery_energy = 0
        n_switches = 0
        while n_switches < number_relay_stations and idx < len(time_plot):
            start_idx = idx
            # Find where battery_usable_capacity is reached
            battery_empty_idx = start_idx
            while battery_empty_idx < len(battery_energy_plot) and (battery_energy_plot[battery_empty_idx] - last_battery_energy) < battery_usable_capacity:
                battery_empty_idx += 1
            if battery_empty_idx >= len(time_plot):
                battery_empty_idx = len(time_plot) - 1
            reached_RS_idx = battery_empty_idx
            RS_location = distance_plot[reached_RS_idx]
            threshold_time_RS = time_plot[reached_RS_idx] - UAV_off_for_recharge_time_min*60 #time at which the drone needs to be at RS
            # Find the index in time_plot for which the value is closest to threshold_time_RS
            go_charge_idx = int(np.argmin(np.abs(np.array(time_plot) - threshold_time_RS)))
            #Find the cruise speed
            VCr = (distance_plot[reached_RS_idx] - distance_plot[go_charge_idx]) / ((time_plot[reached_RS_idx] - time_plot[go_charge_idx])-battery_recharge_time_min*60)
            if VCr < V_vert_prop:
               VCr = V_vert_prop
            # Copy up to threshold
            new_time.extend(time_plot[start_idx:go_charge_idx])
            new_distance.extend(distance_plot[start_idx:go_charge_idx])
            new_power.extend(power_plot[start_idx:go_charge_idx])
            new_speed.extend(speed_plot[start_idx:go_charge_idx])
            new_gradient.extend(gradient_plot[start_idx:go_charge_idx])
            new_acceleration.extend(acceleration_plot[start_idx:go_charge_idx])
            new_pitch_rate.extend(pitch_rate_plot[start_idx:go_charge_idx])
            new_rho.extend(rho_plot[start_idx:go_charge_idx])
            new_altitude.extend(altitude_plot[start_idx:go_charge_idx])
            # Energy offset for this segment
            for i in range(start_idx, go_charge_idx):
                new_battery_energy.append(battery_energy_plot[i] - last_battery_energy)
            
            # At threshold: fly ahead at VCr until battery_usable_capacity is reached
            go_charge_time = time_plot[go_charge_idx]
            go_charge_distance = distance_plot[go_charge_idx]
            go_charge_altitude = altitude_plot[go_charge_idx]
            go_charge_gradient = gradient_plot[go_charge_idx]
            go_charge_rho = rho_plot[go_charge_idx]
            go_charge_pitch = np.arctan(go_charge_gradient / 100)
            go_charge_energy = new_battery_energy[-1] if new_battery_energy else 0
            go_charge_prev_velocity = VCr
            go_charge_prev_pitch = go_charge_pitch
            go_charge_prev_time = go_charge_time
            """
            # Simulate flying ahead at VCr
            orig_times = np.array(time_plot[go_charge_idx:reached_RS_idx+1])
            orig_distances = np.array(distance_plot[go_charge_idx:reached_RS_idx+1])
            orig_gradients = np.array(gradient_plot[go_charge_idx:reached_RS_idx+1])
            orig_altitudes = np.array(altitude_plot[go_charge_idx:reached_RS_idx+1])
            num_points = len(orig_times)
            if num_points < 2:
                break
            new_distances = [fly_distance]
            for j in range(1, num_points):
                dt = orig_times[j] - orig_times[j-1]
                new_distances.append(new_distances[-1] + VCr * dt)
            new_distances = np.array(new_distances)
            new_gradients = np.interp(new_distances, orig_distances, orig_gradients)
            new_altitudes = np.interp(new_distances, orig_distances, orig_altitudes)
            """

            # Simulate power/energy for this segment
            distance = go_charge_distance
            previous_pitch = go_charge_prev_pitch
            energy = go_charge_energy
            for j in range(go_charge_idx, reached_RS_idx + 1):
                if new_distance[j-1] < RS_location:
                    time_now = time_plot[j]
                    dt = (time_now - time_plot[j-1])
                    velocity = VCr
                    distance += VCr * dt
                    gradient_for_plot, altitude = get_gradient_and_altitude_at_distance(distance, distance_plot, gradient_plot, altitude_plot)
                    gradient = np.arctan(gradient_for_plot / 100)  # Convert percentage to radians
                    rho = sva.air_density_isa(altitude)
                    acceleration = 0
                    pitch_rate = (gradient - previous_pitch) / dt
                    previous_pitch = pitch_rate
                    P = calculate_power(df_vertical,df_horizontal,gradient,velocity,rho, acceleration, pitch_rate, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, d_fus, w_fus, L_blade, w_blade, L_stab, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker)
                    P+= PL_power  # Add power for payload
                    energy +=  P*dt/3600  # Convert J to Wh
                else: 
                    time_now = time_plot[j]
                    dt = (time_now - time_plot[j-1])
                    velocity = 0
                    distance += 0
                    gradient_for_plot, altitude = get_gradient_and_altitude_at_distance(distance, distance_plot, gradient_plot, altitude_plot)
                    gradient = np.arctan(gradient_for_plot / 100)  # Convert percentage to radians
                    rho = sva.air_density_isa(altitude)
                    acceleration = 0
                    pitch_rate = 0
                    previous_pitch = 0
                    P = PL_power
                    energy +=  0
                new_time.append(time_now)
                new_distance.append(distance)
                new_power.append(P)
                new_speed.append(velocity)
                new_gradient.append(gradient_for_plot)
                new_acceleration.append(acceleration)
                new_pitch_rate.append(pitch_rate)
                new_rho.append(rho)
                new_altitude.append(altitude)
                new_battery_energy.append(energy)

            # Wait at recharge point (optional: can add a pause here if needed)
            # After battery change, reset battery_energy to zero (full battery)

            if new_battery_energy[-1] > necessary_battery_capacity:
                necessary_battery_capacity = new_battery_energy[-1]
            last_battery_energy = battery_energy_plot[battery_empty_idx]
            idx = battery_empty_idx + 1
            n_switches += 1

        # Copy the rest of the race after last battery switch
        if idx < len(time_plot):
            for i in range(idx, len(time_plot)):
                new_time.append(time_plot[i])
                new_distance.append(distance_plot[i])
                new_power.append(power_plot[i])
                new_speed.append(speed_plot[i])
                new_gradient.append(gradient_plot[i])
                new_acceleration.append(acceleration_plot[i])
                new_pitch_rate.append(pitch_rate_plot[i])
                new_rho.append(rho_plot[i])
                new_altitude.append(altitude_plot[i])
                new_battery_energy.append(battery_energy_plot[i] - last_battery_energy)
            if new_battery_energy[-1] > necessary_battery_capacity:
                necessary_battery_capacity = new_battery_energy[-1]
        
        print(necessary_battery_capacity, "Wh")
        race_results[race_name] = necessary_battery_capacity

        if show:
            # Plot original and new (with relay stations) on the same figure
            fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
            # Plot original
            plot(time_plot, power_plot, speed_plot, gradient_plot, battery_energy_plot,
                race_name + " (original)", V_vert_prop, battery_usable_capacity, axs=axs)
            # Plot new (with relay stations)
            plot(new_time, new_power, new_speed, new_gradient, new_battery_energy,
                race_name + " (relay stations)", V_vert_prop, battery_usable_capacity, multiple_RS=True, axs=axs)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_folder, f"Power_speed_gradient_energy_vs_time_{race_name.replace('.csv', '')}_{timestamp}.png")
            os.makedirs(output_folder, exist_ok=True)
            plt.tight_layout()
            plt.savefig(output_path)
            if show:
                print("Close plot to continue")
                plt.show()
            plt.close()
    print("\n\n------------------------------------------------------------------------------------\n")
    print("---------Summary--------------------------------------------------------------------\n")
    if race_results:
        max_race = max(race_results, key=race_results.get)
        max_battery_energy = race_results[max_race]
        print(f"Maximum battery capacity necessary: {max_battery_energy:.2f} Wh (Race: {max_race})\n")
        avg_battery_energy = sum(race_results.values()) / len(race_results)
        print(f"Average battery capacity necessary across all races: {avg_battery_energy:.2f} Wh\n")
    else:
        print("No race results available to determine maximum energy consumption.\n")
        max_race, max_battery_energy, avg_battery_energy = 0, 0, 0

    print("Done")
    return max_battery_energy

def simulate_1_battery(df_vertical,df_horizontal,race_data, calculate_power, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,PL_power,L_fus,L_n,L_c,L_blade,L_stab, d_fus, w_fus, w_blade, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker):
    # Prepare arrays
    time_plot, distance_plot, power_plot, speed_plot = [], [], [], []
    gradient_plot, acceleration_plot, pitch_rate_plot = [], [], []
    rho_plot, battery_energy_plot, altitude_plot = [], [], []
    t, prev_velocity, prev_grade_smooth, energy = 0, 0, 0, 0
    for index, row in race_data.iterrows():
            distance = row[" distance"]
            time = row[" time"]
            velocity_smooth = row[" velocity_smooth"]
            grade_smooth = np.arctan(row[" grade_smooth"] / 100)
            altitude = row[" altitude"]
            rho = sva.air_density_isa(altitude)
            time_diff = time - t
            if t > 0:
                acceleration = (velocity_smooth - prev_velocity) / time_diff
                pitch_rate = (grade_smooth - prev_grade_smooth) / time_diff
            else:
                acceleration = 0
                pitch_rate = 0
            prev_velocity = velocity_smooth
            prev_grade_smooth = grade_smooth
            P = calculate_power(df_vertical,df_horizontal,grade_smooth,velocity_smooth,rho, acceleration, pitch_rate, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, d_fus, w_fus, L_blade, w_blade, L_stab, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker)
            P+= PL_power  # Add power for payload
            energy += time_diff * P/3600  # Convert J to Wh
            t = time
            time_plot.append(time)
            distance_plot.append(distance)
            power_plot.append(P)
            speed_plot.append(velocity_smooth)
            gradient_plot.append(row[" grade_smooth"])
            acceleration_plot.append(acceleration)
            pitch_rate_plot.append(pitch_rate)
            rho_plot.append(rho)
            altitude_plot.append(altitude)
            battery_energy_plot.append(energy)
    return time_plot, distance_plot, power_plot, speed_plot, gradient_plot, acceleration_plot, pitch_rate_plot, rho_plot, battery_energy_plot, altitude_plot

def plot(time_plot, power_plot, speed_plot, gradient_plot, battery_energy_plot, race_name, V_vert_prop, battery_usable_capacity, axs=None,multiple_RS=False):
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True) if axs is None else (plt.gcf(), axs)
    if multiple_RS:
        label = 'Multiple Relay Stations'
        axs[0].plot(time_plot, power_plot, label=label)
        axs[1].plot(time_plot, speed_plot, label='UAV Speed', color='black')
        axs[2].plot(time_plot, gradient_plot, label='UAV Gradient', color='black')
        axs[3].plot(time_plot, (1 - battery_energy_plot/battery_usable_capacity)*100, label='UAV Battery Usage', color='blue')
        # Draw stall speed line in the velocity plot (axs[1])
        axs[1].axhline(V_vert_prop, color='red', linestyle='--', label='Stall Speed')
        axs[1].legend()
    else:
        label = 'Cyclists'
        axs[1].plot(time_plot, speed_plot, label='Cyclist Speed', color='grey')
        axs[2].plot(time_plot, gradient_plot, label='Cyclist Gradient ', color='grey')



    axs[0].set_title(f"Power vs Time for {race_name}")
    axs[0].set_ylabel("Power [W]")
    axs[0].legend()
    axs[0].grid()

    axs[1].set_title("Speed [m/s] vs Time")
    axs[1].set_ylabel("Speed [m/s]")
    axs[1].grid()

    axs[2].set_title("Gradient vs Time")
    axs[2].set_ylabel("Gradient [%]")
    axs[2].legend()
    axs[2].grid()

    axs[3].set_title("Battery Usage vs Time")
    axs[3].set_xlabel("Time [s]")
    axs[3].set_ylabel("Battery Energy [%]")
    axs[3].grid()



   


def get_gradient_and_altitude_at_distance(distance, distance_plot, gradient_plot, altitude_plot):
    """
    Returns the gradient and altitude at a given distance by interpolating between points.
    Assumes distance_plot is strictly increasing.
    """

    if distance <= distance_plot[0]:
        return gradient_plot[0], altitude_plot[0]
    if distance >= distance_plot[-1]:
        return gradient_plot[-1], altitude_plot[-1]

    idx = np.searchsorted(distance_plot, distance)
    d0, d1 = distance_plot[idx - 1], distance_plot[idx]
    g0, g1 = gradient_plot[idx - 1], gradient_plot[idx]
    a0, a1 = altitude_plot[idx - 1], altitude_plot[idx]
    # Linear interpolation
    frac = (distance - d0) / (d1 - d0)
    gradient = g0 + frac * (g1 - g0)
    altitude = a0 + frac * (a1 - a0)
    return gradient, altitude

def Battery_Size(max_battery_energy, battery_safety_margin = 1.2, battery_energy_density = 450, battery_volumetric_density= 200):
    battery_mass = max_battery_energy * battery_safety_margin / battery_energy_density  # in kg
    battery_volume = battery_mass / battery_volumetric_density  # in m^3
    return battery_mass,battery_volume