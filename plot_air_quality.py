from datetime import datetime
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import requests

# 1. Load API Key
load_dotenv()
API_KEY = os.getenv("AIRNOW_API_KEY")

# 2. Define location (Central Park / Upper West Side zip code)
zip_code = "10024"

# 3. Set start date (Jan 1, 2024) and current date as end date
start_date = datetime(2024, 1, 1)
end_date = datetime.today()

current_date = start_date
all_data = []

print(
    f"Fetching monthly historical air quality data for ZIP {zip_code} from"
    f" {start_date.strftime('%Y-%m-%d')} to present..."
)


def add_month(dt):
  month = dt.month + 1
  year = dt.year
  if month > 12:
    month = 1
    year += 1
  return datetime(year, month, 1)


# 4. Loop through month by month up to today (2026)
while current_date <= end_date:
  date_str = current_date.strftime("%Y-%m-%d")
  url = f"https://www.airnowapi.org/aq/observation/zipCode/historical/?format=application/json&zipCode={zip_code}&date={date_str}T00-0000&API_KEY={API_KEY}"

  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    if data:
      for entry in data:
        all_data.append({
            "Date": entry.get("DateObserved").strip(),
            "Parameter": entry.get("ParameterName"),
            "AQI": entry.get("AQI"),
            "Category": entry.get("Category", {}).get("Name"),
        })

  current_date = add_month(current_date)

# 5. Convert and verify
if all_data:
  df = pd.DataFrame(all_data)

  print(f"\nSuccess! Total rows collected: {len(df)}")
  print("\n--- LATEST DATA (2026 Check) ---")
  print(df.tail(6))  # This will show you it reached 2026!

  # Save to CSV
  df.to_csv("central_park_monthly_air_quality.csv", index=False)

  # 6. Quickly filter for PM2.5 and plot the whole 2024-2026 timeline
  pm25_df = df[df["Parameter"] == "PM2.5"].copy()
  pm25_df["Date"] = pd.to_datetime(pm25_df["Date"])

  plt.figure(figsize=(11, 5))
  plt.plot(
      pm25_df["Date"],
      pm25_df["AQI"],
      marker="o",
      linestyle="-",
      color="#2ca02c",
      linewidth=2,
  )

  # Mark the congestion pricing launch (Jan 2025)
  plt.axvline(
      pd.to_datetime("2025-01-05"),
      color="red",
      linestyle="--",
      label="Congestion Pricing Launch (Jan 2025)",
  )

  plt.title(
      "Central Park Monthly PM2.5 AQI (2024 - Present)", fontsize=13, pad=12
  )
  plt.xlabel("Date", fontsize=11)
  plt.ylabel("AQI Value", fontsize=11)
  plt.grid(True, linestyle="--", alpha=0.6)
  plt.legend()
  plt.tight_layout()
  plt.show()

else:
  print("No data collected. Check your API key.")