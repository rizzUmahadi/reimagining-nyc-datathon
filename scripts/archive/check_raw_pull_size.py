import json
import pandas as pd

with open('data/manhattan_24_25_26_raw.json') as f:
    new_data = json.load(f)

new_df = pd.DataFrame(new_data)

print(f"Total rows in this file: {len(new_df)}")
print("\nRows per year:")
print(new_df['yr'].value_counts())

print("\nDistinct segments per year:")
print(new_df.groupby('yr')['segmentid'].nunique())