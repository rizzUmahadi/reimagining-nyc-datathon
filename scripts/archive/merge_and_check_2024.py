import json
import pandas as pd

# ---------------------------------------------------------------------------
# STEP 1: Load your existing 2024/2025 Manhattan data (already has capitalized columns)
# ---------------------------------------------------------------------------
existing_2024 = pd.read_csv('data/total_traffic_count_2024_manhattan.csv')
existing_2025 = pd.read_csv('data/total_traffic_count_2025_manhattan.csv')

print("Existing data columns:", existing_2024.columns.tolist())

# ---------------------------------------------------------------------------
# STEP 2: Load the new JSON file you saved from your browser
# ---------------------------------------------------------------------------
# CHANGE THIS PATH to wherever you actually saved the file (Cmd+S from browser)
with open('data/manhattan_24_25_26_raw.json') as f:
    new_data = json.load(f)

new_df = pd.DataFrame(new_data)
print("New data columns:", new_df.columns.tolist())

# ---------------------------------------------------------------------------
# STEP 3: Rename the new data's columns to match your existing files
# ---------------------------------------------------------------------------
# This dictionary says: "wherever you see the key on the left, rename it to
# the value on the right." We're matching the new pull's lowercase names
# to your existing files' capitalized names.
rename_map = {
    'yr': 'Yr',
    'm': 'M',
    'd': 'D',
    'hh': 'HH',
    'mm': 'MM',
    'vol': 'Vol',
    'boro': 'Boro',
    'segmentid': 'SegmentID',
    'wktgeom': 'WktGeom',
    'street': 'street',
    'fromst': 'fromSt',
    'tost': 'toSt',
    'direction': 'Direction',
    'requestid': 'RequestID',
}

new_df = new_df.rename(columns=rename_map)

print("\nNew data columns AFTER renaming:", new_df.columns.tolist())

# ---------------------------------------------------------------------------
# STEP 4: Verify both column lists actually match now
# ---------------------------------------------------------------------------
existing_cols = set(existing_2024.columns)
new_cols = set(new_df.columns)

print("\nColumns in existing but NOT in new:", existing_cols - new_cols)
print("Columns in new but NOT in existing:", new_cols - existing_cols)

# ---------------------------------------------------------------------------
# STEP 5: Check data types match, not just names
# ---------------------------------------------------------------------------
print("\nExisting Vol dtype:", existing_2024['Vol'].dtype)
print("New Vol dtype (before conversion):", new_df['Vol'].dtype)

new_df['Vol'] = pd.to_numeric(new_df['Vol'], errors='coerce')

print("New Vol dtype (after conversion):", new_df['Vol'].dtype)

# ---------------------------------------------------------------------------
# STEP 6: Now check what you actually have for 2024
# ---------------------------------------------------------------------------
year_2024 = new_df[new_df['Yr'] == '2024']
print(f"\n2024 rows in new pull: {len(year_2024)}")
print(f"2024 distinct segments in new pull: {year_2024['SegmentID'].nunique()}")