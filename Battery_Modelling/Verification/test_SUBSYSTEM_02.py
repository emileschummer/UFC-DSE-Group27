import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import pytest
from unittest.mock import patch
import importlib

# Patch functions where they are used: in Battery_Modelling.main
@patch("Battery_Modelling.main.flat_race")
@patch("Battery_Modelling.main.get_race_results")
@patch("Battery_Modelling.main.plot_power_vs_velocity")
def test_main_script(mock_plot, mock_get_race, mock_flat_race):
    import Battery_Modelling.main as main_script
    importlib.reload(main_script)  # Ensure up-to-date
    main_script.main()  # Now explicitly call it

    mock_flat_race.assert_called_once()
    mock_get_race.assert_called_once_with("Battery_Modelling/Output")
    mock_plot.assert_called_once()