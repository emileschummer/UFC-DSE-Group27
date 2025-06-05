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

def Battery_Model(V_stall, W,D_rest,D_wing,L_wing,CLmax,alpha_T, N_blades, Chord_blade,CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal,eta_prop_vertical, propeller_wake_efficiency,number_relay_stations,battery_max_usage,VCr,output_folder, show=False):
    print("---------Plot Race Results---------")
    races = sva.make_race_dictionnary()
    race_results = {} #actual energy consumption in Wh
    race_results_7h = {} #energy consumption for a standardised 7h race in Wh
    for race_name, race_data in races.items():
        print(f"---------{race_name}---------")
        if show: 
            fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)  # Create subplots
            label = 'Yangda-style'
        race_plot = []
        calculate_power = calculate_power_UFC_FC
        energy = 0
        t = 0
        prev_velocity = 0 
        prev_grade_smooth = 0 
        time_plot = []
        distance_plot = []
        power_plot = []
        speed_plot = []
        gradient_plot = []
        acceleration_plot = []
        pitch_rate_plot = []
        rho_plot = []
        energy_plot = []
        altitude_plot = []
        for index, row in race_data.iterrows():
            distance = row[" distance"]
            time = row[" time"]  
            velocity_smooth = row[" velocity_smooth"]
            grade_smooth = np.arctan(row[" grade_smooth"] / 100)
            altitude = row[" altitude"]
            rho = sva.air_density_isa(altitude)
            
            # Calculate acceleration using current and previous velocity
            time_diff = time - t
            if t > 0:  # Skip first point
                acceleration = (velocity_smooth - prev_velocity) / time_diff
                pitch_rate = (grade_smooth - prev_grade_smooth) / time_diff  # Calculate pitch rate
            else:
                acceleration = 0
                pitch_rate = 0
            prev_velocity = velocity_smooth  # Store current velocity for next iteration
            prev_grade_smooth = grade_smooth  # Store current grade for next iteration

            P = calculate_power(grade_smooth, velocity_smooth, V_stall, rho, W, acceleration, pitch_rate, D_rest, D_wing, L_wing, CLmax, alpha_T, N_blades, Chord_blade, CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal, eta_prop_vertical, propeller_wake_efficiency)
            energy = energy + time_diff * P
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
            energy_plot.append(energy / 3600)  # Convert energy to Wh

        battery_capacity = energy / number_relay_stations
        battery_threshold = battery_capacity * battery_max_usage  # 20% of the battery capacity
        index_recharge_go = None
        index_battery_empty = None
        # Find the indices where the UAV should start racing ahead and where it would have run out of battery
        for i in range(len(energy_plot)):
            if index_recharge_go is None and energy_plot[i] > battery_threshold:
                index_recharge_go = i
            if index_battery_empty is None and energy_plot[i] > battery_capacity:
                index_battery_empty = i
            if index_recharge_go is not None and index_battery_empty is not None:
                print(time_plot[index_battery_empty])
                break  # Stop if both indices are found
        
        if index_recharge_go is not None and index_battery_empty is not None:
            # --- Race ahead ---
            # Set cruise speed (e.g., VCr) and recalculate the power for the segment
            cruise_speed = VCr
            # Calculate the distance to cover while racing ahead
            distance_start = distance_plot[index_recharge_go]
            distance_end = distance_plot[index_battery_empty]
            # Use the original time steps for the segment
            orig_times = np.array(time_plot[index_recharge_go:index_battery_empty+1])
            orig_distances = np.array(distance_plot[index_recharge_go:index_battery_empty+1])
            orig_gradients = np.array(gradient_plot[index_recharge_go:index_battery_empty+1])
            orig_altitudes = np.array(altitude_plot[index_recharge_go:index_battery_empty+1])

            # Interpolate distances, gradients, and altitudes to match original time steps
            num_points = len(orig_times)
            # Calculate new distances at cruise speed, starting from distance_start
            new_distances = [distance_start]
            for j in range(1, num_points):
                dt = orig_times[j] - orig_times[j-1]
                new_distances.append(new_distances[-1] + cruise_speed * dt)
            new_distances = np.array(new_distances)
            # Interpolate gradient and altitude for new points
            new_gradients = np.interp(new_distances, orig_distances, orig_gradients)
            new_altitudes = np.interp(new_distances, orig_distances, orig_altitudes)

            # Calculate new power and energy for racing ahead, using original time steps
            new_power_plot = []
            new_speed_plot = []
            new_acceleration_plot = []
            new_pitch_rate_plot = []
            new_rho_plot = []
            new_energy_plot = []
            prev_velocity = cruise_speed
            prev_grade = np.arctan(new_gradients[0] / 100)
            prev_time = orig_times[0]
            energy_ahead = energy_plot[index_recharge_go] * 3600  # convert back to Joules

            for j in range(num_points):
                velocity = cruise_speed
                grade = np.arctan(new_gradients[j] / 100)
                altitude = new_altitudes[j]
                rho = sva.air_density_isa(altitude)
                time_now = orig_times[j]
                if j == 0:
                    acceleration = 0
                    pitch_rate = 0
                else:
                    dt = time_now - prev_time
                    acceleration = (velocity - prev_velocity) / dt
                    pitch_rate = (grade - prev_grade) / dt
                P = calculate_power(grade, velocity, V_stall, rho, W, acceleration, pitch_rate, D_rest, D_wing, L_wing, CLmax, alpha_T, N_blades, Chord_blade, CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal, eta_prop_vertical, propeller_wake_efficiency)
                energy_ahead += (time_now - prev_time) * P if j > 0 else 0
                new_power_plot.append(P)
                new_speed_plot.append(velocity)
                new_acceleration_plot.append(acceleration)
                new_pitch_rate_plot.append(pitch_rate)
                new_rho_plot.append(rho)
                new_energy_plot.append(energy_ahead / 3600)
                prev_velocity = velocity
                prev_grade = grade
                prev_time = time_now

            # Overwrite the plot lists for the race ahead segment
            time_plot[index_recharge_go:index_battery_empty+1] = list(orig_times)
            distance_plot[index_recharge_go:index_battery_empty+1] = list(new_distances)
            power_plot[index_recharge_go:index_battery_empty+1] = new_power_plot
            speed_plot[index_recharge_go:index_battery_empty+1] = new_speed_plot
            gradient_plot[index_recharge_go:index_battery_empty+1] = list(new_gradients)
            acceleration_plot[index_recharge_go:index_battery_empty+1] = new_acceleration_plot
            pitch_rate_plot[index_recharge_go:index_battery_empty+1] = new_pitch_rate_plot
            rho_plot[index_recharge_go:index_battery_empty+1] = new_rho_plot
            altitude_plot[index_recharge_go:index_battery_empty+1] = list(new_altitudes)
            energy_plot[index_recharge_go:index_battery_empty+1] = new_energy_plot

            # --- Wait at recharge point ---
            # Find the time when the cyclist reaches the distance_end
            # This is the original time at index_battery_empty
            wait_end_time = time_plot[index_battery_empty]
            # Find the next index after index_battery_empty where the cyclist's distance >= distance_end
            for k in range(index_battery_empty, len(distance_plot)):
                if distance_plot[k] >= distance_end:
                    wait_end_time = time_plot[k]
                    break
            wait_duration = wait_end_time - orig_times[-1]
            if wait_duration > 0:
                # Insert a waiting segment: constant distance, zero power, zero speed, etc.
                time_plot.insert(index_battery_empty+1, orig_times[-1] + wait_duration)
                distance_plot.insert(index_battery_empty+1, distance_end)
                power_plot.insert(index_battery_empty+1, 0)
                speed_plot.insert(index_battery_empty+1, 0)
                gradient_plot.insert(index_battery_empty+1, gradient_plot[index_battery_empty])
                acceleration_plot.insert(index_battery_empty+1, 0)
                pitch_rate_plot.insert(index_battery_empty+1, 0)
                rho_plot.insert(index_battery_empty+1, rho_plot[index_battery_empty])
                altitude_plot.insert(index_battery_empty+1, altitude_plot[index_battery_empty])
                energy_plot.insert(index_battery_empty+1, energy_plot[index_battery_empty])

            # --- Resume following the cyclist with full battery ---
            # From wait_end_time onward, reset energy to zero (full battery)
            for m in range(index_battery_empty+1, len(energy_plot)):
                energy_plot[m] = energy_plot[m] - energy_plot[index_battery_empty+1]

        # If no recharge event, do nothing (default behavior)
        race_plot.append([time_plot, power_plot])
        race_results[race_name] = energy
        #race_results_7h[race_name] = energy / race_data[" time"].max() * 7 * 3600  # Store energy in Wh and max time

        if show: 
            axs[0].plot(time_plot, power_plot, label=label)  # Plot power vs time in the first subplot
            # Highlight regions where speed > V_stall m/s
            for j in range(len(speed_plot) - 1):
                if speed_plot[j] < V_stall:
                    axs[0].axvspan(time_plot[j], time_plot[j + 1], color='red', alpha=0.2)
            axs[1].plot(time_plot, speed_plot, label='Speed', color='black')  # Plot speed vs time
            axs[2].plot(time_plot, gradient_plot, label='Gradient', color='grey')  # Plot gradient vs time

            # Set titles and labels for subplots
            axs[0].set_title(f"Power vs Time for {race_name}")
            axs[0].set_ylabel("Power (W)")
            axs[0].legend()
            axs[0].grid()

            axs[1].set_title("Speed vs Time")
            axs[1].set_ylabel("Speed (m/s)")
            axs[1].legend()
            axs[1].grid()

            axs[2].set_title("Gradient vs Time")
            axs[2].set_xlabel("Time (s)")
            axs[2].set_ylabel("Gradient (%)")
            axs[2].legend()
            axs[2].grid()

            # Save the figure
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_folder, f"Power_speed_gradient_vs_time_{race_name.replace('.csv', '')}_{timestamp}.png")
            os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists
            plt.tight_layout()
            plt.savefig(output_path)
            if show:  
                print("Close plot to continue")
                plt.show()
            plt.close()
    print("\n\n------------------------------------------------------------------------------------\n")
    print("---------Summary--------------------------------------------------------------------\n")
    if race_results:
        max_race = max(race_results_7h, key=race_results_7h.get)
        max_energy = race_results_7h[max_race]
        print(f"Maximum energy consumption: {max_energy:.2f} Wh (Race: {max_race})\n")
        avg_energy = sum(race_results_7h.values()) / len(race_results_7h)
        print(f"Average energy consumption across all races: {avg_energy:.2f} Wh\n")
    else:
        print("No race results available to determine maximum energy consumption.\n")
        max_race, max_energy, avg_energy = 0,0,0

    print("Done")
    return race_results

"""       
        battery_capacity = race_results[race_name] / number_relay_stations

        battery_threshold = battery_capacity * battery_max_usage  # 20% of the battery capacity
        teamA = True  # Assuming teamA is a boolean variable indicating if the team is A
        if teamA:
            index_recharge_go = None
            index_battery_empty = None
            for i in range(len(energy_plot)):
                if index_recharge_go is None and energy_plot[i] > battery_threshold:
                    index_recharge_go = i
                if index_battery_empty is None and energy_plot[i] > battery_capacity:
                    index_battery_empty = i
                if index_recharge_go is not None and index_battery_empty is not None:
                    break  # Stop if both indices are found
            #Change values to go recharge    
            for i in range(index_recharge_go, index_battery_empty):
                #UAV speeds ahead at Recharing_Cyclist_Speed_Multiplier times the cyclist speed to recharge point
                if distance_plot[i-1] < distance_plot[index_battery_empty]: 
                    
                    
                        # Calculate acceleration using current and previous velocity
                    time_diff = time_plot - time_plot[i-1]
                    if time_plot[i] > 0:  # Skip first point
                        acceleration = (speed_plot[i] - speed_plot[i-1]) / time_diff* Recharing_Cyclist_Speed_Multiplier
                        pitch_rate = (gradient_plot[i] - gradient_plot[i-1]) / time_diff  # Calculate pitch rate
                    else:
                        acceleration = 0
                        pitch_rate = 0
                    P = calculate_power(gradient_plot[i],speed_plot[i]*Recharing_Cyclist_Speed_Multiplier,V_stall,rho[i], W, acceleration, pitch_rate,D_rest,D_wing,L_wing,CLmax,alpha_T, N_blades, Chord_blade,CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal,eta_prop_vertical, propeller_wake_efficiency)
                    energy = energy_plot[i-1] + time_diff * P

                    distance_plot[i] = distance_plot[i-1] + speed_plot[i] * time_diff * Recharing_Cyclist_Speed_Multiplier
                    power_plot[i] = P
                    speed_plot[i] = speed_plot[i] * Recharing_Cyclist_Speed_Multiplier
                    gradient_plot.append(row[" grade_smooth"])
                    acceleration_plot[i] = acceleration
                    pitch_rate_plot[i] = pitch_rate
                    energy_plot[i]=energy / 3600  # Convert energy to Wh
                    
                    
                #UAV is at recharge point
                else: 

"""