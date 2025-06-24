import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

# Time array from 0 to 7
t = np.linspace(0, 7, 500)

fig, ax = plt.subplots(figsize=(10,6))

# Green curved lines (approximate quarter circle shapes for three segments)
for start in [0, 3, 5]:
    segment_t = np.linspace(start, start+2, 200)
    # Using sqrt curve to mimic the shape: y = 100 * sqrt((t - start)/2)
    green_curve = 100 * np.sqrt((segment_t - start)/2)
    ax.plot(segment_t, green_curve, color='green', linewidth=5)

# Brown rectangular lines (step function like shapes)
for start in [0, 3, 5]:
    rect_x = [start, start+0.5, start+0.5, start+1.5, start+1.5, start+2, start+2]
    rect_y = [0, 0, 70, 70, 40, 40, 0]
    ax.plot(rect_x, rect_y, color='brown', linewidth=5)

# Black smooth curves (approximate with exponential approach)
for start in [0, 3, 5]:
    black_t = np.linspace(start, start+2, 200)
    # Approximate black curve shape (scaled sigmoid)
    black_curve = 100 / (1 + np.exp(-2*(black_t - (start+1))))
    ax.plot(black_t, black_curve, color='black', linewidth=1)

# Labels and limits
ax.set_xlabel('Time')
ax.set_ylabel('Battery %')
ax.set_title('Battery % over Time')
ax.set_xlim(0, 7)
ax.set_ylim(0, 100)
ax.grid(True)

plt.show()
