import numpy as np
#-------------Same across Configurations-------------------
W = 250 #inputs0 N
eta = 0.8 #inputs1
#-------------Different across Configurations-------------------
# UFC_MMA_1 Helicopter
CD_MMA1 =0.105 #inputs 2 https://dspace-erf.nlr.nl/server/api/core/bitstreams/0a756857-3708-4250-9524-bdbcc0020d33/content 
S_MMA1 = 0.16 #inputs 3 http://eprints.gla.ac.uk/116394/1/116394.pdf
diameter_MMA1 = 1.041 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/9dc27553-90f0-4209-b744-0adee5c75f27/content 
A_MMA1 = (diameter_MMA1/2)**2*np.pi# inputs 4
