import pandas as pd
import random 
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

TeamA = [100]
TeamB = [100]

TeamAInstant = 100  # Example starting value, you can adjust this
TeamBInstant = 100  # Example starting value, you can adjust this

T = [0]

for i in range(60*2):
    TeamAInstant = TeamAInstant - i * 0.011
    TeamBInstant = TeamBInstant - i * 0.011

    TeamA.append(TeamAInstant)
    TeamB.append(TeamBInstant)
    T.append(i)

#plt.figure(figsize=(10, 6))
plt.plot(T, TeamA, label='Team A')
plt.plot(T, TeamB, label='Team B')
plt.xlabel('Time')
plt.ylabel('Battery')
plt.title('Comparison of Team A and Team B over Time')
plt.legend()
plt.show()
