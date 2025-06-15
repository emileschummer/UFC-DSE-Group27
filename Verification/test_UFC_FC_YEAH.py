import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest as pt
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import *

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

V=10
rho=1.225  # Density of air at sea level in kg/m^3
h= 0

# UNIT 03
expected_CD= 0.000141103
def test_flat_plate_drag_coefficient():

    result= flat_plate_drag_coefficient(V, rho, h, S_wing, L_blade, w_blade)

    assert pt.approx(result, rel=1e-6) == expected_CD

#UNIT 04
expected_CD_cube = 0.008426384
def test_cube_drag_coefficient():

    result= cube_drag_coefficient(V, rho, h, S_wing, L_gimbal)

    assert pt.approx(result, rel=1e-6) == expected_CD_cube


# UNIT 05
expected_CD_fus = 0.004261856
def test_fuselage_drag_coefficient():

    Cf_fus = flat_plate_drag_coefficient(V, rho, h, S_wing, L_fus, w_fus)
    result = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d, S_wing)
    
    assert pt.approx(result, rel=1e-6) == expected_CD_fus