import pytest
import numpy as np
import pandas as pd
import aerosandbox as asb

from Airfoil import (
    setup_wing_and_airplane,
    calculate_section_properties_and_reynolds,
    generate_2d_stall_database,
    interpolate_stall_data_for_sections,
    run_vlm_sweep_with_stall_correction,
    plot_aerodynamic_coefficients,
)

@pytest.fixture
def simple_airfoil():
    # minimal airfoil for testing
    return asb.Airfoil(name="Test", coordinates=np.array([[0.0, 0.0], [1.0, 0.0]]))

def test_setup_wing_and_airplane_returns_wing_and_airplane(simple_airfoil):
    wing, airplane = setup_wing_and_airplane(
        simple_airfoil,
        num_spanwise_sections=3,
        r_chord=1.0,
        t_chord=0.5,
        r_twist=0.0,
        t_twist=0.0,
        sweep=0.0,
    )
    assert hasattr(wing, "xsecs")
    assert isinstance(airplane, asb.Airplane)
    # subdivided into 3 spanwise sections => xsecs length = 3+1
    assert len(wing.xsecs) == 4

def test_calculate_section_properties_and_reynolds(simple_airfoil):
    wing, _ = setup_wing_and_airplane(
        simple_airfoil, 4, 1.0, 1.0, 0.0, 0.0, 0.0
    )
    secs = calculate_section_properties_and_reynolds(wing, operational_velocity=10.0, operational_altitude=0.0)
    # should have one entry per panel = len(xsecs)-1
    assert isinstance(secs, list)
    assert len(secs) == len(wing.xsecs) - 1
    for d in secs:
        assert "Re" in d and d["Re"] > 0
        for key in ["id", "y_mid", "chord", "area"]:
            assert key in d

def test_generate_2d_stall_database_monkeypatched(monkeypatch, simple_airfoil):
    # stub out XFoil calls
    class DummyAirfoil:
        def __init__(self, name, coordinates):
            pass
        def generate_polars(self, alphas, Res, xfoil_kwargs, include_compressibility_effects):
            pass
        def CL_function(self, alpha, Re):
            return 0.5  # constant CL
    monkeypatch.setattr(asb, "Airfoil", DummyAirfoil)

    section_data = [{"Re": 1e5}, {"Re": 2e5}]
    alpha_range2D = np.array([-5.0, 0.0, 5.0])
    df = generate_2d_stall_database(
        airfoil_profile=simple_airfoil,
        section_data=section_data,
        alpha_range2D=alpha_range2D,
        xfoil_path="xfoil",
        Re_numbers=3,
    )
    assert isinstance(df, pd.DataFrame)
    for col in ["Re_polar", "alpha_stall_2D", "Cl_max_2D", "K_post"]:
        assert col in df.columns
    assert df.shape[0] >= 1

def test_interpolate_stall_data_for_sections():
    section_data = [{"Re": 1e5}]
    stall_df = pd.DataFrame({
        "Re_polar": [5e4, 1e5, 2e5],
        "alpha_stall_2D": [1.0, 2.0, 3.0],
        "Cl_max_2D": [0.1, 0.2, 0.3],
        "K_post": [-0.05, -0.1, -0.15],
    })
    out = interpolate_stall_data_for_sections(section_data, stall_df, delta_alpha_3D_correction=0.5)
    sec = out[0]
    assert "alpha_stall_2D_interp" in sec
    assert "Cl_max_2D_interp" in sec
    assert "K_post_interp" in sec
    assert np.isclose(sec["alpha_stall_3D"], sec["alpha_stall_2D_interp"] - 0.5)

def test_run_vlm_sweep_with_stall_correction_monkeypatched(monkeypatch):
    # dummy wing-like
    class DummyWing:
        symmetric = True
        def area(self): return 2.0
    # stub out VLM
    class DummyVLM:
        def __init__(self, airplane, op_point, spanwise_resolution, chordwise_resolution):
            # 2 sections * 2 chordwise panels = 4 per wing *2 for symmetric = 8
            # but code only uses half (4)
            self.vortex_strengths = np.ones(4)
        def run(self):
            return {"CL": 7.0, "CD": 9.0}
    monkeypatch.setattr(asb, "VortexLatticeMethod", DummyVLM)

    # prepare inputs
    alpha_range3D = [0.0]
    dummy_airplane = object()
    section_data = [
        {"chord": 1.0, "area": 1.0, "alpha_stall_3D": 2.0, "Cl_max_2D_interp": 0.2, "K_post_interp": -0.05}
        for _ in range(2)
    ]
    CLs_vlm, CDs_vlm, CLs_corr, lift_dist = run_vlm_sweep_with_stall_correction(
        alpha_range3D=alpha_range3D,
        vlm_airplane=dummy_airplane,
        operational_velocity=1.0,
        section_data_list=section_data,
        num_spanwise_sections=2,
        wing=DummyWing(),
        operational_altitude=0.0,
        vlm_chordwise_resolution=2,
    )
    assert CLs_vlm == [7.0]
    assert CDs_vlm == [9.0]
    # corrected CL = (2 * sum(gamma)*2 sections)/(wing_area)
    assert CLs_corr == [8.0]
    assert lift_dist["alpha"] == [0.0]
    assert lift_dist["CLs"] == [[4.0, 4.0]]

def test_plot_aerodynamic_coefficients_no_error():
    # should not error with Plot=False
    result = plot_aerodynamic_coefficients(
        alphas=[0, 5],
        CLs_vlm=[0.1, 0.2],
        CLs_corrected=[0.1, 0.15],
        CDs_vlm=[0.01, 0.02],
        Plot=False,
    )
    assert result is None