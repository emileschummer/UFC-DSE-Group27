import os
import numpy as np
import pandas as pd
import aerosandbox as asb
import pytest
import AeroMain

def test_run_full_aero_returns_expected_structure(monkeypatch, tmp_path):
    # Stub out dependencies in AeroMain
    coords = np.array([[0.0, 0.0], [1.0, 0.0]])
    monkeypatch.setattr(AeroMain, "load_airfoil_dat", lambda path: coords)
    # Return dummy wing and airplane
    monkeypatch.setattr(AeroMain, "setup_wing_and_airplane", lambda a, n, rc, tc, rt, tt, s: ("wing_obj", "airplane_obj"))
    # Return dummy section data
    monkeypatch.setattr(AeroMain, "calculate_section_properties_and_reynolds", lambda wing, v, alt: [{"Re": 1e5}])
    # Return dummy stall DataFrame
    stall_df = pd.DataFrame({
        "Re_polar": [1e5],
        "alpha_stall_2D": [2.0],
        "Cl_max_2D": [0.2],
        "K_post": [-0.05],
    })
    monkeypatch.setattr(AeroMain, "generate_2d_stall_database", lambda af, sd, a2d, xp, rn: stall_df)
    # Identity interpolation
    monkeypatch.setattr(AeroMain, "interpolate_stall_data_for_sections", lambda sd, df, da: sd)
    # Stub VLM sweep
    dummy_CLs = [0.5, 0.6]
    dummy_CDs = [0.01, 0.02]
    dummy_CLs_corr = [0.45, 0.55]
    dummy_lift = {"alpha": [1, 2], "CLs": [[0.25, 0.25], [0.3, 0.3]]}
    monkeypatch.setattr(
        AeroMain,
        "run_vlm_sweep_with_stall_correction",
        lambda alpha_range3D, airplane, v, sd, n, wing, alt, c: (dummy_CLs, dummy_CDs, dummy_CLs_corr, dummy_lift),
    )
    # Stub plotting
    monkeypatch.setattr(AeroMain, "plot_aerodynamic_coefficients", lambda *args, **kwargs: None)

    # Call with a small alpha_range3D and custom csv_path
    alpha_range3D = [1, 2]
    csv_file = tmp_path / "out.csv"
    result = AeroMain.run_full_aero(
        airfoil_dat_path="dummy.dat",
        alpha_range3D=alpha_range3D,
        num_spanwise_sections=2,
        csv_path=str(csv_file),
        Plot=False,
    )

    # Check return structure
    assert isinstance(result, dict)
    expected_keys = {"wing_geom", "airplane_geom", "CDs_vlm_original", "CLs_corrected", "lift_distribution", "alphas"}
    assert set(result.keys()) == expected_keys
    assert result["wing_geom"] == "wing_obj"
    assert result["airplane_geom"] == "airplane_obj"
    assert result["CDs_vlm_original"] == dummy_CDs
    assert result["CLs_corrected"] == dummy_CLs_corr
    assert result["lift_distribution"] == dummy_lift
    assert result["alphas"] == alpha_range3D

    # Check CSV was written correctly
    assert csv_file.exists()
    df = pd.read_csv(csv_file)
    # DataFrame should have two rows matching alpha_range3D
    assert list(df["alpha (deg)"]) == alpha_range3D
    assert list(df["CL_corrected"]) == dummy_CLs_corr
    assert list(df["CD_vlm"]) == dummy_CDs

def test_run_full_aero_skips_csv_when_none(monkeypatch):
    # Stub minimal dependencies
    monkeypatch.setattr(AeroMain, "load_airfoil_dat", lambda path: np.zeros((2,2)))
    monkeypatch.setattr(AeroMain, "setup_wing_and_airplane", lambda *args, **kwargs: (None, None))
    monkeypatch.setattr(AeroMain, "calculate_section_properties_and_reynolds", lambda *args, **kwargs: [])
    monkeypatch.setattr(AeroMain, "generate_2d_stall_database", lambda *args, **kwargs: pd.DataFrame())
    monkeypatch.setattr(AeroMain, "interpolate_stall_data_for_sections", lambda *args, **kwargs: [])
    monkeypatch.setattr(
        AeroMain,
        "run_vlm_sweep_with_stall_correction",
        lambda *args, **kwargs: ([], [], [], {"alpha": [], "CLs": []}),
    )
    monkeypatch.setattr(AeroMain, "plot_aerodynamic_coefficients", lambda *args, **kwargs: None)

    # Call with csv_path=None
    result = AeroMain.run_full_aero(csv_path=None)
    # No exception, returns dict
    assert "wing_geom" in result and "alphas" in result