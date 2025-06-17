import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np
import pandas as pd
import pytest
from unittest.mock import MagicMock, call # Import call for checking call arguments

# Import the module to be tested
from Final_UAV_Sizing.Modelling.Wing_Sizing import AeroMain

def test_run_full_aero_orchestration(monkeypatch, tmp_path):
    """
    Tests the main orchestration logic of run_full_aero, ensuring:
    - Dependencies are called as expected.
    - Output directory and CSV files are created correctly.
    - Return structure is correct.
    - Key calculations like alpha_at_max_cl are performed and used.
    """
    # 1. Setup mock paths using tmp_path
    mock_output_dir_arg = tmp_path / "test_outputs"
    # AeroMain will create a "Wing_Sizing" subdirectory within this
    expected_final_output_dir = mock_output_dir_arg / "Wing_Sizing"
    mock_csv_path_arg = tmp_path / "primary_aero_results.csv"
    expected_secondary_csv_path = expected_final_output_dir / "aero_specific.csv"

    # 2. Define mock return values for dependencies
    mock_airfoil_name = "TestAirfoil"
    mock_airfoil_coords = np.array([[1,0], [0.5, 0.05], [0,0], [0.5, -0.05], [1,0]]) # Dummy valid coords
    
    mock_wing_geom_obj = MagicMock(name="mock_wing_geom")
    mock_airplane_geom_obj = MagicMock(name="mock_airplane_geom")
    
    mock_section_data_list = [{"Re": 1.5e5, "id": 0}] # Dummy section data
    
    mock_stall_df = pd.DataFrame({
        "Re_polar": [1.5e5], "alpha_stall_2D": [12.0], "Cl_max_2D": [1.2], "K_post": [-0.05],
    })
    
    # Define data for a 2-point alpha sweep
    alpha_range3D_input = np.array([10.0, 15.0]) # Max CL should be at 15.0 degrees
    dummy_CLs_vlm = np.array([0.9, 1.1])
    dummy_CDs_vlm = np.array([0.04, 0.06])
    dummy_CLs_corrected = np.array([0.8, 1.0]) # Max corrected CL is 1.0 at alpha 15.0
    dummy_CM_vlm = np.array([-0.05, -0.06])
    dummy_lift_distribution = {"alpha": alpha_range3D_input.tolist(), "CLs": [[0.4, 0.4], [0.5, 0.5]]}
    expected_alpha_at_max_cl = 15.0 # Based on dummy_CLs_corrected

    mock_max_distribution_data = {"y_span": [0, 0.75], "Cl_dist": [0.9, 1.1]}

    # 3. Mock 'aerosandbox' (asb) used within AeroMain
    mock_asb_module = MagicMock(name="mock_asb_module")
    mock_asb_airfoil_instance = MagicMock(name="mock_asb_airfoil_instance")
    mock_asb_module.Airfoil.return_value = mock_asb_airfoil_instance
    monkeypatch.setattr(AeroMain, "asb", mock_asb_module)

    # 4. Monkeypatch (stub) imported functions within AeroMain's scope
    mock_load_airfoil_dat = MagicMock(return_value=mock_airfoil_coords)
    monkeypatch.setattr(AeroMain, "load_airfoil_dat", mock_load_airfoil_dat)

    mock_setup_wing_and_airplane = MagicMock(return_value=(mock_wing_geom_obj, mock_airplane_geom_obj))
    monkeypatch.setattr(AeroMain, "setup_wing_and_airplane", mock_setup_wing_and_airplane)

    mock_calc_sections = MagicMock(return_value=mock_section_data_list)
    monkeypatch.setattr(AeroMain, "calculate_section_properties_and_reynolds", mock_calc_sections)

    mock_gen_stall_db = MagicMock(return_value=mock_stall_df)
    monkeypatch.setattr(AeroMain, "generate_2d_stall_database", mock_gen_stall_db)

    # interpolate_stall_data_for_sections often modifies input; ensure it returns a consistent structure
    mock_interpolated_section_data = [{"Re": 1.5e5, "id": 0, "alpha_stall_3D": 11.0}] # Example processed data
    mock_interpolate = MagicMock(return_value=mock_interpolated_section_data)
    monkeypatch.setattr(AeroMain, "interpolate_stall_data_for_sections", mock_interpolate)

    mock_vlm_sweep = MagicMock(return_value=(
        dummy_CLs_vlm, dummy_CDs_vlm, dummy_CLs_corrected, dummy_lift_distribution, dummy_CM_vlm
    ))
    monkeypatch.setattr(AeroMain, "run_vlm_sweep_with_stall_correction", mock_vlm_sweep)

    mock_plot_coeffs = MagicMock()
    monkeypatch.setattr(AeroMain, "plot_aerodynamic_coefficients", mock_plot_coeffs)

    mock_load_distribution = MagicMock(return_value=mock_max_distribution_data)
    monkeypatch.setattr(AeroMain, "load_distribution_halfspan", mock_load_distribution)

    # 5. Call the function under test
    result = AeroMain.run_full_aero(
        airfoil_dat_path="dummy_path.dat", # Path itself is mocked by load_airfoil_dat
        name=mock_airfoil_name,
        xfoil_path="dummy_xfoil_path",
        operational_velocity=10.0,
        num_spanwise_sections=10, # Example value
        vlm_chordwise_resolution=5, # Example value
        alpha_range3D=alpha_range3D_input,
        csv_path=str(mock_csv_path_arg),
        output_folder=str(mock_output_dir_arg),
        Plot=False # Important for testing without actual plot windows
    )

    # 6. Assertions
    # Check asb.Airfoil call
    mock_asb_module.Airfoil.assert_called_once_with(name=mock_airfoil_name, coordinates=mock_airfoil_coords)

    # Check calls to patched functions (selected examples)
    mock_load_airfoil_dat.assert_called_once_with("dummy_path.dat")
    mock_setup_wing_and_airplane.assert_called_once_with(
        mock_asb_airfoil_instance, 10, # num_spanwise_sections
        # Other default geometry args from run_full_aero if not overridden in call
        AeroMain.run_full_aero.__defaults__[6], # r_chord
        AeroMain.run_full_aero.__defaults__[7], # t_chord
        AeroMain.run_full_aero.__defaults__[8], # r_twist
        AeroMain.run_full_aero.__defaults__[9], # t_twist
        AeroMain.run_full_aero.__defaults__[10] # sweep
    )
    mock_calc_sections.assert_called_once_with(mock_wing_geom_obj, 10.0, AeroMain.run_full_aero.__defaults__[11]) # op_vel, op_alt
    mock_gen_stall_db.assert_called_once_with(
        mock_asb_airfoil_instance, mock_section_data_list, 
        AeroMain.run_full_aero.__defaults__[4], # alpha_range2D
        "dummy_xfoil_path", 
        AeroMain.run_full_aero.__defaults__[12] # Re_numbers
    )
    mock_interpolate.assert_called_once_with(mock_section_data_list, mock_stall_df, AeroMain.run_full_aero.__defaults__[3]) # delta_alpha_3D_correction
    mock_vlm_sweep.assert_called_once_with(
        alpha_range3D_input, mock_airplane_geom_obj, 10.0, mock_interpolated_section_data, 10, mock_wing_geom_obj, 
        AeroMain.run_full_aero.__defaults__[11], # op_alt
        5 # vlm_chordwise_resolution
    )

    # Check return structure and values
    assert isinstance(result, dict)
    expected_keys = {
        "wing_geom", "airplane_geom", "CDs_vlm_original", "CLs_corrected", 
        "lift_distribution", "alphas", "CM_vlm", "max_distribution"
    }
    assert set(result.keys()).issuperset(expected_keys) # Check if all expected keys are present
    
    assert result["wing_geom"] is mock_wing_geom_obj
    assert result["airplane_geom"] is mock_airplane_geom_obj
    assert np.array_equal(result["CDs_vlm_original"], dummy_CDs_vlm)
    assert np.array_equal(result["CLs_corrected"], dummy_CLs_corrected)
    assert result["lift_distribution"] == dummy_lift_distribution
    assert np.array_equal(result["alphas"], alpha_range3D_input)
    assert np.array_equal(result["CM_vlm"], dummy_CM_vlm)
    assert result["max_distribution"] == mock_max_distribution_data

    # Check directory creation
    assert expected_final_output_dir.is_dir()

    # Check plotting call
    mock_plot_coeffs.assert_called_once()
    # Check some key args of plot_coeffs call
    call_args, call_kwargs = mock_plot_coeffs.call_args
    assert np.array_equal(call_args[0], alpha_range3D_input)
    assert np.array_equal(call_args[1], dummy_CLs_vlm)
    assert np.array_equal(call_args[2], dummy_CLs_corrected)
    assert np.array_equal(call_args[3], dummy_CDs_vlm)
    assert call_args[4] is False # Plot argument
    assert call_kwargs['output_folder'] == str(expected_final_output_dir)


    # Check load_distribution_halfspan call (after plot_coeffs)
    mock_load_distribution.assert_called_once_with(
        mock_wing_geom_obj, dummy_lift_distribution, expected_alpha_at_max_cl,
        half_span=1.5, plot=False, output_folder=str(expected_final_output_dir)
    )

    # Check primary CSV file
    assert mock_csv_path_arg.exists()
    df_primary = pd.read_csv(mock_csv_path_arg)
    assert list(df_primary["alpha (deg)"]) == alpha_range3D_input.tolist()
    assert np.allclose(df_primary["CL_corrected"], dummy_CLs_corrected)
    assert np.allclose(df_primary["CD_vlm"], dummy_CDs_vlm)
    assert np.allclose(df_primary["Cm_vlm"], dummy_CM_vlm)

    # Check secondary CSV file
    assert expected_secondary_csv_path.exists()
    df_secondary = pd.read_csv(expected_secondary_csv_path)
    assert list(df_secondary["alpha (deg)"]) == alpha_range3D_input.tolist()
    assert np.allclose(df_secondary["CL_corrected"], dummy_CLs_corrected)
    assert np.allclose(df_secondary["CD_vlm"], dummy_CDs_vlm)
    assert np.allclose(df_secondary["Cm_vlm"], dummy_CM_vlm)