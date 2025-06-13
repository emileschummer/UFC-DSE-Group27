import sys
import os

# Add the parent directory of 'Midterm_Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Midterm_Battery_Modelling.Modelling.plot_power import *

import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import pandas as pd

#Test for plot_power_vs_velocity_sensitivity function
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_1", return_value=10)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_2", return_value=20)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_3", return_value=30)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_4", return_value=40)
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.plt.plot")
@patch("Midterm_Battery_Modelling.Sensitivity_Analysis.plot_power.plt.show")
def test_plot_power_vs_velocity_sensitivity(mock_show, mock_plot, mock_p1, mock_p2, mock_p3, mock_p4):
    plot_power_vs_velocity_sensitivity(iterations=2)
    assert mock_plot.called
    assert mock_show.called

