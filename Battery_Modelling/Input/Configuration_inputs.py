import numpy as np
#Power equation: https://www.spinningwing.com/the-helicopter/momentum-theory/?utm_source=chatgpt.com 
#-------------Same across Configurations-------------------
W = 250 #inputs0 N
eta = 0.8 #inputs1


#-------------Different across Configurations-------------------
# UFC_MMA_1 Helicopter
CD_MMA1 =0.105 #inputs 2 https://dspace-erf.nlr.nl/server/api/core/bitstreams/0a756857-3708-4250-9524-bdbcc0020d33/content 
S_MMA1 = 0.16 #inputs 3 http://eprints.gla.ac.uk/116394/1/116394.pdf
diameter_MMA1 = 1.041 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/9dc27553-90f0-4209-b744-0adee5c75f27/content 
A_MMA1 = (diameter_MMA1/2)**2*np.pi# inputs 4

#UFC_MMA_2 Quadcopter
CD_MMA2 = 0.425 #inputs 5 https://www.icas.org/icas_archive/ICAS2020/data/papers/ICAS2020_0781_paper.pdf
Stop_MMA2 = 0.45 #https://www.icas.org/icas_archive/ICAS2020/data/papers/ICAS2020_0781_paper.pdf
Sfront_MMA2 = 0.35
totalA_MMA2 = (1.041/2)**2*np.pi


#UFC_MMA_3 Osprey
CD0_MMA3 = 0.0264 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
piAe_MMA3 = 20.41 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
S_MMA3 = 1.25 #m^2 x2.5 compared to research (cuz reearch is 10kg, we go 25)
CLmax_MMA3 = 1.3824 *0.9 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
#clmax is 2 says: https://www.sciencedirect.com/science/article/pii/S2090447922004051
r_MMA3 = 0.21 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle

#UFC_MMA_4 Yangda
CD0_MMA4 = 0.0264 #same as osprey
piAe_MMA4 = 20.41 #same as osprey
S_MMA4 = 1.25 #m^2 x2.5 compared to research (cuz reearch is 10kg, we go 25)
CLmax_MMA4 = 1.3824 *0.9 #same as osprey
r_MMA4 = r_MMA3 #same as osprey
prop_efficiency_MMA4 = 0.8

