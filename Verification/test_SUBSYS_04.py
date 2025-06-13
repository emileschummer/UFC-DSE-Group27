import sys
import os

# Add the parent directory of 'Midterm_Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Midterm_Battery_Modelling.Modelling.plot_power import *

import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import pandas as pd

#Test get_race_results function
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_1", return_value=100)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_2", return_value=200)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_3", return_value=300)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_4", return_value=400)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.sva.air_density_isa", return_value=1.225)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.sva.make_race_dictionnary")
def test_get_race_results_output(mock_make_race_dict, mock_rho, mock_p1, mock_p2, mock_p3, mock_p4, tmp_path):

    # Minimal mock race data
    mock_df = pd.DataFrame({
        " time": [0, 1, 2],
        " velocity_smooth": [10, 15, 20],
        " altitude": [100, 100, 100],
        " grade_smooth": [0, 0, 0]
    })

    mock_make_race_dict.return_value = {"MockRace.csv": mock_df}

    # Run the function
    get_race_results(folder=tmp_path, iterations=2, variance=0.0)

    # Check that a file was created
    output_files = list(tmp_path.glob("race_results_*.txt"))
    assert len(output_files) == 1

    # Read and validate output content
    content = output_files[0].read_text()
    assert "MockRace.csv" in content
    assert "UFC-MMA-1" in content
    assert "Maximum energy consumption" in content
    assert "Drones required" in content