import sys
import os

# Add the parent directory of 'Midterm_Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from Midterm_Battery_Modelling.Input.Strava_input_csv import make_race_dictionnary

@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.path.exists", return_value=True)
@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.listdir", return_value=["test.csv"])
@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.path.join", side_effect=lambda *args: "/".join(args))
@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.pd.read_csv")
def test_make_race_dictionnary(mock_read_csv, mock_join, mock_listdir, mock_exists):
    mock_df = pd.DataFrame({"a": [1, 2]})
    mock_read_csv.return_value = mock_df

    races = make_race_dictionnary()
    assert "test.csv" in races
    assert races["test.csv"].equals(mock_df)

@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.path.exists", return_value=False)
def test_no_data_folder(mock_exists):

    result = make_race_dictionnary()
    assert result == {}

@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.path.exists", return_value=True)
@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.listdir", return_value=["corrupt.csv"])
@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.path.join", side_effect=lambda *args: "/".join(args))
@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.pd.read_csv", side_effect=Exception("Corrupted"))
def test_read_csv_throws_exception(mock_read_csv, mock_join, mock_listdir, mock_exists):
    result = make_race_dictionnary()
    assert "corrupt.csv" not in result

@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.path.exists", return_value=True)
@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.listdir", return_value=["note.txt", "readme.md"])
@patch("Midterm_Battery_Modelling.Input.Strava_input_csv.os.path.join", side_effect=lambda *args: "/".join(args))
def test_skips_non_csv_files(mock_join, mock_listdir, mock_exists):
    result = make_race_dictionnary()
    assert result == {}
