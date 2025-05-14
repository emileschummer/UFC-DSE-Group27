import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import pytest
from unittest.mock import patch
from Battery_Modelling.Modelling.races import get_race_results

def get_mock_race_df():
    return pd.DataFrame({
        " time": [0, 1, 2],
        " distance": [0, 8.2, 20],
        " velocity_smooth": [10, 20, 15],
        " altitude": [100, 110, 105],
        " grade_smooth": [0, 5, -3]
    })

@patch("Battery_Modelling.Modelling.races.sva.make_race_dictionnary")
@patch("Battery_Modelling.Modelling.races.plt.savefig")
@patch("Battery_Modelling.Modelling.races.plt.show")
def test_get_race_results(mock_show, mock_savefig, mock_make_races):
    mock_race = {"mock_race.csv": get_mock_race_df()}
    mock_make_races.return_value = mock_race

    get_race_results(output_folder="mock_output")

    mock_savefig.assert_called_once()
    mock_show.assert_called_once()


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
    from Battery_Modelling.Modelling.races import plot_power_vs_velocity

    plot_power_vs_velocity()

    assert mock_power1.call_count == 1000
    assert mock_power2.call_count == 1000
    assert mock_power3.call_count == 1000
    assert mock_power4.call_count == 1000

    assert mock_plot.call_count == 4

    mock_legend.assert_called_once()
    mock_show.assert_called_once()


@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_1", return_value=10)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_2", return_value=20)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_3", return_value=30)
@patch("Battery_Modelling.Modelling.races.calculate_power_UFC_MMA_4", return_value=40)
def test_flat_race_output(mock_p1, mock_p2, mock_p3, mock_p4, capsys):
    from Battery_Modelling.Modelling.races import flat_race

    flat_race()

    captured = capsys.readouterr()

    assert "---------7h Flat Race at 50km/h---------" in captured.out
    assert "UFC-MMA-1 Helicopter Energy (Wh):  " in captured.out
    assert "UFC-MMA-2 Quadcopter Energy (Wh):  " in captured.out
    assert "UFC-MMA-3 Osprey Energy (Wh):  " in captured.out
    assert "UFC-MMA-4 Yangda Energy (wh):  " in captured.out