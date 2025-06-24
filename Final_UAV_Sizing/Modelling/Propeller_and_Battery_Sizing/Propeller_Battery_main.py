import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from datetime import datetime
from Input import fixed_input_values as input

from Model.Battery_modelling import Battery_Model
from Model.UFC_FC_YEAH import calculate_thrust_UFC_FC, cube_drag_coefficient,fuselage_drag_coefficient,flat_plate_drag_coefficient

import pandas as pd




def main():
    #3. Battery Sizing
        print("--------------------------------------------------")
        print("Battery Sizing")
    #3.1 Battery Consumption Model
        ##Prepare Inputs
        input_folder = input.engine_input_folder
        output_folder = r'Final_UAV_Sizing\Output\Final_Runs\RS_2_Pick'
        aero_df = pd.read_csv("Final_UAV_Sizing/Output/Final_Runs/RS_2_Pick/Wing_Sizing/aero_specific_06_17.csv")
        data_folder = "Final_UAV_Sizing/Input/ExtraRaceData"
        V_vert_prop = input.V_stall*input.V_stall_safety_margin
        W = 23.43*input.g
        S_wing = 2.31757
        CLmax = aero_df.loc[aero_df["CL_corrected"].idxmax()]
        numberengines_vertical = input.numberengines_vertical
        numberengines_horizontal = input.numberengines_horizontal
        propeller_wake_efficiency = input.propeller_wake_efficiency
        number_relay_stations = 2
        UAV_off_for_recharge_time_min = input.UAV_off_for_recharge_time_min
        battery_recharge_time_min = input.battery_recharge_time_min
        PL_power = input.PL_power
        show = True
        show_all = False #Set to True to show all race plots
        L_n = input.L_n
        L_c = input.L_c
        L_fus = input.L_fus
        L_blade = input.L_blade
        L_stab = input.L_stab
        d_fus = input.d_fus
        w_fus = S_wing / input.L_fus
        w_blade = input.w_blade
        w_stab = input.w_stab
        L_poles = input.L_poles
        w_poles = input.w_poles
        L_motor =  input.L_motor
        L_gimbal =  input.L_gimbal
        L_speaker = input.L_speaker
        ##Run
        altitude = 1500
        V= 120/3.6
        rho=1.225
        incline = 0
        a = 0
        gamma_dot = 0
        Cf_blade= flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_blade, w_blade)
        Cf_stab = flat_plate_drag_coefficient(V, rho, altitude,S_wing,L_stab, w_stab)
        Cf_poles = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_poles, w_poles)
        Cf_fus = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_fus, w_fus)
        CD_speaker = cube_drag_coefficient(V, rho, altitude, S_wing, L_speaker)
        CD_gimbal = cube_drag_coefficient(V, rho, altitude, S_wing, L_gimbal)
        CD_motor = cube_drag_coefficient(V, rho, altitude, S_wing, L_motor)
        CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)
        print(calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_gimbal, CD_speaker, CD_motor, Cf_blade, Cf_stab, Cf_poles))
        #print(Battery_Model(input_folder,output_folder,aero_df,data_folder,V_vert_prop,W,CLmax,S_wing,numberengines_vertical,numberengines_horizontal,propeller_wake_efficiency,number_relay_stations,UAV_off_for_recharge_time_min,battery_recharge_time_min,PL_power,show,show_all,L_fus,L_n,L_c,L_blade,L_stab, d_fus, w_fus, w_blade, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker))

if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = f"battery_test"
    main()
