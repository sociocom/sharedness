import pandas as pd
from scipy.stats import pearsonr

# Load the dataset
df = pd.read_excel("../data/score_indices.xlsx")

# Drop rows with missing values in the required columns
df = df.dropna(subset=["individual well-being", "SSI"])

# === Overall correlation ===
r_all, p_all = pearsonr(df["individual well-being"], df["SSI"])
print("Overall correlation:")
print(f"r = {r_all:.3f}, p = {p_all:.3g}\n")

# === Correlation by team ===
print("Correlation by team:")
for team, group in df.groupby("team"):
    if group.shape[0] > 1:  # Need at least 2 data points to compute correlation
        r, p = pearsonr(group["individual well-being"], group["SSI"])
        print(f"Team {team}: r = {r:.3f}, p = {p:.3g}")

# === Correlation by week ===
print("\nCorrelation by week:")
for week, group in df.groupby("week"):
    if group.shape[0] > 1:  # Need at least 2 data points to compute correlation
        r, p = pearsonr(group["individual well-being"], group["SSI"])
        print(f"Week {week}: r = {r:.3f}, p = {p:.3g}")
