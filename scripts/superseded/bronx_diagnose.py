import pandas as pd

def load(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    return df

b2024 = load('data/total_traffic_count_2024_bronx.csv')
b2025 = load('data/total_traffic_count_2025_bronx.csv')

dates_2024 = set(zip(b2024['m'], b2024['d']))
dates_2025 = set(zip(b2025['m'], b2025['d']))
common_dates = dates_2024 & dates_2025
print(f"Common calendar days: {len(common_dates)}")

segments_2024 = set(b2024['segmentid'])
segments_2025 = set(b2025['segmentid'])
common_segments = segments_2024 & segments_2025
print(f"Common segments: {len(common_segments)}")
print(f"2024 segments: {sorted(segments_2024)}")
print(f"2025 segments: {sorted(segments_2025)}")