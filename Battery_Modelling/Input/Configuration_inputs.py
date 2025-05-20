import numpy as np
#Power equation: https://www.spinningwing.com/the-helicopter/momentum-theory/
#-------------Same across Configurations-------------------
W = 200 #inputs0 N
eta = 0.8 #inputs1



#-------------Different across Configurations-------------------
# UFC_MMA_1 Helicopter
CD0_MMA1 =0.105 #inputs 2 https://dspace-erf.nlr.nl/server/api/core/bitstreams/0a756857-3708-4250-9524-bdbcc0020d33/content 
S_parasite_MMA1 = 0.16 #inputs 3 http://eprints.gla.ac.uk/116394/1/116394.pdf
diameter_MMA1 = 1.041 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/9dc27553-90f0-4209-b744-0adee5c75f27/content 
r_MMA1 = diameter_MMA1/2 #inputs 4
A_prop_MMA1 = (r_MMA1)**2*np.pi# inputs 5
N_blades_MMA1 = 2 #inputs 6
chord_factor = 3.5 #https://www.dji.com/nl/support/product/t20
chord_blade_MMA1 = r_MMA1/chord_factor #inputs 7
cd_blade_MMA1 = 0.014 #inputs 8
omega_MMA1 = 300 #inputs 9 ChatGPT this
solidity_MMA1 = 0.05 #inputs 10

#UFC_MMA_2 Quadcopter
CD0_MMA2 = 0.425 #inputs 2 https://www.icas.org/icas_archive/ICAS2020/data/papers/ICAS2020_0781_paper.pdf
Stop_MMA2 = 0.45 #inputs 3 https://www.icas.org/icas_archive/ICAS2020/data/papers/ICAS2020_0781_paper.pdf
Sfront_MMA2 = 0.35#inputs 4
A_prop_MMA2 = A_prop_MMA1 #inputs 6
N_blades_MMA2 = N_blades_MMA1 #inputs 7
cd_blade_MMA2 = cd_blade_MMA1 #inputs 9
omega_MMA2 = omega_MMA1 #inputs 10
solidity_MMA2 = solidity_MMA1#inputs 11
numberengine_MMA2 = 4 #inputs 12
r_MMA2 = np.sqrt(A_prop_MMA2/numberengine_MMA2/np.pi) #inputs 5
chord_blade_MMA2 = r_MMA2/chord_factor #inputs 8

#UFC_MMA_3 Osprey
CD0_MMA3 = 0.0264 #inputs 2 https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
piAe_MMA3 = 20.41 #inputs 3 https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
S_wing_MMA3 = 0.5*2 #inputs 4 m^2 x2 compared to research (cuz reearch is 10kg, we go 20)
CLmax_MMA3 = 2*0.9 #1.3824 *0.9 #inputs 5 + safety margin https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
#clmax is 2 says: https://www.sciencedirect.com/science/article/pii/S2090447922004051
wing_eff_prop_on_MMA3 = 0.7 #inputs 7 
V_stall_MMA3 = np.sqrt(2*W/(1.225*S_wing_MMA3*CLmax_MMA3))#inputs 8
A_prop_MMA3 = A_prop_MMA1#(r_MMA3)**2*np.pi #inputs 9
N_blades_MMA3 = N_blades_MMA1 #inputs 10
cd_blade_MMA3 = cd_blade_MMA1 #inputs 12
omega_MMA3 = omega_MMA1 #inputs 13
solidity_MMA3 = solidity_MMA1 #inputs 14
numberengines_MMA3=2 #inputs 15
r_MMA3 = np.sqrt(A_prop_MMA3/numberengines_MMA3/np.pi) #inputs 5 #0.21*2 #inputs 6 x2 compared to research https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
chord_blade_MMA3 = r_MMA3/chord_factor #inputs 11

#UFC_MMA_4 Yangda
CD0_MMA4 = CD0_MMA3 #inputs 2 same as osprey
piAe_MMA4 = piAe_MMA3 #inputs 3 same as osprey
S_MMA4 = 1.25 #inputs 4 m^2 x2.5 compared to research (cuz reearch is 10kg, we go 25)
CLmax_MMA4 =  CLmax_MMA3#1.3824 *0.9 #inputs 5 + safety margin same as osprey
wing_eff_prop_on_MMA4 = wing_eff_prop_on_MMA3 #inputs 7 
prop_efficiency_MMA4 = 0.8#inputs 8
V_stall_MMA4 = np.sqrt(2*W/(1.225*S_MMA4*CLmax_MMA4))#inputs 9
A_prop_MMA4 = A_prop_MMA3 #inputs 10
N_blades_MMA4 = N_blades_MMA1 #inputs 11
cd_blade_MMA4 = cd_blade_MMA1 #inputs 13
omega_MMA4 = omega_MMA1 #inputs 14
solidity_MMA4 = solidity_MMA1#inputs 15
numberengines_vertical_MMA4 = 4 #inputs 16
numberengines_horizontal_MMA4 = 1 #inputs 17
r_MMA4 = np.sqrt(A_prop_MMA4/(numberengines_vertical_MMA4)/np.pi) #inputs 5
chord_blade_MMA4 = r_MMA4/chord_factor #inputs 12
 #inputs 6same as osprey

inputs_list_original = [[W,eta,CD0_MMA1,S_parasite_MMA1,r_MMA1,A_prop_MMA1,N_blades_MMA1,chord_blade_MMA1,cd_blade_MMA1,omega_MMA1,solidity_MMA1],
                        [W,eta,CD0_MMA2,Stop_MMA2,Sfront_MMA2,r_MMA2,A_prop_MMA2,N_blades_MMA2,chord_blade_MMA2,cd_blade_MMA2,omega_MMA2,solidity_MMA2,numberengine_MMA2],
                        [W,eta,CD0_MMA3,piAe_MMA3,S_wing_MMA3, CLmax_MMA3,r_MMA3,wing_eff_prop_on_MMA3,V_stall_MMA3,A_prop_MMA3,N_blades_MMA3,chord_blade_MMA3,cd_blade_MMA3,omega_MMA3,solidity_MMA3,numberengines_MMA3],
                        [W,eta,CD0_MMA4,piAe_MMA4,S_MMA4,CLmax_MMA4,r_MMA4,wing_eff_prop_on_MMA4,prop_efficiency_MMA4,V_stall_MMA4,A_prop_MMA4,N_blades_MMA4,chord_blade_MMA4,cd_blade_MMA4,omega_MMA4,solidity_MMA4,numberengines_vertical_MMA4,numberengines_horizontal_MMA4]]

def largest_real_positive_root(roots):
    real_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]
    if not real_roots:
        return 0  # or raise an exception or return some sentinel value
    return max(real_roots)