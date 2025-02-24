import pandas as pd

# Load the final dataset
df_final = pd.read_csv("final_dataset.csv")

# Convert release_date to datetime
df_final["release_date"] = pd.to_datetime(df_final["release_date"])

# Step 1: Manual Checks (Simplified Validation)
print("Validating delays...")
# Check if delayed releases have unusually high intervals
delayed_summary = df_final[df_final["is_delayed"] == 1].groupby("repo").agg({
    "interval_days": "mean",
    "open_issues": "mean",
    "avg_pr_comments": "mean"
}).reset_index()
print("Average stats for delayed releases by repo:")
print(delayed_summary)

# Step 2: Outlier Removal
# Remove releases with intervals > 365 days (1 year) as irregular
print("\nRemoving outliers (interval_days > 365)...")
outliers = df_final["interval_days"] > 365
print(f"Found {outliers.sum()} outliers")
df_cleaned = df_final[~outliers].copy()

# Step 3: Imputation
# For remaining NaN or zero values in open_issues/avg_pr_comments, use repo-specific medians
print("\nImputing missing data...")
for column in ["open_issues", "avg_pr_comments"]:
    # Calculate median per repo, excluding zeros
    repo_medians = df_cleaned[df_cleaned[column] > 0].groupby("repo")[column].median()
    # Fill zeros/NaN with repo median, or overall median if repo has no non-zero values
    overall_median = df_cleaned[column].median()
    df_cleaned[column] = df_cleaned.apply(
        lambda row: row[column] if row[column] > 0 else 
                    (repo_medians.get(row["repo"], overall_median) if pd.notna(row[column]) else overall_median),
        axis=1
    )

# Ensure data types
df_cleaned["interval_days"] = df_cleaned["interval_days"].astype(int)
df_cleaned["is_delayed"] = df_cleaned["is_delayed"].astype(int)
df_cleaned["open_issues"] = df_cleaned["open_issues"].astype(int)

# Save cleaned dataset
df_cleaned.to_csv("final_dataset_cleaned.csv", index=False)
print("Cleaned dataset saved to final_dataset_cleaned.csv")

# Summary stats
print("\nSummary of cleaned dataset:")
print(df_cleaned.describe())