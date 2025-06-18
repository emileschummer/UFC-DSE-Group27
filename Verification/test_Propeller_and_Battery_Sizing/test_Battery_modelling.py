import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest as pt
import pandas as pd
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import *
from Final_UAV_Sizing.Input.fixed_input_values import *
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.Battery_modelling import *

import numpy as np
import pandas as pd
from unittest.mock import patch
import shutil
W = 250
aero_df = pd.read_csv(aero_csv)
vert_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv"
hor_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv"
df_vertical = pd.read_csv(vert_folder)
df_vertical['Thrust_N'] = df_vertical[' Thrust (g) '] * 9.81 / 1000
df_horizontal = pd.read_csv(hor_folder)
df_horizontal['Thrust_N'] = df_horizontal[' Thrust (g) '] * 9.81 / 1000

calculate_power = calculate_power_FC
race_data = pd.DataFrame({
        " distance": [0, 10],
        " time": [0, 1],
        " velocity_smooth": [0, 10],
        " grade_smooth": [0, 5],
        " altitude": [0, 10]
    })

# BM 01
def test_simulate_1_battery():

    outcome= simulate_1_battery(df_vertical,df_horizontal,race_data, calculate_power, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,PL_power,L_fus,L_n,L_c,L_blade,L_stab, d_fus, w_fus, w_blade, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker)

    assert len(outcome[1]) == 2
    assert outcome[2][0] == PL_power + (calculate_power_FC(df_vertical,df_horizontal,0,0,0, 0, 0, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, d_fus, w_fus, L_blade, w_blade, L_stab, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker))
    assert all([p >= 0 for p in outcome[2]])
    P = outcome[2][1]
    expected_energy_Wh = (1 * P) / 3600
    assert np.isclose(outcome[8][1], expected_energy_Wh, rtol=1e-6)

#BM 02
distance_plot = [0, 30, 100]
gradient_plot = [0, 3, 9]
altitude_plot = [0, 30, 90]

d = 65
frac = (65 - 30) / (100 - 30)
expected_gradient = 3 + frac * (9 - 3)
expected_altitude = 30 + frac * (90 - 30)

def test_get_gradient_and_altitude_at_distance():
    gradient, altitude = get_gradient_and_altitude_at_distance(d, distance_plot, gradient_plot, altitude_plot)

    assert pt.approx(gradient, rel=1e-6) == expected_gradient
    assert pt.approx(altitude, rel=1e-6) == expected_altitude

#BM 03
def dummy_input_folders(tmp_path):
    # Create input folders
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"
    data_folder = tmp_path / "RaceData"
    input_folder.mkdir()
    output_folder.mkdir()
    data_folder.mkdir()

    # Copy the existing vertical and horizontal CSV files
    shutil.copy2(vert_folder, input_folder / "UAV_Propellers_and_Motor_Specs_Vertical.csv")
    shutil.copy2(hor_folder, input_folder / "UAV_Propellers_and_Motor_Specs_Horizontal.csv")

    # Create dummy race data
    race_df = pd.DataFrame({
        " distance": np.linspace(0, 100, 10),
        " time": np.linspace(0, 90, 10),
        " velocity_smooth": np.linspace(0, 10, 10),
        " grade_smooth": np.linspace(0, 5, 10),
        " altitude": np.linspace(0, 100, 10)
    })
    race_df.to_csv(data_folder / "race1.csv", index=False)

    return str(input_folder), str(output_folder), aero_df, str(data_folder)


def test_Battery_Model(tmp_path):
    input_folder, output_folder, aero_df, data_folder = dummy_input_folders(tmp_path)

    max_energy = Battery_Model(
        input_folder=input_folder,
        output_folder=output_folder,
        aero_df=aero_df,
        data_folder=data_folder,
        number_relay_stations=1,
        show=False,
        show_all=False
    )

    assert isinstance(max_energy, float)
    assert max_energy > 0

#BM 4
def test_Battery_Size():
    max_battery_energy= 0
    expected_mass= 0
    expected_volume= 0
    battery_mass,battery_volume= Battery_Size(max_battery_energy, battery_safety_margin = 1.2, battery_energy_density = 450, battery_volumetric_density= 200)
    assert pt.approx(expected_mass, rel=1e-6) == battery_mass
    assert pt.approx(expected_volume, rel=1e-6) == battery_volume
