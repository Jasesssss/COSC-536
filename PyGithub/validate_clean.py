import pandas as pd

df_final = pd.read_csv("final_dataset.csv")

df_final["release_date"] = pd.to_datetime(df_final["release_date"])

print("Validating delays...")
delayed_summary = df_final[df_final["is_delayed"] == 1].groupby("repo").agg({
    "interval_days": "mean",
    "open_issues": "mean",
    "avg_pr_comments": "mean"
}).reset_index()
print("Average stats for delayed releases by repo:")
print(delayed_summary)

print("\nRemoving outliers (interval_days > 365)...")
outliers = df_final["interval_days"] > 365
print(f"Found {outliers.sum()} outliers")
df_cleaned = df_final[~outliers].copy()

print("\nImputing missing data...")
for column in ["open_issues", "avg_pr_comments"]:
    repo_medians = df_cleaned[df_cleaned[column] > 0].groupby("repo")[column].median()
    overall_median = df_cleaned[column].median()
    df_cleaned[column] = df_cleaned.apply(
        lambda row: row[column] if row[column] > 0 else 
                    (repo_medians.get(row["repo"], overall_median) if pd.notna(row[column]) else overall_median),
        axis=1
    )

df_cleaned["interval_days"] = df_cleaned["interval_days"].astype(int)
df_cleaned["is_delayed"] = df_cleaned["is_delayed"].astype(int)
df_cleaned["open_issues"] = df_cleaned["open_issues"].astype(int)

df_cleaned.to_csv("final_dataset_cleaned.csv", index=False)
print("Cleaned dataset saved to final_dataset_cleaned.csv")

print("\nSummary of cleaned dataset:")
print(df_cleaned.describe())