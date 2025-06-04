import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

cols = [
    'Service ceiling [m]', 'Operating altitude [m]', 'Cruising speed [m/s]',
    'Loitering speed [m/s]', 'Max level speed [m/s]', 'Max operating speed [m/s]',
    'Never-exceed speed [m/s]', 'Stalling speed [m/s]', 'Rate of climb [m/s]',
    'Endurance [h]', 'Gross wing area [m2]', 'Max T-O weight [kg]',
    'Max payload [kg]', 'Operating weight, empty [kg]', 'Payload with max fuel [kg]',
    'Weight empty [kg]', 'Length, overall [m]', 'Wing span [m]',
    'Radius of operation [km]', 'Range [km]'
]

# --- CORRELATION MATRIX HEATMAP ---
# Load all columns for correlation analysis
df_corr = pd.read_csv(
    r'C:\Users\marco\Desktop\Janes analysis\pivoted_equipment_specs_final.csv',
    usecols=cols
)

# Compute correlation matrix (using only numeric columns)
corr = df_corr.corr(numeric_only=True)

plt.figure(figsize=(14, 10))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": .8})
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig(r"C:\Users\marco\Desktop\Janes analysis\correlation_matrix.png", dpi=300)
plt.close()
print("Correlation matrix saved as correlation_matrix.png in", os.path.dirname(r"C:\Users\marco\Desktop\Janes analysis\correlation_matrix.png"))

# 1. USER-DEFINED: pick exactly two columns here
x_col = 'Max payload [kg]'   # ← change this to your chosen x-axis column
y_col = 'Max T-O weight [kg]'         # ← change this to your chosen y-axis column

# 2. LOAD DATA: only pull in the two selected columns
df = pd.read_csv(
    r'C:\Users\marco\Desktop\Janes analysis\pivoted_equipment_specs_final.csv',
    usecols=[x_col, y_col]
)

# 3. FILTER: drop rows where either x or y is NaN or ≤ 0
df = df.dropna(subset=[x_col, y_col])
df = df[(df[x_col] > 0) & (df[y_col] > 0)]

# 3a. CHECK: ensure there is data left after filtering
if df.empty:
    raise ValueError(f"After filtering, no data left for columns '{x_col}' and '{y_col}'.")

# 4. EXTRACT NUMPY ARRAYS
x = df[x_col].values
y = df[y_col].values

# For smooth plotting of fitted curves
x_line = np.linspace(x.min(), x.max(), 200)

# 5. COMPUTE TOTAL SUM OF SQUARES
ss_tot = np.sum((y - np.mean(y)) ** 2)

# 5a. Exponential fit:   y ≈ a * exp(b * x)
try:
    log_y = np.log(y)
    b_exp, log_a_exp = np.polyfit(x, log_y, 1)
    a_exp = np.exp(log_a_exp)
    y_line_exp = a_exp * np.exp(b_exp * x_line)
    y_pred_exp = a_exp * np.exp(b_exp * x)
    ss_res_exp = np.sum((y - y_pred_exp) ** 2)
    r2_exp = 1 - ss_res_exp / ss_tot
except Exception:
    y_line_exp = None
    r2_exp = np.nan

# 5b. Logarithmic fit:   y ≈ a + b * log(x)
try:
    log_x = np.log(x)
    b_log, a_log = np.polyfit(log_x, y, 1)
    y_line_log = a_log + b_log * np.log(x_line)
    y_pred_log = a_log + b_log * np.log(x)
    ss_res_log = np.sum((y - y_pred_log) ** 2)
    r2_log = 1 - ss_res_log / ss_tot
except Exception:
    y_line_log = None
    r2_log = np.nan

# 5c. Square-root fit:   y ≈ a + b * sqrt(x)
try:
    sqrt_x = np.sqrt(x)
    b_sqrt, a_sqrt = np.polyfit(sqrt_x, y, 1)
    y_line_sqrt = a_sqrt + b_sqrt * np.sqrt(x_line)
    y_pred_sqrt = a_sqrt + b_sqrt * np.sqrt(x)
    ss_res_sqrt = np.sum((y - y_pred_sqrt) ** 2)
    r2_sqrt = 1 - ss_res_sqrt / ss_tot
except Exception:
    y_line_sqrt = None
    r2_sqrt = np.nan

# 5d. Linear fit:   y ≈ m * x + b
try:
    m_lin, b_lin = np.polyfit(x, y, 1)
    y_line_lin = m_lin * x_line + b_lin
    y_pred_lin = m_lin * x + b_lin
    ss_res_lin = np.sum((y - y_pred_lin) ** 2)
    r2_lin = 1 - ss_res_lin / ss_tot
except Exception:
    y_line_lin = None
    r2_lin = np.nan

# 5e. Quadratic fit:   y ≈ a2 * x^2 + a1 * x + a0
try:
    a2_quad, a1_quad, a0_quad = np.polyfit(x, y, 2)
    y_line_quad = a2_quad * x_line**2 + a1_quad * x_line + a0_quad
    y_pred_quad = a2_quad * x**2 + a1_quad * x + a0_quad
    ss_res_quad = np.sum((y - y_pred_quad) ** 2)
    r2_quad = 1 - ss_res_quad / ss_tot
except Exception:
    y_line_quad = None
    r2_quad = np.nan

# 5f. Cubic fit:   y ≈ a3 * x^3 + a2 * x^2 + a1 * x + a0
try:
    a3_cub, a2_cub, a1_cub, a0_cub = np.polyfit(x, y, 3)
    y_line_cub = a3_cub * x_line**3 + a2_cub * x_line**2 + a1_cub * x_line + a0_cub
    y_pred_cub = a3_cub * x**3 + a2_cub * x**2 + a1_cub * x + a0_cub
    ss_res_cub = np.sum((y - y_pred_cub) ** 2)
    r2_cub = 1 - ss_res_cub / ss_tot
except Exception:
    y_line_cub = None
    r2_cub = np.nan

# --- PRINT REGRESSION EQUATIONS ---
print("\n--- Regression Equations ---")
if y_line_exp is not None:
    print(f"Exponential: y = {a_exp:.4g} * exp({b_exp:.4g} * x)")
else:
    print("Exponential: Fit failed.")

if y_line_log is not None:
    print(f"Logarithmic: y = {a_log:.4g} + {b_log:.4g} * log(x)")
else:
    print("Logarithmic: Fit failed.")

if y_line_sqrt is not None:
    print(f"Square-root: y = {a_sqrt:.4g} + {b_sqrt:.4g} * sqrt(x)")
else:
    print("Square-root: Fit failed.")

if y_line_lin is not None:
    print(f"Linear: y = {m_lin:.4g} * x + {b_lin:.4g}")
else:
    print("Linear: Fit failed.")

if y_line_quad is not None:
    print(f"Quadratic: y = {a2_quad:.4g} * x^2 + {a1_quad:.4g} * x + {a0_quad:.4g}")
else:
    print("Quadratic: Fit failed.")

if y_line_cub is not None:
    print(f"Cubic: y = {a3_cub:.4g} * x^3 + {a2_cub:.4g} * x^2 + {a1_cub:.4g} * x + {a0_cub:.4g}")
else:
    print("Cubic: Fit failed.")

# 6. PLOT
plt.figure(figsize=(8, 5))
plt.scatter(x, y, label='Data', alpha=0.7)

if y_line_exp is not None:
    plt.plot(x_line, y_line_exp, label=f'Exp Fit (R²={r2_exp:.3f})')
if y_line_log is not None:
    plt.plot(x_line, y_line_log, label=f'Log Fit (R²={r2_log:.3f})')
if y_line_sqrt is not None:
    plt.plot(x_line, y_line_sqrt, label=f'Sqrt Fit (R²={r2_sqrt:.3f})')
if y_line_lin is not None:
    plt.plot(x_line, y_line_lin, label=f'Linear Fit (R²={r2_lin:.3f})')
if y_line_quad is not None:
    plt.plot(x_line, y_line_quad, label=f'Quadratic Fit (R²={r2_quad:.3f})')
if y_line_cub is not None:
    plt.plot(x_line, y_line_cub, label=f'Cubic Fit (R²={r2_cub:.3f})')

plt.xlabel(x_col)
plt.ylabel(y_col)
plt.title(f'{y_col} vs {x_col}')
plt.legend()
plt.tight_layout()
plt.show()