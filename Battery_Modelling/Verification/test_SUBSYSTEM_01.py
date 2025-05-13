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
