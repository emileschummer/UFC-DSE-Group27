import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Battery_Modelling.Sensitivity_Analysis.plot_power import *

import pytest
from unittest.mock import patch, MagicMock
import numpy as np

#Test for plot_power_vs_velocity_sensitivity function
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_1", return_value=10)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_2", return_value=20)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_3", return_value=30)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_4", return_value=40)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.plt.plot")
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.plt.show")
def test_plot_power_vs_velocity_sensitivity(mock_show, mock_plot, mock_p1, mock_p2, mock_p3, mock_p4):
    plot_power_vs_velocity_sensitivity(iterations=2)
    assert mock_plot.called
    assert mock_show.called

#Test for get_race_results function
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_1", return_value=100)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_2", return_value=200)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_3", return_value=300)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_4", return_value=400)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.sva.air_density_isa", return_value=1.225)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.sva.make_race_dictionnary")
def test_get_race_results(mock_make_race_dict, mock_air_density, mock_p1, mock_p2, mock_p3, mock_p4, capsys):
    import pandas as pd
    mock_df = pd.DataFrame({
        " time": [0, 1, 2],
        " velocity_smooth": [10, 15, 20],
        " altitude": [100, 100, 100],
        " grade_smooth": [0, 0, 0]
    })

    mock_make_race_dict.return_value = {"mock_race.csv": mock_df}

    get_race_results(iterations=2)

    captured = capsys.readouterr()
    assert "mock_race.csv" in captured.out
    assert "UFC-MMA-1" in captured.out
