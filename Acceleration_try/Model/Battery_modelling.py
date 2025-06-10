import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import matplotlib.pyplot as plt
from math import ceil
import os
from datetime import datetime
from Acceleration_try.Model.UFC_FC_Battery_Model import *
from Acceleration_try.Input import Strava_input_csv as sva

def Battery_Model(output_folder, V_vert_prop=10, W=250, D_rest=50, CLmax=2.2, S_wing=1.5, piAe=20.41, CD0_wing=0.0264, alpha_T=0.2, N_blades=2, Chord_blade=0.02, CD_blade=0.014, omega=300, r_prop_vertical=0.07, numberengines_vertical=4, numberengines_horizontal=1, eta_prop_horizontal=0.8, eta_prop_vertical=0.8, propeller_wake_efficiency=0.8, number_relay_stations=3, battery_max_usage=0.8, VCr=15, show=False):
    print("---------Plot Race Results---------")
    races = sva.make_race_dictionnary()
    race_results = {}
    for race_name, race_data in races.items():
        print(f"---------{race_name}---------")
        calculate_power = calculate_power_UFC_FC
        # Prepare arrays
        time_plot, distance_plot, power_plot, speed_plot = [], [], [], []
        gradient_plot, acceleration_plot, pitch_rate_plot = [], [], []
        rho_plot, energy_plot, altitude_plot = [], [], []
        t, prev_velocity, prev_grade_smooth, energy = 0, 0, 0, 0

        # 1. Simulate following the cyclist for the whole race
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
            P = calculate_power(grade_smooth, velocity_smooth, rho, V_vert_prop, W, acceleration, pitch_rate, D_rest, CLmax, S_wing, piAe, CD0_wing, alpha_T, N_blades, Chord_blade, CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal, eta_prop_vertical, propeller_wake_efficiency)
            energy += time_diff * P
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
            energy_plot.append(energy)

        # 2. Calculate battery capacity and threshold
        total_energy = energy_plot[-1]
        battery_usable_capacity = total_energy / (number_relay_stations + 1)
        battery_threshold = battery_usable_capacity * battery_max_usage
        battery_limits = [battery_usable_capacity, battery_threshold]

        # 3. Simulate battery switches
        # We'll build new arrays as we go
        new_time, new_distance, new_power, new_speed = [], [], [], []
        new_gradient, new_acceleration, new_pitch_rate = [], [], []
        new_rho, new_altitude, new_energy = [], [], []

        idx = 0
        last_energy = 0
        n_switches = 0
        while n_switches < number_relay_stations and idx < len(time_plot):
            # Find next index where battery_threshold is reached
            start_idx = idx
            while idx < len(energy_plot) and (energy_plot[idx] - last_energy) < battery_threshold:
                idx += 1
            if idx >= len(time_plot):
                # No more switches needed
                break

            # Copy up to threshold
            new_time.extend(time_plot[start_idx:idx])
            new_distance.extend(distance_plot[start_idx:idx])
            new_power.extend(power_plot[start_idx:idx])
            new_speed.extend(speed_plot[start_idx:idx])
            new_gradient.extend(gradient_plot[start_idx:idx])
            new_acceleration.extend(acceleration_plot[start_idx:idx])
            new_pitch_rate.extend(pitch_rate_plot[start_idx:idx])
            new_rho.extend(rho_plot[start_idx:idx])
            new_altitude.extend(altitude_plot[start_idx:idx])
            # Energy offset for this segment
            if len(new_energy) == 0:
                energy_offset = 0
            else:
                energy_offset = new_energy[-1]
            for i in range(start_idx, idx):
                new_energy.append(energy_plot[i] - last_energy + energy_offset)

            # At threshold: fly ahead at VCr until battery_usable_capacity is reached
            fly_start_idx = idx
            fly_energy = 0  # Reset energy to 0 for new battery
            fly_time = time_plot[fly_start_idx]
            fly_distance = distance_plot[fly_start_idx]
            fly_altitude = altitude_plot[fly_start_idx]
            fly_gradient = gradient_plot[fly_start_idx]
            fly_rho = rho_plot[fly_start_idx]
            fly_pitch = np.arctan(fly_gradient / 100)
            fly_prev_velocity = VCr
            fly_prev_pitch = fly_pitch
            fly_prev_time = fly_time

            # Find where battery_usable_capacity is reached
            fly_idx = fly_start_idx
            while fly_idx < len(energy_plot) and (energy_plot[fly_idx] - last_energy) < battery_usable_capacity:
                fly_idx += 1
            if fly_idx >= len(time_plot):
                fly_idx = len(time_plot) - 1

            # Simulate flying ahead at VCr
            orig_times = np.array(time_plot[fly_start_idx:fly_idx+1])
            orig_distances = np.array(distance_plot[fly_start_idx:fly_idx+1])
            orig_gradients = np.array(gradient_plot[fly_start_idx:fly_idx+1])
            orig_altitudes = np.array(altitude_plot[fly_start_idx:fly_idx+1])
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

            # Simulate power/energy for this segment
            for j in range(num_points):
                velocity = VCr
                grade = np.arctan(new_gradients[j] / 100)
                altitude = new_altitudes[j]
                rho = sva.air_density_isa(altitude)
                time_now = orig_times[j]
                if j == 0:
                    acceleration = 0
                    pitch_rate = 0
                else:
                    dt = time_now - orig_times[j-1]
                    acceleration = 0
                    pitch_rate = (grade - fly_prev_pitch) / dt
                P = calculate_power(grade, velocity, rho, V_vert_prop, W, acceleration, pitch_rate, D_rest, CLmax, S_wing, piAe, CD0_wing, alpha_T, N_blades, Chord_blade, CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal, eta_prop_vertical, propeller_wake_efficiency)
                if j == 0:
                    fly_energy_now = 0  # Reset to 0 at battery change
                else:
                    fly_energy_now += (time_now - orig_times[j-1]) * P
                new_time.append(time_now)
                new_distance.append(new_distances[j])
                new_power.append(P)
                new_speed.append(velocity)
                new_gradient.append(new_gradients[j])
                new_acceleration.append(acceleration)
                new_pitch_rate.append(pitch_rate)
                new_rho.append(rho)
                new_altitude.append(altitude)
                new_energy.append(fly_energy_now)
                fly_prev_pitch = grade

            # Wait at recharge point (optional: can add a pause here if needed)
            # After battery change, reset energy to zero (full battery)
            last_energy = energy_plot[fly_idx]
            idx = fly_idx + 1
            n_switches += 1

        # Copy the rest of the race after last battery switch
        if idx < len(time_plot):
            energy_offset = new_energy[-1] if new_energy else 0
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
                new_energy.append(energy_plot[i] - last_energy + energy_offset)

        race_results[race_name] = sum(new_energy) if new_energy else 0

        if show:
            plot(new_time, new_power, new_speed, new_gradient, new_energy, race_name, V_vert_prop, output_folder, show, battery_limits)
    print("\n\n------------------------------------------------------------------------------------\n")
    print("---------Summary--------------------------------------------------------------------\n")
    print(race_results)
    if race_results:
        max_race = max(race_results, key=race_results.get)
        max_energy = race_results[max_race]
        print(f"Maximum energy consumption: {max_energy:.2f} J (Race: {max_race})\n")
        avg_energy = sum(race_results.values()) / len(race_results)
        print(f"Average energy consumption across all races: {avg_energy:.2f} J\n")
    else:
        print("No race results available to determine maximum energy consumption.\n")
        max_race, max_energy, avg_energy = 0, 0, 0

    print("Done")
    return race_results

def plot(time_plot, power_plot, speed_plot, gradient_plot, energy_plot, race_name, V_vert_prop, output_folder, show, battery_limits, axs=None):
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True) if axs is None else (plt.gcf(), axs)
    label = 'Yangda-style'

    axs[0].plot(time_plot, power_plot, label=label)
    for j in range(len(speed_plot) - 1):
        if speed_plot[j] < V_vert_prop:
            axs[0].axvspan(time_plot[j], time_plot[j + 1], color='red', alpha=0.2)
    axs[1].plot(time_plot, speed_plot, label='Speed', color='black')
    axs[2].plot(time_plot, gradient_plot, label='Gradient', color='grey')
    axs[3].plot(time_plot, energy_plot, label='Energy', color='blue')

    # Draw battery capacity and threshold lines
    battery_usable_capacity, battery_threshold = battery_limits
    axs[3].axhline(battery_usable_capacity, color='red', linestyle='--', label=f'Battery Capacity: {battery_usable_capacity:.0f} J')
    axs[3].axhline(battery_threshold, color='orange', linestyle='--', label=f'Battery Threshold: {battery_threshold:.0f} J')
    axs[3].legend()

    axs[0].set_title(f"Power vs Time for {race_name}")
    axs[0].set_ylabel("Power (W)")
    axs[0].legend()
    axs[0].grid()

    axs[1].set_title("Speed vs Time")
    axs[1].set_ylabel("Speed (m/s)")
    axs[1].legend()
    axs[1].grid()

    axs[2].set_title("Gradient vs Time")
    axs[2].set_ylabel("Gradient (%)")
    axs[2].legend()
    axs[2].grid()

    axs[3].set_title("Energy vs Time")
    axs[3].set_xlabel("Time (s)")
    axs[3].set_ylabel("Energy (J)")
    axs[3].grid()

    # Annotate battery lines
    axs[3].annotate(f'{battery_usable_capacity:.0f} J', xy=(time_plot[-1], battery_usable_capacity), 
                    xytext=(-80, 5), textcoords='offset points', color='red', va='bottom', ha='right',
                    arrowprops=dict(arrowstyle='->', color='red'))
    axs[3].annotate(f'{battery_threshold:.0f} J', xy=(time_plot[-1], battery_threshold), 
                    xytext=(-80, -15), textcoords='offset points', color='orange', va='top', ha='right',
                    arrowprops=dict(arrowstyle='->', color='orange'))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"Power_speed_gradient_energy_vs_time_{race_name.replace('.csv', '')}_{timestamp}.png")
    os.makedirs(output_folder, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    if show:
        print("Close plot to continue")
        plt.show()
    plt.close()