import pandas as pd

# Load dataset
df = pd.read_csv('data/manhattan_jan_24_25_26_full.csv')
df.columns = [c.lower() for c in df.columns]
df['vol'] = pd.to_numeric(df['vol'], errors='coerce').fillna(0)

# Build datetime and day flags
df['date'] = pd.to_datetime(
    df['yr'].astype(str) + '-' + 
    df['m'].astype(str).str.zfill(2) + '-' + 
    df['d'].astype(str).str.zfill(2)
)
df['day_of_week'] = df['date'].dt.dayofweek  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
df['day_name'] = df['date'].dt.day_name()

# Keep strictly Monday - Friday (5 weekdays per year)
df_weekdays = df[df['day_of_week'] < 5].copy()

# Summary statistics per segment
weekday_comparison = (
    df_weekdays
    .groupby(['yr', 'segmentid', 'street', 'direction'])
    .agg(
        days_counted=('d', 'nunique'),
        slots_counted=('vol', 'count'),
        total_volume=('vol', 'sum'),
        mean_15min_vol=('vol', 'mean'),
        peak_15min_vol=('vol', 'max')
    )
    .reset_index()
)

print(weekday_comparison.to_string(index=False))