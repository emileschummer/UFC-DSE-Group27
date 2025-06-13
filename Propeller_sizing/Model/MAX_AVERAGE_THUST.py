import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pandas as pd
from Propeller_sizing.Model.UFC_FC_YEAH import *
import Propeller_sizing.Input.Strava_input_csv as sva
from statistics import mode, StatisticsError
W= 250
S_wing = 2
CLmax = 2
V_vert_prop = 11
numberengines_vertical = 4
numberengines_horizontal = 1
propeller_wake_efficiency = 0.7
L_blade = 0.7366
w_blade = 0.075
L_stab= 0.6
w_stab= 0.5
L_poles= 3.6*L_blade/2 + 0.5
w_poles= 0.34
L_motor = 0.3
L_gimbal = 0.12
L_speaker = 0.1

L_n = 0.2
L_c = 0.6
L_fus = 2*L_n + L_c
w_fus = S_wing / L_fus
d = 0.25

aero_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'aero.csv'))

races = sva.make_race_dictionnary()


for race_name, race_data in races.items():
    
    Tvertical_list= []
    Thorizontal_list = []
    acceleration_list = []
    CD_list = []
    t = 0
    prev_velocity = 0 
    prev_grade_smooth= 0 
    for index, row in race_data.iterrows():
        time = row[" time"]  
        velocity_smooth = row[" velocity_smooth"]
        grade_smooth = np.arctan(row[" grade_smooth"] / 100)
        altitude = row[" altitude"]
        rho = sva.air_density_isa(altitude)
        Cf_blade= flat_plate_drag_coefficient(velocity_smooth, rho, altitude, S_wing, L_blade, w_blade)
        Cf_stab = flat_plate_drag_coefficient(velocity_smooth, rho, altitude,S_wing,L_stab, w_stab)
        Cf_poles = flat_plate_drag_coefficient(velocity_smooth, rho, altitude, S_wing, L_poles, w_poles)
        Cf_fus = flat_plate_drag_coefficient(velocity_smooth, rho, altitude, S_wing, L_fus, w_fus)
        CD_speaker = cube_drag_coefficient(velocity_smooth, rho, altitude, S_wing, L_speaker)
        CD_gimbal = cube_drag_coefficient(velocity_smooth, rho, altitude, S_wing, L_gimbal)
        CD_motor = cube_drag_coefficient(velocity_smooth, rho, altitude, S_wing, L_motor)
        CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d, S_wing)

        
        # Calculate acceleration using current and previous velocity
        time_diff = time - t
        if t > 0:  # Skip first point
            acceleration = (velocity_smooth - prev_velocity) / time_diff
            pitch_rate = (grade_smooth - prev_grade_smooth) / time_diff
        else:
            acceleration = 0
            pitch_rate = 0
        acceleration_list.append(acceleration)
        prev_velocity = velocity_smooth
        prev_grade_smooth = grade_smooth
        t = time

        Tvertical, Thorizontal, CD = calculate_thrust_UFC_FC(grade_smooth, velocity_smooth, rho, acceleration, pitch_rate, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_gimbal, CD_speaker, CD_motor, Cf_blade, Cf_stab, Cf_poles)
        Tvertical_list.append(Tvertical)
        Thorizontal_list.append(Thorizontal)
        CD_list.append(CD)
    
    # Statistics calculations
    non_zero_vertical = [t for t in Tvertical_list if t != 0]
    non_negative_horizontal = [t for t in Thorizontal_list if t >= 0]
    print(f"\nRace: {race_name}")
    print(f"Maximum absolute vertical thrust: {max(abs(np.array(Tvertical_list))):.2f} N")
    print(f"Maximum absolute horizontal thrust: {max(abs(np.array(Thorizontal_list))):.2f} N")
    print(f"Average vertical thrust (excluding zeros): {sum(non_zero_vertical)/len(non_zero_vertical):.2f} N")
    print(f"Average horizontal thrust (excluding negative): {sum(non_negative_horizontal)/len(non_negative_horizontal):.2f} N")
    try:
        print(f"Most common vertical thrust value (excluding zeros): {mode(non_zero_vertical):.2f} N")
        print(f"Most common horizontal thrust value (excluding negative): {mode(Thorizontal_list):.2f} N")
    except StatisticsError:
        print("No unique mode found for thrust values")

    print(f"Average CD: {sum(CD_list)/len(CD_list):.6f}")
    
    # Create subplots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16), sharex=True)
    
    time_points = race_data[' time'].values
    
    # Plot horizontal thrust
    ax1.plot(time_points, Thorizontal_list, 'b-', label='Horizontal Thrust')
    ax1.set_ylabel('Thrust (N)')
    ax1.set_title(f'{race_name} - Time History')
    ax1.grid(True)
    ax1.legend()
    
    # Plot altitude
    ax2.plot(time_points, race_data[' grade_smooth'].values, 'g-', label='Gradient')
    ax2.set_ylabel('Gradient (%)')
    ax2.grid(True)
    ax2.legend()
    
    # Plot velocity
    ax3.plot(time_points, race_data[' velocity_smooth'].values, 'r-', label='Velocity')
    ax3.set_ylabel('Velocity (m/s)')
    ax3.grid(True)
    ax3.legend()
    
    # Plot acceleration
    ax4.plot(time_points, acceleration_list, 'm-', label='Acceleration')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Acceleration (m/s²)')
    ax4.grid(True)
    ax4.legend()
    
    plt.tight_layout()
    #plt.show()

'''
    # Create a new figure for velocity vs gradient plot
    plt.figure(figsize=(10, 6))

    # Create bins for gradient values
    gradient_bins = np.arange(-20, 21, 1)  # Adjust range as needed
    max_velocities = []
    bin_centers = []

    # Group data by gradient and find maximum velocity for each group
    for i in range(len(gradient_bins)-1):
        mask = (race_data[' grade_smooth'] >= gradient_bins[i]) & (race_data[' grade_smooth'] < gradient_bins[i+1])
        if mask.any():
            max_velocities.append(race_data[' velocity_smooth'][mask].max())
            bin_centers.append((gradient_bins[i] + gradient_bins[i+1]) / 2)

    # Plot maximum velocity vs gradient
    plt.plot(bin_centers, max_velocities, 'bo-')
    plt.xlabel('Gradient (%)')
    plt.ylabel('Maximum Velocity (m/s)')
    plt.title(f'{race_name} - Maximum Velocity vs Gradient')
    plt.grid(True)
    plt.show()
'''