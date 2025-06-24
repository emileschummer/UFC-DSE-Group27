import pytest as pt
from unittest.mock import patch, MagicMock 
import numpy as np
import pandas as pd
import types  
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from Final_UAV_Sizing.Modelling.Wing_Sizing.Airfoil import (
    setup_wing_and_airplane,
    calculate_section_properties_and_reynolds,
    generate_2d_stall_database,
    interpolate_stall_data_for_sections,
    run_vlm_sweep_with_stall_correction
)

mock_asb_global = MagicMock()


mock_asb_global.WingXSec = MagicMock(return_value=types.SimpleNamespace(chord=1, twist=0, airfoil=None, xyz_le=[0,0,0]))
mock_asb_global.Wing = MagicMock()
mock_asb_global.Airplane = MagicMock()
mock_asb_global.Airfoil = MagicMock()
mock_asb_global.OperatingPoint = MagicMock()
mock_asb_global.Atmosphere = MagicMock()
mock_asb_global.VortexLatticeMethod = MagicMock()


#######################################################################################
#######################################################################################
#######################################################################################

                        # TESTING #


#######################################################################################
#######################################################################################
#######################################################################################



@patch('Final_UAV_Sizing.Modelling.Wing_Sizing.Airfoil.asb', new=mock_asb_global)
def test_AW_1():
    #test_setup_wing_and_airplane
    # Reset mocks for specific test to ensure isolation
    mock_asb_global.Wing.reset_mock()
    mock_asb_global.Airplane.reset_mock()
    mock_asb_global.WingXSec.reset_mock()
    # Configure specific return values per test
    mock_asb_global.Wing.return_value = types.SimpleNamespace(
        xsecs=[], symmetric=True, subdivide_sections=MagicMock(return_value="subdivided_wing_instance")
    )
    mock_asb_global.Airplane.return_value = "test_airplane_instance"

    mock_asb_global.WingXSec = MagicMock(return_value=types.SimpleNamespace(chord=1, twist=0, airfoil=None, xyz_le=[0,0,0]))


    mock_airfoil_obj = types.SimpleNamespace(name="test_af")

    wing, airplane = setup_wing_and_airplane(
        chosen_airfoil=mock_airfoil_obj,
        num_spanwise_sections=5,
        r_chord=1.0, t_chord=0.5,
        r_twist=0, t_twist=-2,
        sweep=0.2
    )

    assert len(mock_asb_global.WingXSec.call_args_list) == 2
    mock_asb_global.WingXSec.assert_any_call(xyz_le=[0, 0, 0], chord=1.0, twist=0, airfoil=mock_airfoil_obj)
    mock_asb_global.WingXSec.assert_any_call(xyz_le=[0.2, 1.5, 0], chord=0.5, twist=-2, airfoil=mock_airfoil_obj)

    mock_asb_global.Wing.assert_called_once()
    assert mock_asb_global.Wing.call_args[1]['symmetric'] is True
    
    mock_asb_global.Wing.return_value.subdivide_sections.assert_called_once_with(5)
    mock_asb_global.Airplane.assert_called_once_with(wings=["subdivided_wing_instance"])
    assert wing == "subdivided_wing_instance"
    assert airplane == "test_airplane_instance"

@patch('Final_UAV_Sizing.Modelling.Wing_Sizing.Airfoil.asb', new=mock_asb_global)
def test_AW_2():
    #test_calculate_section_properties_and_reynolds
    mock_asb_global.Atmosphere.reset_mock()
    mock_asb_global.OperatingPoint.reset_mock()

    mock_xsec1 = types.SimpleNamespace(chord=1.0, xyz_le=[0, 0, 0])
    mock_xsec2 = types.SimpleNamespace(chord=0.8, xyz_le=[0.1, 0.5, 0])
    mock_xsec3 = types.SimpleNamespace(chord=0.6, xyz_le=[0.2, 1.0, 0])
    mock_wing_object = types.SimpleNamespace(xsecs=[mock_xsec1, mock_xsec2, mock_xsec3])

    mock_atmosphere_instance = types.SimpleNamespace(
        density=MagicMock(return_value=1.225),
        dynamic_viscosity=MagicMock(return_value=1.81e-5)
    )
    mock_asb_global.Atmosphere.return_value = mock_atmosphere_instance
    mock_asb_global.OperatingPoint.return_value = types.SimpleNamespace(
        velocity=10, atmosphere=mock_atmosphere_instance
    )

    operational_velocity = 10
    operational_altitude = 0
    
    section_data = calculate_section_properties_and_reynolds(
        mock_wing_object, operational_velocity, operational_altitude
    )

    assert len(section_data) == 2

    assert section_data[0]['y_mid'] == pt.approx(0.25)
    assert section_data[0]['chord'] == pt.approx(0.9)
    assert section_data[0]['span_segment'] == pt.approx(0.5)
    assert section_data[0]['area'] == pt.approx(0.9 * 0.5)
    expected_re0 = (10 * 0.9) / (1.81*10**-5 / 1.225)
    assert section_data[0]['Re'] == pt.approx(expected_re0, rel=1*10**-3)

    assert section_data[1]['y_mid'] == pt.approx(0.75)
    assert section_data[1]['chord'] == pt.approx(0.7)
    assert section_data[1]['span_segment'] == pt.approx(0.5)
    assert section_data[1]['area'] == pt.approx(0.7 * 0.5)
    expected_re1 = (10 * 0.7) / (1.81*10**-5 / 1.225)
    assert section_data[1]['Re'] == pt.approx(expected_re1, rel=1*10**-3)

@patch('Final_UAV_Sizing.Modelling.Wing_Sizing.Airfoil.asb', new=mock_asb_global)
def test_AW_3():
    #test_generate_2d_stall_database_simple_case
    mock_asb_global.Airfoil.reset_mock()

    mock_airfoil_profile = types.SimpleNamespace(name="test_af", coordinates="temp_coords")
    
    mock_internal_af = MagicMock()
    mock_internal_af.generate_polars = MagicMock()
    
    def mock_cl_function(alpha, Re):
        if Re == pt.approx(100000, rel=0.1): 
            if alpha == 10: return 1.0
            if alpha == 12: return 1.2 
            if alpha == 14: return 1.1
            if alpha == 16: return 1.0
        return 0.0
    mock_internal_af.CL_function = MagicMock(side_effect=mock_cl_function)
    mock_asb_global.Airfoil.return_value = mock_internal_af

    # FIX: Changed section Re so the function calculates a discrete Re of 100,000
    section_data = [{'Re': 125000}, {'Re': 130000}]
    alpha_range2D = np.array([10, 12, 14, 16])
    xfoil_path = "dummy_xfoil_path"
    Re_numbers = 1

    stall_df = generate_2d_stall_database(
        mock_airfoil_profile, section_data, alpha_range2D, xfoil_path, Re_numbers
    )
    
    assert isinstance(stall_df, pd.DataFrame)
    assert len(stall_df) == 1
    
    mock_internal_af.generate_polars.assert_called_once()
    called_Re_arg = mock_internal_af.generate_polars.call_args[1]['Res']
    assert len(called_Re_arg) == 1
    assert called_Re_arg[0] == pt.approx(100000, rel=0.1) 

    assert stall_df['Re_polar'].iloc[0] == pt.approx(100000)
    assert stall_df['alpha_stall_2D'].iloc[0] == pt.approx(12)
    assert stall_df['Cl_max_2D'].iloc[0] == pt.approx(1.2)
    # FIX: The calculated K_post from the mock data is -0.05
    assert stall_df['K_post'].iloc[0] == pt.approx(-0.05, abs=1*10**-4)


def test_AW_4():
    #test_interpolate_stall_data_for_sections
    section_data = [
        {'id': 0, 'Re': 150000},
        {'id': 1, 'Re': 250000}
    ]
    stall_df_data = {
        'Re_polar':       [100000, 200000, 300000],
        'alpha_stall_2D': [10,     12,     11],
        'Cl_max_2D':      [1.0,    1.2,    1.15],
        'K_post':         [-0.05,  -0.06,  -0.055]
    }
    stall_df = pd.DataFrame(stall_df_data)
    delta_alpha_3D_correction = 1.0

    updated_section_data = interpolate_stall_data_for_sections(
        section_data, stall_df, delta_alpha_3D_correction
    )

    assert updated_section_data[0]['alpha_stall_2D_interp'] == pt.approx(11.0)
    assert updated_section_data[0]['Cl_max_2D_interp'] == pt.approx(1.1)
    assert updated_section_data[0]['K_post_interp'] == pt.approx(-0.055)
    assert updated_section_data[0]['alpha_stall_3D'] == pt.approx(10.0)

    assert updated_section_data[1]['alpha_stall_2D_interp'] == pt.approx(11.5)
    assert updated_section_data[1]['Cl_max_2D_interp'] == pt.approx(1.175)
    assert updated_section_data[1]['K_post_interp'] == pt.approx(-0.0575)
    assert updated_section_data[1]['alpha_stall_3D'] == pt.approx(10.5)

@patch('Final_UAV_Sizing.Modelling.Wing_Sizing.Airfoil.asb', new=mock_asb_global)
def test_AW_5():
    #test_run_vlm_sweep_with_stall_correction_basic_run
    mock_asb_global.VortexLatticeMethod.reset_mock()
    mock_asb_global.OperatingPoint.reset_mock()
    mock_asb_global.Atmosphere.reset_mock()


    alpha_range3D = np.array([0, 10, 15])
    mock_vlm_airplane = "mock_airplane_for_vlm"
    operational_velocity = 20
    operational_altitude = 0
    num_spanwise_sections = 1
    vlm_chordwise_resolution = 2
    mock_wing = types.SimpleNamespace(symmetric=True, area=MagicMock(return_value=1.0))
    section_data_list = [{
        'id': 0, 'chord': 0.5, 'area': 0.25,
        'alpha_stall_3D': 12.0, 'Cl_max_2D_interp': 1.2, 'K_post_interp': -0.05
    }]

    # Sequence of results from calling vlm.run() multiple times
    run_results_sequence = [
        {"CL": 0.0, "CD": 0.01, "Cm": -0.01},
        {"CL": 1.0, "CD": 0.05, "Cm": -0.05},
        {"CL": 1.3, "CD": 0.08, "Cm": -0.08}
    ]
    # Simulates vortex_strengths attribute on the vlm object after call to vlm.run().
    vortex_strengths_sequence = [
        np.array([0.0] * 4),
        np.array([2.5] * 4),
        np.array([3.0] * 4)
    ]


    mock_vlm_instance = MagicMock()

    # simulates how the real VLM object behaves
    run_call_iterator = iter(zip(run_results_sequence, vortex_strengths_sequence))
    def vlm_run_side_effect():
        results, strengths = next(run_call_iterator)
        mock_vlm_instance.vortex_strengths = strengths  
        return results  # dictionary

    mock_vlm_instance.run.side_effect = vlm_run_side_effect

    mock_asb_global.VortexLatticeMethod.return_value = mock_vlm_instance
    mock_asb_global.Atmosphere.return_value = types.SimpleNamespace()
    mock_asb_global.OperatingPoint.return_value = types.SimpleNamespace()


    CLs_vlm, CDs_vlm, CLs_corrected, lift_dist, Cms = run_vlm_sweep_with_stall_correction(
        alpha_range3D, mock_vlm_airplane, operational_velocity,
        section_data_list, num_spanwise_sections, mock_wing, operational_altitude,
        vlm_chordwise_resolution
    )


    # Check VLM instantiated and run once for each alpha
    assert mock_asb_global.VortexLatticeMethod.call_count == 3
    assert mock_vlm_instance.run.call_count == 3

    # Alpha = 0 deg, pre stall
    assert CLs_vlm[0] == pt.approx(0.0)
    assert CDs_vlm[0] == pt.approx(0.01)
    assert CLs_corrected[0] == pt.approx(0.0)
    assert np.allclose(lift_dist["CLs"][0], [0.0])

    # Alpha = 10 deg, pre stall
    assert CLs_vlm[1] == pt.approx(1.0)
    assert CDs_vlm[1] == pt.approx(0.05)
    assert CLs_corrected[1] == pt.approx(0.5) #Sectional CL from gamma: 1.0. Corrected CL is (2 * 1.0 * 0.25) / 1.0 = 0.5
    assert np.allclose(lift_dist["CLs"][1], [1.0])

    # Alpha = 15 deg (post-stall)
    assert CLs_vlm[2] == pt.approx(1.3)
    assert CDs_vlm[2] == pt.approx(0.08)
    assert CLs_corrected[2] == pt.approx(0.525, abs=1*10**-4)# Corrected CL is (2 * 1.05 * 0.25) / 1.0 = 0.525
    assert np.allclose(lift_dist["CLs"][2], [1.05])