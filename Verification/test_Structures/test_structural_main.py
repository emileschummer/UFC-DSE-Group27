import sys
import os
import pytest as pt
import numpy as np

target_folder = os.path.join(os.path.dirname(__file__), "..", '..')
sys.path.append(os.path.abspath(target_folder))


from Structural_Sizing_unittest_version.Main import *
from Structural_Sizing_unittest_version.ForceAndStressCals import *
from Structural_Sizing_unittest_version.InertiaCalcs import *
from Structural_Sizing_unittest_version.Main_for_testing import *

# def test_structure_main_runs():

#     Materials_Input=[Aluminum7075T6(),Aluminum2024T4(),Aluminum2024T4(),NaturalFibre(),NaturalFibre()] 
#     VTOL_Input=[0.01,0.736,70.6,2.28]
#     Tail_Input=[0.15,3,20,30]
#     Legs_Input=[0.25,25]
#     Wing_Input=[3,0.65,18,lift_distribution_test,Drag_distribution_test]
#     Fuselage_Input=[0.125,0.1,0.3,0.4,0.4,0.6,150,10,2,5,0.8,10]
#     SF=1.5
#     BigG=1.1

#     result = Structure_Main(
#         Materials_Input=Materials_Input,
#         VTOL_Input=VTOL_Input,
#         Tail_Input=Tail_Input,
#         Legs_Input=Legs_Input,
#         Wing_Input=Wing_Input,
#         Fuselage_Input=Fuselage_Input,
#         SF=SF,
#         BigG=BigG
#     )

#     # Check that result is a tuple of 6 numbers
#     assert isinstance(result, tuple)
#     assert len(result) == 6
#     result = np.array(result)

#     expected_results = np.array([0.0786027, 1.39922, 2.01747, 1.67710, 5.17239, 12.7157])


#     assert np.allclose(result, expected_results, rtol=1e-5, atol=1e-8)








# Dummy distribution functions
def dummy_distribution(x):
    return 1.0

@pt.fixture
def model():
    Materials_Input = [PLA3DPrintMaterial(),PLA3DPrintMaterial(),PLA3DPrintMaterial(),PLA3DPrintMaterial(),PLA3DPrintMaterial()]
    VTOL_Input = [0.01, 0.736, 70.6, 2.28]
    Tail_Input = [0.15, 3, 20, 30]
    Legs_Input = [0.25, 25]
    Wing_Input = [3, 0.65, 18, dummy_distribution, dummy_distribution]
    Fuselage_Input = [0.125, 0.1, 0.3, 0.4, 0.4, 0.6, 150, 10, 2, 5, 0.8, 10]
    SF = 1.5
    BigG = 1.1
    return StructureModel(Materials_Input, VTOL_Input, Tail_Input, Legs_Input, Wing_Input, Fuselage_Input, SF, BigG)

def test_model_output(model):
    result = model.run()
    assert isinstance(result, tuple)
    assert len(result) == 7
    result = np.array(result)
    expected_results = np.array([ 0.508806,  0.140241 ,  3.93376,  0.899878 ,  2.36539,
        7.33927, 14.8481])
    assert np.allclose(result, expected_results, rtol=1e-5, atol=1e-8)
    print(result)

def test_init_sets_attributes(model):
    assert hasattr(model, "Materials_Input")
    assert hasattr(model, "VTOL_Input")
    assert hasattr(model, "Tail_Input")
    assert hasattr(model, "Legs_Input")
    assert hasattr(model, "Wing_Input")
    assert hasattr(model, "Fuselage_Input")
    assert hasattr(model, "SF")
    assert hasattr(model, "BigG")

def test_init_materials_sets_materials(model):
    model.init_materials()
    assert hasattr(model, "Material_VTOL")
    assert hasattr(model, "Material_WingBox")
    assert hasattr(model, "Material_Leg")
    assert hasattr(model, "Material_Fuselage")
    assert hasattr(model, "Material_Airfoil")

def test_init_geometry_sets_geometry(model):
    model.init_geometry()
    assert hasattr(model, "MAC")
    assert hasattr(model, "R_in_VTOL_front")
    assert hasattr(model, "R_out_VTOL_front")
    assert hasattr(model, "R_in_fuselage")
    assert hasattr(model, "R_out_fuselage")

def test_init_loads_sets_loads(model):
    model.init_loads()
    assert hasattr(model, "Safety_Factor")
    assert hasattr(model, "F_Vtol")
    assert hasattr(model, "T_Vtol")
    assert hasattr(model, "Main_Engine_Thrust")

def test_optimize_vtol_front_runs(model):
    # Should update R_out_VTOL_front and not raise
    before = model.R_out_VTOL_front
    model.optimize_vtol_front()
    assert model.R_out_VTOL_front >= before

def test_optimize_vtol_back_runs(model):
    before = model.R_out_VTOL_back
    model.optimize_vtol_back()
    assert model.R_out_VTOL_back >= before

def test_optimize_wingbox_runs(model):
    before = model.R_in_WingBox
    model.optimize_wingbox()
    assert model.R_in_WingBox <= before

def test_optimize_leg_runs(model):
    before = model.R_leg
    model.optimize_leg()
    assert model.R_leg >= before

def test_optimize_fuselage_runs(model):
    before = model.R_out_fuselage
    model.optimize_fuselage()
    assert model.R_out_fuselage >= before

def test_calculate_skin_mass_returns_positive(model, monkeypatch: pt.MonkeyPatch):
    # Patch AirfoilDataExtraction functions to avoid file IO
    monkeypatch.setattr("Structural_Sizing.Main_for_testing.load_airfoil_dat", lambda x: [(0,0),(1,0),(1,1),(0,1)])
    monkeypatch.setattr("Structural_Sizing.Main_for_testing.Airfoil_Moment_of_Inertia", lambda pts, scale: (0,0,0,1.0*scale))
    mass = model.calculate_skin_mass()
    assert isinstance(mass, float)
    assert mass > 0

def test_calculate_vtol_pole_mass_returns_positive(model):
    mass = model.calculate_vtol_pole_mass()
    assert isinstance(mass, float)
    assert mass > 0

def test_calculate_fuselage_mass_returns_positive(model):
    mass = model.calculate_fuselage_mass()
    assert isinstance(mass, float)
    assert mass > 0

def test_calculate_leg_mass_returns_positive(model):
    mass = model.calculate_leg_mass()
    assert isinstance(mass, float)
    assert mass > 0

def test_calculate_wingbox_mass_returns_positive(model):
    mass = model.calculate_wingbox_mass()
    assert isinstance(mass, float)
    assert mass > 0

if __name__ == "__main__":
    pt.main([__file__])