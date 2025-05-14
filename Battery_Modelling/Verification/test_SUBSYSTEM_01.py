from unittest.mock import patch
from Battery_Modelling.Sensitivity_Analysis.plot_power import *
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

#Test get_race_results function for one race
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.sva.make_race_dictionnary")
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.plt.savefig")
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.plt.show")
def test_get_race_results(mock_show, mock_savefig, mock_make_races):
    mock_race = {"mock_race.csv": mock_race_df()}
    mock_make_races.return_value = mock_race

    get_race_results(output_folder="mock_output")

    mock_savefig.assert_called_once()
    mock_show.assert_called_once()


#Test plot_power_vs_velocity function
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_1", return_value=1)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_2", return_value=2)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_3", return_value=3)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_4", return_value=4)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.plt.show")
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.plt.plot")
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.plt.legend")
def test_plot_power_vs_velocity(
    mock_legend, mock_plot, mock_show,
    mock_power1, mock_power2, mock_power3, mock_power4
):
    from Battery_Modelling.Sensitivity_Analysis.plot_power import plot_power_vs_velocity

    plot_power_vs_velocity()

    assert mock_power1.call_count == 1000
    assert mock_power2.call_count == 1000
    assert mock_power3.call_count == 1000
    assert mock_power4.call_count == 1000

    assert mock_plot.call_count == 4

    mock_legend.assert_called_once()
    mock_show.assert_called_once()

#Test plot_power_vs_gradient function
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_1", return_value=10)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_2", return_value=20)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_3", return_value=30)
@patch("Battery_Modelling.Sensitivity_Analysis.plot_power.calculate_power_UFC_MMA_4", return_value=40)
def test_flat_race_output(mock_p1, mock_p2, mock_p3, mock_p4, capsys):
    from Battery_Modelling.Sensitivity_Analysis.plot_power import flat_race

    flat_race()

    captured = capsys.readouterr()

    assert "---------7h Flat Race at 50km/h---------" in captured.out
    assert "UFC-MMA-1 Helicopter Energy (Wh):  " in captured.out
    assert "UFC-MMA-2 Quadcopter Energy (Wh):  " in captured.out
    assert "UFC-MMA-3 Osprey Energy (Wh):  " in captured.out
    assert "UFC-MMA-4 Yangda Energy (wh):  " in captured.out


