import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from unittest.mock import patch
from Battery_Modelling.Modelling.races import *
import pandas as pd

#Mock data for testing
def mock_race_df():
    return pd.DataFrame({
        " time": [0, 1, 2],
        " distance": [0, 10, 20],
        " velocity_smooth": [0, 17, 18],  # all > 15
        " altitude": [100, 110, 120],
        " grade_smooth": [0, 0, 0]
    })


#Test plot_power_vs_velocity function
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_1", return_value=1)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_2", return_value=2)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_3", return_value=3)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_4", return_value=4)
@patch("Battery_Modelling.Modelling.races.plt.show")
@patch("Battery_Modelling.Modelling.races.plt.plot")
@patch("Battery_Modelling.Modelling.races.plt.legend")
def test_plot_power_vs_velocity(
    mock_legend, mock_plot, mock_show,
    mock_power1, mock_power2, mock_power3, mock_power4
):
    plot_power_vs_velocity_sensitivity()

    assert mock_power1.call_count == 1000
    assert mock_power2.call_count == 1000
    assert mock_power3.call_count == 1000
    assert mock_power4.call_count == 1000

    assert mock_plot.call_count == 4

    mock_legend.assert_called_once()
    mock_show.assert_called_once()