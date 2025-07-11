import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
import pandas as pd
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import *
import Final_UAV_Sizing.Input.RaceData.Strava_input_csv as sva
from statistics import mode, StatisticsError
from Final_UAV_Sizing.Input.fixed_input_values import *
W= 25*g
aero_df = pd.read_csv(aero_csv)

races = sva.make_race_dictionnary('Final_UAV_Sizing/Input/PropRaceData')
df_vertical = pd.read_csv('Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv')
df_vertical['Thrust_N']= df_vertical[' Thrust (g) '] * g /1000
df_horizontal = pd.read_csv('Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv')
df_horizontal['Thrust_N']= df_horizontal[' Thrust (g) '] * g /1000

def analyze_race_thrust():
    
    for race_name, race_data in races.items():
        Tvertical_list = []
        Thorizontal_list = []
        acceleration_list = []
        CD_list = []
        t = 0
        prev_velocity = 0 
        prev_grade_smooth = 0 
        
        for index, row in race_data.iterrows():
            time = row[" time"]  
            V = row[" velocity_smooth"]
            incline = np.arctan(row[" grade_smooth"] / 100)
            altitude = row[" altitude"]
            rho = sva.air_density_isa(altitude)
            
            # Calculate drag coefficients
            CD_blade= flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_blade, w_blade)
            CD_poles = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_poles, w_poles)
            Cf_fus = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_fus, w_fus)
            CD_speaker = cube_drag_coefficient(V, rho, altitude, S_wing, L_speaker)
            CD_gimbal = cube_drag_coefficient(V, rho, altitude, S_wing, L_gimbal)
            CD_motor = cube_drag_coefficient(V, rho, altitude, S_wing, L_motor)
            CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)
            Cf_wing = flat_plate_drag_coefficient(V, rho, altitude, S_wing, MAC, b)
            Cf_hor = flat_plate_drag_coefficient(V, rho, altitude, S_wing, tail_chord, tail_span)
            CD_ver = flat_plate_drag_coefficient(V, rho, altitude, S_wing, tail_chord_v, tail_span_v)
            
            # Calculate acceleration
            time_diff = time - t
            if t > 0:
                acceleration = (V - prev_velocity) / time_diff
                pitch_rate = (incline - prev_grade_smooth) / time_diff
            else:
                acceleration = 0
                pitch_rate = 0
            
            acceleration_list.append(acceleration)
            prev_velocity = V
            prev_grade_smooth = incline
            t = time
            
            # Calculate thrust
            Tvertical, Thorizontal, CD = calculate_thrust_UFC_FC(incline,V,rho, acceleration, pitch_rate, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_gimbal, CD_speaker, CD_motor, CD_blade, Cf_hor, CD_poles, Cf_wing, CD_ver)
            
            Tvertical_list.append(Tvertical)
            Thorizontal_list.append(Thorizontal)
            CD_list.append(CD)
            
        # Print statistics
        print(f"\nRace: {race_name}")
        print(f"Maximum absolute vertical thrust: {max(abs(np.array(Tvertical_list))):.2f} N")
        print(f"Maximum absolute horizontal thrust: {max(abs(np.array(Thorizontal_list))):.2f} N")
        print(f"Average vertical thrust: {sum(Tvertical_list)/len(Tvertical_list):.2f} N")
        print(f"Average horizontal thrust: {sum(Thorizontal_list)/len(Thorizontal_list):.2f} N")
        vertical_q75 = np.percentile(np.abs(Tvertical_list), 75)
        horizontal_q75 = np.percentile(np.abs(Thorizontal_list), 75)
        print(f"75th percentile vertical thrust: {vertical_q75:.2f} N")
        print(f"75th percentile horizontal thrust: {horizontal_q75:.2f} N")
        print(f"Average CD: {sum(CD_list)/len(CD_list):.6f}")
        
        # Plot results
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16), sharex=True)
        time_points = race_data[' time'].values
        
        ax1.plot(time_points, Thorizontal_list, 'b-', label='Horizontal Thrust')
        ax1.set_ylabel('Thrust (N)')
        ax1.set_title(f'{race_name} - Time History')
        ax1.grid(True)
        ax1.legend()
        
        ax2.plot(time_points, race_data[' grade_smooth'].values, 'g-', label='Gradient')
        ax2.set_ylabel('Gradient (%)')
        ax2.grid(True)
        ax2.legend()
        
        ax3.plot(time_points, race_data[' velocity_smooth'].values, 'r-', label='Velocity')
        ax3.set_ylabel('Velocity (m/s)')
        ax3.grid(True)
        ax3.legend()
        
        ax4.plot(time_points, race_data[' altitude'], 'm-', label='Altitude')
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Altitude (m)')
        ax4.grid(True)
        ax4.legend()
        
        plt.tight_layout()
        plt.show()
print(analyze_race_thrust())