import sys
import os
import pytest as pt

target_folder = os.path.join(os.path.dirname(__file__), "..", '..')
sys.path.append(os.path.abspath(target_folder))

from Structural_Sizing_unittest_version.InertiaCalcs import *

#test StructSize21

def test_circle_moment_of_inertia():
    r_out = 0.05  # m
    r_in = 0.02  # m
    I = Circle_Moment_of_Inertia(r_out, r_in)
    assert I == pt.approx(4.7831e-06, rel=1e-5)  # m^4

#test StructSize22
def test_solid_circle_moment_of_inertia():
    R = 0.05  # m
    I = Solid_Circle_moment_of_Inertia(R)
    assert I == pt.approx(4.9087e-06, rel=1e-5)  # m^4

#test StructSize23
def test_rectangle_moment_of_inertia():
    B = 0.1  # m
    H = 0.2  # m
    I_x = Rectangle_Moment_of_Inertia(B, H)
    assert I_x == pt.approx(6.6667e-05, rel=1e-5)  # m^4

#test StructSize24

def test_i_beam_moment_of_inertia():
    t1 = 0.01  # m
    t2 = 0.02  # m
    t3 = 0.01  # m
    B = 0.1  # m
    H = 0.2  # m
    I = I_Beam_Moment_of_Inertia(t1, t2, t3, B, H)
    assert I == pt.approx(1.3352e-05, rel=1e-5)  # m^4

#test StructSize25

def test_wing_box_moment_of_inertia():
    B = 0.1  # m
    H = 0.2  # m
    t = 0.01  # m
    I = WingBox_Moment_of_inertia(B, H, t)
    assert I == pt.approx(2.77867e-05, rel=1e-5)  # m^4

#test StructSize26

def test_circle_polar_moment_of_inertia():
    R_out = 0.05  # m
    R_in = 0.02  # m
    J = Circle_Polar_Moment_of_Inertia(R_out, R_in)
    assert J == pt.approx(9.56615e-06, rel=1e-5)  # m^4

#test StructSize27

def test_circle_polar_moment_of_inertia2():
    t = 0.01  # m
    R_out = 0.05  # m
    J = Circle_Polar_Moment_of_Inertia2(t, R_out)
    assert J == pt.approx(7.85398e-06, rel=1e-5)  # m^4

#test StructSize28

def test_semi_circle_moment_of_inertia_fuselage():
    R_out = 0.05  # m
    R_in = 0.02  # m
    B = 0.1  # m
    H = 0.2  # m
    t_Ibeam = 0.01  # m
    I = Semi_Circle_Moment_of_Inertia_Fuselage(R_out, R_in, B, H, t_Ibeam)
    assert I == pt.approx(3.9204e-05, rel=1e-5)  # m^4

#test StructSize29

def test_semi_circle_moment_of_inertia():
    R_in = 0.02  # m
    R_out = 0.05  # m
    I = Semi_Circle_Moment_of_Inertia(R_in, R_out)
    assert I == pt.approx(5.7338e-06, rel=1e-5)  # m^4

#test StructSize30
def test_first_area_q_wingbox():
    h = 0.2  # m
    b = 0.1  # m
    t = 0.01  # m
    Q = First_Area_Q_WingBox(h, b, t)
    assert Q == pt.approx(0.0001355, rel=1e-5)  # m^3

#test StructSize31

def test_first_area_q_ibeam():
    h = 0.2  # m
    b = 0.1  # m
    t1 = 0.01  # m
    t2 = 0.02  # m
    Q = First_Area_Q_IBeam(h, b, t1, t2)
    assert Q == pt.approx(0.0011125, rel=1e-5)  # m^3

#test StructSize32

def test_first_area_q_circle():
    R_out = 0.05  # m
    R_in = 0.02  # m
    t = 0.01  # m
    Q = First_Area_Q_Circle(R_out, R_in, t)
    assert Q == pt.approx(0.00076983, rel=1e-5)
    
#test StructSize33

def test_first_area_q_semicircle():
    R_out = 0.05  # m
    R_in = 0.02  # m
    t = 0.01  # m
    Q = First_Area_Q_SemiCircle(t, R_out, R_in)
    assert Q == pt.approx(2.45e-05, rel=1e-5)

#test StructSize34

def test_spring_constant():
    E = 210e9  # Pa
    I = 1e-6   # m^4
    L = 1.0    # m
    k = Spring_Constant(E, I, L)
    assert k == pt.approx(210000, rel=1e-5)  # N/m

#test StructSize35

def test_tube_area():
    R_out = 0.05  # m
    R_in = 0.02   # m
    A = Tube_Area(R_out, R_in)
    assert A == pt.approx(0.0065973, rel=1e-5)
    
#test StructSize36

def test_i_beam_area():
    t1 = 0.01  # m
    t2 = 0.02  # m
    t3 = 0.01  # m
    B = 0.1    # m
    H = 0.2    # m
    A = I_beam_Area(t1, t2, t3, B, H)
    assert A == pt.approx(0.0052, rel=1e-5)  # m^2

#test StructSize37

def test_wing_box_area():
    B = 0.1  # m
    H = 0.2  # m
    t = 0.01  # m
    A = WingBox_Area(B, H, t)
    assert A == pt.approx(0.0056, rel=1e-5)  # m^2

#test StructSize38

def test_volume():
    A = 0.0056  # m^2
    L = 1.0     # m 
    V = Volume(A, L)
    assert V == pt.approx(0.0056, rel=1e-5)  # m^3


if __name__ == "__main__":
    pt.main([__file__])
