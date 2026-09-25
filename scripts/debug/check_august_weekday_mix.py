import pandas as pd

for year, dates in [(2024, ("2024-08-05", "2024-08-11")), (2025, ("2025-08-05", "2025-08-11")), (2026, ("2026-08-05", "2026-08-11"))]:
    date_range = pd.date_range(dates[0], dates[1])
    weekdays = sum(1 for d in date_range if d.weekday() < 5)
    weekends = sum(1 for d in date_range if d.weekday() >= 5)
    print(f"{year}: {date_range[0].strftime('%A')} to {date_range[-1].strftime('%A')} — {weekdays} weekdays, {weekends} weekend days")