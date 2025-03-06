import pandas as pd

# Load PR dataset
df_prs = pd.read_csv("pr_data.csv")

# Ensure datetime formats are consistent
df_prs["created_at"] = pd.to_datetime(df_prs["created_at"]).dt.tz_localize(None)
df_prs["merged_at"] = pd.to_datetime(df_prs["merged_at"]).dt.tz_localize(None)

# Check if the dataset contains lines changed per PR
if "additions" in df_prs.columns and "deletions" in df_prs.columns:
    # Compute total lines changed (additions + deletions)
    df_prs["lines_changed"] = df_prs["additions"] + df_prs["deletions"]
    
    # Compute the average lines changed per PR for each repository
    pr_lines_stats = df_prs.groupby("repo").agg(
        avg_lines_changed=("lines_changed", "mean")  # Mean lines changed per PR
    ).reset_index()
    
    # Load the final dataset
    df_final = pd.read_csv("final_dataset_enhanced.csv")
    
    # Merge new PR complexity metric into the dataset
    df_final = df_final.merge(pr_lines_stats, on="repo", how="left")
    
    # Fill missing values (if any repository has no recorded changes)
    df_final["avg_lines_changed"] = df_final["avg_lines_changed"].fillna(0)
    
    # Save updated dataset
    df_final.to_csv("final_dataset_enhanced.csv", index=False)
    
    print("Updated dataset saved with avg_lines_changed per PR.")
else:
    print("PR dataset does not contain 'additions' and 'deletions' columns.")
