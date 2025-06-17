import sys
import os
import pytest as pt

target_folder = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(os.path.abspath(target_folder))

from Structural_Sizing_unittest_version.ForceAndStressCals import *

#test StrucSize1

def test_max_force():
    F1 = 1000  # N
    L = 2500   # m
    F2 = 2000  # N
    max_force = Max_Force(L, F1, F2)
    assert max_force == pt.approx(7499997, rel=1e-5)

#test StrucSize2

def test_bending_simple():
    M = 5000  # Nm
    Y = 0.1   # m
    I = 0.0001  # m^4
    stress = Bending_Simple(M, Y, I)
    assert stress == pt.approx(5000000, rel=1e-5)  # Pa

#test StrucSize3

def test_bending():
    Mx = 3000  # Nm
    Ix = 0.0001  # m^4
    X = 0.05   # m
    My = 2000  # Nm
    Iy = 0.0002  # m^4
    Y = 0.1   # m
    stress = Bending(Mx, Ix, X, My, Iy, Y)
    assert stress == pt.approx(3500000, rel=1e-5)  # Pa

#test StrucSize4

def test_shear_circle_torsion():
    T = 1000  # Nm
    r = 0.05  # m
    J = 0.0001  # m^4
    shear = Shear_Circle_Torsion(T, r, J)
    assert shear == pt.approx(500000, rel=1e-5)  # Pa

#test StrucSize5

def test_shear_torsion():
    T = 1000  # Nm
    t = 0.01  # m
    A = 0.001  # m^2
    shear = Shear_Torsion(T, t, A)
    assert shear == pt.approx(50000000, rel=1e-5)  # Pa

#test StrucSize6

def test_torsion_open():
    T = 1000  # Nm
    l = 2.0   # m
    t = 0.01  # m
    shear = Torsion_Open(T, l, t)
    assert shear == pt.approx(15000000, rel=1e-5)  # Pa

#test StrucSize7
 
def test_shear_transverse_general():
    F = 1000  # N
    Q = 0.0001  # m^3
    I = 0.0001  # m^4
    t = 0.01   # m
    shear = Shear_Transverse_General(F, Q, I, t)
    assert shear == pt.approx(100000, rel=1e-5)

#test StrucSize8

def test_shear_transverse_rectangle():
    F = 1000  # N
    B = 0.1   # m
    H = 0.2   # m
    shear = Shear_Transverse_Rectangle(F, B, H)
    assert shear == pt.approx(75000, rel=1e-5)  # Pa

#test StrucSize9

def test_shear_transverse_circle():
    R_in = 0.05  # m
    R_out = 0.1  # m
    F = 1000     # N
    shear = Shear_Transverse_Circle(R_in, R_out, F)
    assert shear == pt.approx(79224, rel=1e-5) 
    
#test StrucSize0

def test_buckling_stress():
    E = 200e9  # Pa
    L = 2.0    # m
    I = 0.0001  # m^4
    A = 0.01   # m^2
    K = 1      # pin ends
    stress = Buckling_Stress(E, L, I, A, K)
    assert stress == pt.approx(4934802200, rel=1e-5)  # Pa

#test StrucSize11

def test_shear_torsional():
    T = 1000  # Nm
    A_m = 0.001  # m^2
    t = 0.01  # m
    shear = Shear_Torsional(T, A_m, t)
    assert shear == pt.approx(50000000, rel=1e-5)  # Pa

#test StrucSize12

def test_tip_deflection():
    F = 1000  # N
    L = 2.0   # m
    E = 200e9  # Pa
    I = 0.0001  # m^4
    V_tip = Tip_Deflection(F, L, E, I)
    assert V_tip == pt.approx(0.0001, rel=1e-5)  # m

#test StrucSize13

def test_tip_deflection_angle():
    F = 1000  # N
    L = 2.0   # m
    E = 200e9  # Pa
    I = 0.0001  # m^4
    angle = Tip_Deflection_angle(F, L, E, I)
    assert angle == pt.approx(0.0001, rel=1e-5)  # radians

#test StrucSize14

def test_twist():
    T = 1000  # Nm
    L = 2.0   # m
    G = 79.3e9  # Pa
    J = 0.0001  # m^4
    angle = Twist(T, L, G, J)
    assert angle == pt.approx(0.00025, rel=1e-2)  # radians

#test StrucSize15

def test_tresca():
    stress1 = 100e6  # Pa
    stress2 = 50e6   # Pa
    stress3 = 25e6   # Pa
    tresca_stress = Tresca(stress1, stress2, stress3)
    assert tresca_stress == pt.approx(70711000, rel=1e-5)  # Pa

#test StrucSize16

def test_von_mises():
    stress1 = 100e6  # Pa
    stress2 = 50e6   # Pa
    stress3 = 25e6   # Pa
    shear1 = 30e6  # Pa
    shear2 = 20e6  # Pa
    shear3 = 10e6  # Pa
    von_mises_stress = Von_Mises(stress1, stress2, stress3, shear1, shear2, shear3)
    assert von_mises_stress == pt.approx((92601000, 53463000), rel=1e-5)  # Pa

#test StrucSize17
def test_cut_out_corrections():
    diameter = 0.1  # m
    width = 0.5    # m
    k_t = Cut_Out_Corrections(diameter, width)
    assert k_t == pt.approx(3.728, rel=1e-2)  # dimensionless

#test StrucSize18
def test_compute_total_lift_and_centroid():
    def lift_func(z):
        return 111.11 * z**2

    a = 0
    b = 1
    total_lift, x_centroid = Compute_Total_Lift_and_Centroid(lift_func, a, b)
    assert total_lift == pt.approx(37.037, rel=1e-3)  # N
    assert x_centroid == pt.approx(0.75, rel=1e-3)  # m

#test StrucSize19

def test_lift_distribution_test():
    z = 0.5  # example value
    lift = lift_distribution_test(z)
    assert lift == pt.approx(27.7775, rel=1e-4)  # N

#test StrucSize20

def test_drag_distribution_test():
    z = 0.5  # example value
    drag = Drag_distribution_test(z)
    assert drag == pt.approx(2.77775, rel=1e-4)  # N

if __name__ == "__main__":
    pt.main([__file__])

