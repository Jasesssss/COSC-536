import pandas as pd
import numpy as np

# Load release data from Step 5
df_releases = pd.read_csv("release_data.csv")

# Calculate median interval per repository
df_releases["median_interval"] = df_releases.groupby("repo")["interval_days"].transform(np.median)

# Define delay threshold (1.5× median)
df_releases["delay_threshold"] = df_releases["median_interval"] * 1.5

# Flag releases as delayed if interval exceeds threshold
df_releases["is_delayed"] = df_releases["interval_days"] > df_releases["delay_threshold"]

# Ensure data types are clean
df_releases["release_date"] = pd.to_datetime(df_releases["release_date"])
df_releases["interval_days"] = df_releases["interval_days"].astype(int)
df_releases["is_delayed"] = df_releases["is_delayed"].astype(int)  # 1 = delayed, 0 = not delayed

# Save updated dataset
df_releases.to_csv("release_data_with_delays.csv", index=False)
print("Release data with delays saved to release_data_with_delays.csv")

# Optional: Summary stats
print("\nSummary of delays by repository:")
delay_summary = df_releases.groupby("repo").agg({
    "interval_days": ["mean", "median", "max"],
    "is_delayed": "sum"
}).reset_index()
delay_summary.columns = ["repo", "mean_interval", "median_interval", "max_interval", "delayed_count"]
print(delay_summary)