import pandas as pd
import numpy as np

df_releases = pd.read_csv("release_data.csv")

df_releases["median_interval"] = df_releases.groupby("repo")["interval_days"].transform(np.median)

df_releases["delay_threshold"] = df_releases["median_interval"] * 1.5

df_releases["is_delayed"] = df_releases["interval_days"] > df_releases["delay_threshold"]

df_releases["release_date"] = pd.to_datetime(df_releases["release_date"])
df_releases["interval_days"] = df_releases["interval_days"].astype(int)
df_releases["is_delayed"] = df_releases["is_delayed"].astype(int)  

df_releases.to_csv("release_data_with_delays.csv", index=False)
print("Release data with delays saved to release_data_with_delays.csv")

print("\nSummary of delays by repository:")
delay_summary = df_releases.groupby("repo").agg({
    "interval_days": ["mean", "median", "max"],
    "is_delayed": "sum"
}).reset_index()
delay_summary.columns = ["repo", "mean_interval", "median_interval", "max_interval", "delayed_count"]
print(delay_summary)