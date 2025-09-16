import pandas as pd
from scipy.stats import pearsonr

# ===== Input files =====
IDX_PATH = "../data/score_indices.xlsx"   # team, week, individual well-being, SSI, TSI
IHS_PATH = "../data/score_ihs.xlsx"       # expected columns: team, ihs

# ===== Load data =====
df_idx = pd.read_excel(IDX_PATH)
df_ihs = pd.read_excel(IHS_PATH)

# If column names are different, adjust them here (uncomment and edit if necessary)
# df_ihs = df_ihs.rename(columns={"IHS_score": "ihs"})

# ===== Utility function =====
def corr_with_ihs(df_idx, df_ihs, metric_col, min_points=4):
    """
    For the given metric_col, this function performs:
      1) Remove missing values
      2) Keep only teams with at least min_points of non-missing values
      3) Calculate the team mean for the metric
      4) Merge with IHS scores
      5) Compute Pearson correlation coefficient and p-value
    Returns correlation results and intermediate tables
    """
    # 1) Remove missing values
    df_metric = df_idx.dropna(subset=[metric_col, "team"]).copy()

    # 2) Filter teams with enough data points (independently for each metric)
    df_metric = df_metric.groupby("team").filter(lambda g: g[metric_col].notna().sum() >= min_points)

    # 3) Compute team mean
    team_mean = (
        df_metric.groupby("team", as_index=False)[metric_col]
        .mean()
        .rename(columns={metric_col: f"mean_{metric_col}"})
    )

    # 4) Merge with IHS
    merged = pd.merge(team_mean, df_ihs, on="team", how="inner")

    # 5) Correlation
    n = merged.shape[0]
    if n >= 2:
        r, p = pearsonr(merged[f"mean_{metric_col}"], merged["ihs"])
    else:
        r, p = float("nan"), float("nan")

    return {
        "metric": metric_col,
        "n_used": n,
        "r": r,
        "p": p,
        "table": merged,           # table used for correlation
        "team_mean_table": team_mean,  # team mean table after filtering
    }

# ===== Run =====
res_ssi = corr_with_ihs(df_idx, df_ihs, metric_col="SSI", min_points=4)
res_tsi = corr_with_ihs(df_idx, df_ihs, metric_col="TSI", min_points=4)

# ===== Output =====
print("=== Correlation: team mean SSI vs IHS ===")
print(f"n = {res_ssi['n_used']}")
print(f"r = {res_ssi['r']:.3f}" if pd.notna(res_ssi['r']) else "r = NaN")
print(f"p = {res_ssi['p']:.3g}\n" if pd.notna(res_ssi['p']) else "p = NaN\n")

print("=== Correlation: team mean TSI vs IHS ===")
print(f"n = {res_tsi['n_used']}")
print(f"r = {res_tsi['r']:.3f}" if pd.notna(res_tsi['r']) else "r = NaN")
print(f"p = {res_tsi['p']:.3g}\n" if pd.notna(res_tsi['p']) else "p = NaN\n")
