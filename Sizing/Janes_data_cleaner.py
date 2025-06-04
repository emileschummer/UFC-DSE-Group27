import pandas as pd
import re

# 1. Paths – adjust if needed
in_path  = r'c:\Users\marco\Desktop\Janes analysis\pivoted_equipment_specs.csv'
out_path = r'c:\Users\marco\Desktop\Janes analysis\pivoted_equipment_specs_final.csv'

# 2. Load data
df = pd.read_csv(in_path)

# 3. Helpers
def clean_ceiling(val):
    if pd.isna(val): return pd.NA
    m = re.search(r'([\d,]+)\s*m\b', str(val))
    return int(m.group(1).replace(',', '')) if m else pd.NA

def knots_to_m_s(val):
    if pd.isna(val): return pd.NA
    m = re.search(r'([\d\.]+)\s*kt', str(val))
    return round(float(m.group(1)) * 0.514444, 2) if m else pd.NA

def duration_to_hours(val):
    if pd.isna(val): return pd.NA
    s = str(val)
    hrs  = int(re.search(r'(\d+)\s*hr',  s).group(1)) if re.search(r'(\d+)\s*hr',  s) else 0
    mins = int(re.search(r'(\d+)\s*min', s).group(1)) if re.search(r'(\d+)\s*min', s) else 0
    return round(hrs + mins/60, 2)

def wing_area_to_m2(val):
    if pd.isna(val): return pd.NA
    m = re.search(r'([\d\.]+)\s*m\b', str(val))
    return float(m.group(1)) if m else pd.NA

def weight_to_kg(val):
    if pd.isna(val): return pd.NA
    m = re.search(r'([\d\.]+)\s*kg', str(val))
    return float(m.group(1)) if m else pd.NA

def length_to_m(val):
    if pd.isna(val): return pd.NA
    s    = str(val)
    # mm → m
    m_mm = re.search(r'([\d,\.]+)\s*mm\b', s)
    if m_mm:
        return round(float(m_mm.group(1).replace(',', ''))/1000, 3)
    # m → m
    m_m = re.search(r'([\d\.]+)\s*m\b', s)
    return float(m_m.group(1)) if m_m else pd.NA

def km_value(val):
    if pd.isna(val): return pd.NA
    m = re.search(r'([\d,\.]+)\s*km\b', str(val))
    return float(m.group(1).replace(',', '')) if m else pd.NA

def climb_to_m_s(val):
    if pd.isna(val): return pd.NA
    m = re.search(r'([\d,\.]+)\s*m/min', str(val))
    return round(float(m.group(1).replace(',', ''))/60, 2) if m else pd.NA

# 4. Apply conversions

# Ceiling fields
for col in ['Absolute ceiling', 'Service ceiling', 'Operating altitude']:
    df[f'{col} [m]'] = df[col].apply(clean_ceiling)

# Speed fields
for col in [
    'Cruising speed', 'Loitering speed',
    'Max level speed', 'Max operating speed',
    'Never-exceed speed', 'Stalling speed'
]:
    df[f'{col} [m/s]'] = df[col].apply(knots_to_m_s)

# Rate of climb
df['Rate of climb [m/s]'] = df['Rate of climb'].apply(climb_to_m_s)

# Endurance
df['Endurance [h]'] = df['Endurance'].apply(duration_to_hours)

# Wing area
df['Gross wing area [m2]'] = df['Gross wing area'].apply(wing_area_to_m2)

# Weights
for col in [
    'Max T-O weight', 'Max payload',
    'Operating weight, empty', 'Payload with max fuel',
    'Weight empty'
]:
    df[f'{col} [kg]'] = df[col].apply(weight_to_kg)

# Length
df['Length, overall [m]'] = df['Length, overall'].apply(length_to_m)

# Wing span
df['Wing span [m]'] = df['Wing span'].apply(length_to_m)

# Range & radius
df['Radius of operation [km]'] = df['Radius of operation'].apply(km_value)
df['Range [km]']               = df['Range'].apply(km_value)

# 5. Drop original text columns
df.drop(columns=[
    'Absolute ceiling', 'Service ceiling', 'Operating altitude',
    'Cruising speed', 'Loitering speed', 'Max level speed',
    'Max operating speed', 'Never-exceed speed', 'Stalling speed',
    'Rate of climb', 'Endurance', 'Gross wing area',
    'Max T-O weight', 'Max payload', 'Operating weight, empty',
    'Payload with max fuel', 'Weight empty', 'Length, overall',
    'Wing span', 'Radius of operation', 'Range'
], inplace=True)

# 6. Save final CSV
df.to_csv(out_path, index=False)
print(f'All conversions done. Final file saved to:\n{out_path}')
