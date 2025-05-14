import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from unittest.mock import patch
from Battery_Modelling.Modelling.races import plot_race_results, flat_race
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

#Test plot_race_results function for one race
@patch("Battery_Modelling.Modelling.races.sva.make_race_dictionnary")
@patch("Battery_Modelling.Modelling.races.plt.savefig")
@patch("Battery_Modelling.Modelling.races.plt.show")
def test_plot_race_results(mock_show, mock_savefig, mock_make_races):
    mock_race = {"mock_race.csv": mock_race_df()}
    mock_make_races.return_value = mock_race

    plot_race_results(output_folder="mock_output")

    mock_savefig.assert_called_once()
    mock_show.assert_called_once()

#Test flat_race function
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_1", return_value=10)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_2", return_value=20)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_3", return_value=30)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_4", return_value=40)
def test_flat_race_output(mock_p1, mock_p2, mock_p3, mock_p4, capsys):

    flat_race()

    captured = capsys.readouterr()

    assert "---------7h Flat Race at 50km/h---------" in captured.out
    assert "UFC-MMA-1 Helicopter Energy (Wh):  " in captured.out
    assert "UFC-MMA-2 Quadcopter Energy (Wh):  " in captured.out
    assert "UFC-MMA-3 Osprey Energy (Wh):  " in captured.out
    assert "UFC-MMA-4 Yangda Energy (wh):  " in captured.out


