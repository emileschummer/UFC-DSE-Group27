import pandas as pd

# 1. Read in your original data
df = pd.read_csv(r'c:\Users\marco\Desktop\Janes analysis\ExportSheet_data.csv')

# 2. Pivot so that each Max. Equipment Designation is a row
#    and each unique Specs Combi is its own column with the concatenated Concat Data
pivot = (
    df
    .groupby(['Max. Equipment Designation', 'Specs Combi'])['Concat Data']
    .agg(lambda vals: ' '.join(vals.astype(str)))
    .unstack(fill_value='')
    .reset_index()
)

# 3. Inspect the first few rows
print(pivot.head())

# 4. Write the full pivoted table back to CSV
output_path = r'c:\Users\marco\Desktop\Janes analysis\pivoted_equipment_specs.csv'
pivot.to_csv(output_path, index=False)
print(f'Pivoted table saved to {output_path}')
