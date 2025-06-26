import sys
import os
import pandas as pd
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
from matplotlib import pyplot as plt

def make_race_dictionnary(data_folder = 0):
    races = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Location of main.py
    if data_folder == 0:
            data_folder = r"C:\Users\marco\Desktop\RaceData"
    if not os.path.exists(data_folder):
        print(f"Data folder {data_folder} does not exist.")
        return {}
    
    for file_name in os.listdir(data_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(data_folder, file_name)
            try:
                data = pd.read_csv(file_path)
                races[file_name] = data
            except Exception as e:
                print(f"Error processing file {file_name}: {e}") 
    return races

def air_density_isa(h):
    T0 = 288.15  # Sea level standard temperature (K)
    p0 = 101325  # Sea level standard pressure (Pa)
    L = -0.0065  # Temperature lapse rate (K/m)
    g = 9.80665  # Gravity (m/s^2)
    R = 287.058  # Specific gas constant for air (J/kg·K)

    T = T0 + L * h
    p = p0 * (T / T0) ** (-g / (L * R))
    rho = p / (R * T)

    return rho


def plot_race_velocities(output_folder="StravaFiles/Output", show=False, unit_ms=True, percentile_value_input=10, adjust_velocity=True):
    print("---------Plot Race Results---------")
    races = make_race_dictionnary('StravaFiles')
    all_adjusted_velocities = []
    percentile_value = 100 - percentile_value_input
    
    # Conversion factor from m/s to km/h
    MS_TO_KMH = 3.6
    
    for race_name, race_data in races.items():
        print(f"---------{race_name}---------")
        for index, row in race_data.iterrows():
            velocity_smooth = row[" velocity_smooth"]
            if adjust_velocity:
                grade_smooth = np.arctan(row[" grade_smooth"] / 100)
                altitude = row[" altitude"]
                rho = air_density_isa(altitude)
                # adjusted_velocity = velocity_smooth * np.sqrt(rho / np.cos(grade_smooth))
                adjusted_velocity = velocity_smooth
            else:
                adjusted_velocity = velocity_smooth
            
            # Convert to km/h if needed - do this for ALL data
            if not unit_ms:
                adjusted_velocity *= MS_TO_KMH
                
            all_adjusted_velocities.append(adjusted_velocity)
    
    if all_adjusted_velocities:
        max_velocity = max(all_adjusted_velocities)
        # Adjust bin size based on unit - km/h needs larger bins
        bin_size = 3.6 if not unit_ms else 1  # 3.6 km/h bins for km/h, 1 m/s bins for m/s
        max_bin = int(np.ceil(max_velocity / bin_size)) * bin_size
        bin_edges = np.arange(0, max_bin + bin_size, bin_size)
    else:
        print("No velocities found.")
        return
    
    bar_gap = 0.2  # Fraction of bin width to leave as whitespace between bars
    
    # Calculate the desired percentile
    percentile_velocity = np.percentile(all_adjusted_velocities, percentile_value)
    
    # Plot combined histogram for all races
    fig, ax = plt.subplots(figsize=(8, 5))
    counts, bins, patches = ax.hist(all_adjusted_velocities, bins=bin_edges, alpha=0.7, color='#00A6D6', density=False)
    total = np.sum(counts)
    bin_width = bins[1] - bins[0] if len(bins) > 1 else 1
    percentages = (counts / total) * 100 if total > 0 else counts
    
    ax.clear()
    bar_width = bin_width * (1 - bar_gap)
    bars = ax.bar(bins[:-1] + bar_width/2, percentages, width=bar_width, alpha=0.7, color='#00A6D6', align='center')
    
    title_unit = "m/s" if unit_ms else "km/h"
    ax.set_xlabel(f"{'Adjusted ' if adjust_velocity else ''}Velocity [{title_unit}]")
    ax.set_ylabel("Percentage of Time [%]")
    
    # Set reasonable x-axis ticks to avoid overlap
    if unit_ms:
        ax.set_xticks(bin_edges)
    else:
        # For km/h, use every 5th or 10th tick to avoid crowding
        tick_interval = 10 if max(bin_edges) > 50 else 5
        tick_positions = np.arange(0, max(bin_edges) + tick_interval, tick_interval)
        ax.set_xticks(tick_positions)
    
    ax.grid(True)
    
    # Plot the percentile line and annotate
    ax.axvline(percentile_velocity, color='red', linestyle='--', linewidth=2, 
               label=f"{percentile_value_input}th Percentile: {percentile_velocity:.2f} {title_unit}")
    
    # Find and highlight the bin with the most coverage
    if len(percentages) > 0:
        max_bin_idx = np.argmax(percentages)
        most_present_velocity = (bins[max_bin_idx] + bins[max_bin_idx + 1]) / 2
        bars[max_bin_idx].set_color('orange')
        ax.axvline(most_present_velocity, color='orange', linestyle='-', linewidth=2, 
                   label=f"Most Present: {most_present_velocity:.2f} {title_unit}")
    
    ax.legend()
    plt.tight_layout()
    plt.show()
    plt.close()
    print("Done")

if __name__ == "__main__":
    plot_race_velocities(unit_ms=False,percentile_value_input = 66,adjust_velocity=True)