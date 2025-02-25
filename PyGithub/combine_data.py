import pandas as pd

df_issues = pd.read_csv("issue_data.csv")
df_prs = pd.read_csv("pr_data.csv")
df_releases = pd.read_csv("release_data_with_delays.csv")

df_issues["release_id"] = df_issues.groupby("repo").cumcount() + 1
df_prs["release_id"] = df_prs.groupby("repo").cumcount() + 1

issues_agg = df_issues.groupby(["repo", "release_id"]).size().reset_index(name="open_issues")

prs_agg = df_prs.groupby(["repo", "release_id"]).agg({"comments": "mean"}).reset_index()
prs_agg.rename(columns={"comments": "avg_pr_comments"}, inplace=True)

df_final = df_releases.merge(
    issues_agg,
    on=["repo", "release_id"],
    how="left"
).merge(
    prs_agg,
    on=["repo", "release_id"],
    how="left"
)

df_final["open_issues"] = df_final["open_issues"].fillna(0).astype(int)
df_final["avg_pr_comments"] = df_final["avg_pr_comments"].fillna(0)

df_final["release_date"] = pd.to_datetime(df_final["release_date"])
df_final["interval_days"] = df_final["interval_days"].astype(int)
df_final["is_delayed"] = df_final["is_delayed"].astype(int)

df_final.to_csv("final_dataset.csv", index=False)
print("Final dataset saved to final_dataset.csv")

print("\nPreview of final dataset:")
print(df_final.head())