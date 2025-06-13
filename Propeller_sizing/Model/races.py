import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
from matplotlib import pyplot as plt
import Input.Config as config
from Model.UFC_FC_YEAH import *
import Input.Strava_input_csv as sva

def plot_race_results(output_folder="Output", show = False):
    print("---------Plot Race Results---------")
    races = sva.make_race_dictionnary()
    race_results = {}
    inputs = config.input_list_final
    for race_name, race_data in races.items():
        print(f"---------{race_name}---------")
        fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)  # Create subplots
        race_configurations_plot = []
        race_plot= []
        label= 'Yangda-style'
        calculate_power = calculate_power_UFC_FC
        energy = 0
        t = 0
        prev_velocity = 0 
        prev_grade_smooth= 0 
        time_plot = []
        power_plot = []
        speed_plot = []
        gradient_plot = []
        for index, row in race_data.iterrows():
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
            prev_velocity = velocity_smooth # Store current velocity for next iteration
            prev_grade_smooth = grade_smooth  # Store current grade for next iteration

            P = calculate_power(grade_smooth, velocity_smooth, rho, inputs, acceleration, pitch_rate)
            energy = energy + time_diff * P
            t = time
            time_plot.append(time)
            power_plot.append(P)
            speed_plot.append(velocity_smooth)
            gradient_plot.append(row[" grade_smooth"])
        race_plot.append([time_plot, power_plot])
        if race_name not in race_results:
            race_results[race_name] = [0] * 4
        race_results[race_name] = energy / 3600  # Store energy in Wh
        axs[0].plot(time_plot, power_plot, label=label)  # Plot power vs time in the first subplot

        # Highlight regions where speed > V_stall m/s
        V_stall = inputs[9] 
        for j in range(len(speed_plot) - 1):
            if speed_plot[j] > V_stall:
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
        plt.tight_layout()
        plt.savefig(output_path)
        if show:  
            print("Close plot to continue")
            plt.show()
        plt.close()
    print("Done")

def flat_race(folder):
    print("---------7h Flat Race at 50km/h---------")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(folder, f"flat_race_{timestamp}.txt")
    inputs = config.input_list_final
    with open(output_file, "w") as file:
        file.write("---------7h Flat Race at 50km/h---------\n")
        file.write("Fixed, defined design inputs\n")
        file.write(f"UFC-MMA-4 Yangda Energy (Wh): {calculate_power_UFC_FC(0, 50/3.6, 1.225, inputs, 0, 0) * 7}\n")
    print("Done")