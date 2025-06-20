import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data from CSV
df = pd.read_csv('Battery_density/data.csv')

# Check that required columns exist
required_columns = {'Year', 'Energy Density (Wh/kg)', 'Battery Type'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"CSV must contain columns: {required_columns}")

plt.figure(figsize=(10, 6))

# Assign a color to each battery type
battery_types = df['Battery Type'].unique()
# Ensure 'Solid-State' is first in the order
battery_types = sorted(battery_types, key=lambda x: (x != 'Solid-State', x))
colors = plt.cm.tab10.colors  # or use another colormap if >10 types
color_map = {bt: colors[i % len(colors)] for i, bt in enumerate(battery_types)}

handles = []
labels = []

for battery_type, group in df.groupby('Battery Type'):
    color = color_map[battery_type]
    sc = plt.scatter(group['Year'], group['Energy Density (Wh/kg)'], label=battery_type, color=color)
    # Fit a linear trend line
    x = group['Year']
    y = group['Energy Density (Wh/kg)']
    coeffs = np.polyfit(x, y, 1)
    trend = np.poly1d(coeffs)
    # Plot trendline for actual data range
    ln1, = plt.plot(x, trend(x), linestyle='-', color=color, label=f'{battery_type} Trend (Actual)')
    # Plot extended trendline to 2050
    x_extended = np.arange(x.min(), 2050)
    ln2, = plt.plot(x_extended, trend(x_extended), linestyle='--', color=color, label=f'{battery_type} Trend (to 2050)')
    # Collect handles and labels for custom legend
    handles.extend([sc, ln1, ln2])
    labels.extend([battery_type, f'{battery_type} Trend (Actual)', f'{battery_type} Trend (to 2050)'])

# Mark 2032 with a vertical red line
plt.axvline(2032, color='black', linestyle='-', linewidth=2, label='2032')
plt.text(2032 + 0.5, plt.ylim()[1]*0.95, 'Entry into Service - 2032', color='black', va='top', fontsize=10)

# Custom legend: ensure 'Solid-State' is first
# Get all legend handles/labels, but move 'Solid-State' and its trends to the front
legend_items = list(zip(labels, handles))
solid_state_items = [item for item in legend_items if item[0].startswith('Solid-State')]
other_items = [item for item in legend_items if not item[0].startswith('Solid-State')]
# Add the vertical line label at the end if not already present

plt.legend([item[1] for item in solid_state_items + other_items] + [plt.Line2D([], [], color='red', linestyle='-', linewidth=2)],
           [item[0] for item in solid_state_items + other_items] + ['2032'],
           title='Battery Type', fontsize='small')

plt.xlabel('Year')
plt.ylabel('Energy Density [Wh/kg]')
plt.title('Energy Density Over Time by Battery Type')
plt.grid(True)
plt.tight_layout()
plt.show()
