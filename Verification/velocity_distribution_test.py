import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import patch, MagicMock
import sys

# Add the project root directory to the Python path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from StravaFiles.velocity_distribution import (
    make_race_dictionnary,
    air_density_isa,
    plot_race_velocities
)

@pytest.fixture
def temp_race_data_dir(tmp_path):
    """Create a temporary directory with sample race CSV files."""
    data_dir = tmp_path / "RaceData"
    data_dir.mkdir()
    
    # Valid CSV 1
    df1_data = {' velocity_smooth': [10.0, 11.5, 12.0], ' grade_smooth': [1, 0, -1], ' altitude': [100, 105, 110]}
    df1 = pd.DataFrame(df1_data)
    df1.to_csv(data_dir / "race1.csv", index=False)

    # Valid CSV 2
    df2_data = {' velocity_smooth': [8.0, 9.5], ' grade_smooth': [2, 3], ' altitude': [200, 210]}
    df2 = pd.DataFrame(df2_data)
    df2.to_csv(data_dir / "race2.csv", index=False)

    # Non-CSV file
    (data_dir / "notes.txt").write_text("some notes")

    # Malformed CSV
    (data_dir / "bad_race.csv").write_text("header1,header2\n1,2,3")

    return str(data_dir)


def test_make_race_dictionary_folder_not_exist():
    """Test behavior when the data folder does not exist."""
    non_existent_folder = "path/that/does/not/exist"
    races = make_race_dictionnary(data_folder=non_existent_folder)
    assert races == {}

def test_air_density_isa():
    """Test the ISA air density calculation at different altitudes."""
    # Sea level
    assert air_density_isa(0) == pytest.approx(1.225, rel=1e-3)
    # 1000 meters
    assert air_density_isa(1000) == pytest.approx(1.112, rel=1e-3)
    # 11000 meters (tropopause)
    assert air_density_isa(11000) == pytest.approx(0.3639, rel=1e-3)



@patch('StravaFiles.velocity_distribution.plt')
@patch('StravaFiles.velocity_distribution.make_race_dictionnary')
def test_plot_race_velocities_no_data(mock_make_races, mock_plt):
    """Test that the function handles the case where no race data is found."""
    mock_make_races.return_value = {}
    
    plot_race_velocities()

    mock_make_races.assert_called_once()
    # If there's no data, no plotting should occur
    mock_plt.subplots.assert_not_called()
    mock_plt.show.assert_not_called()