import pandas as pd
import numpy as np

# ==== Settings ====
PATH = "../data/score_emo.xlsx"

# Candidate column names for emotion and well-being
EMOTION_COL_CANDIDATES = ["emotion", "Emotion", "emo_label", "label"]
WB_COL_CANDIDATES = ["individual well-being", "well-being", "wellbeing", "WB", "wb", "score"]

# Desired output order of emotions (to match the example table)
EMOTION_ORDER = ["Joy", "Trust", "Anxiety", "Surprise", "Sadness", "Anger", "Disgust"]

# Decimal precision
DEC = 3

# ==== Load data ====
df = pd.read_excel(PATH)

# Function to pick the first matching column
def pick_col(cands, cols):
    for c in cands:
        if c in cols:
            return c
    raise ValueError(f"Required column not found. Tried: {cands}")

emo_col = pick_col(EMOTION_COL_CANDIDATES, df.columns)
wb_col  = pick_col(WB_COL_CANDIDATES, df.columns)

# Drop rows with missing values
df = df.dropna(subset=[emo_col, wb_col]).copy()

# Normalize emotion labels: strip whitespace, replace multiple spaces, capitalize
df[emo_col] = (
    df[emo_col].astype(str).str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.capitalize()
)

# Overall statistics
overall_N   = int(df.shape[0])
overall_mu  = float(df[wb_col].mean())
overall_sd  = float(df[wb_col].std(ddof=1))  # sample SD

# Per-emotion statistics
grp = df.groupby(emo_col)[wb_col].agg(N="count", Mean="mean", SD=lambda x: x.std(ddof=1)).reset_index()
grp.rename(columns={emo_col: "Emotion"}, inplace=True)
grp["Delta"] = grp["Mean"] - overall_mu

# Reorder emotions according to EMOTION_ORDER
order_map = {e: i for i, e in enumerate(EMOTION_ORDER)}
grp["__order__"] = grp["Emotion"].map(order_map)
grp = pd.concat([
    grp[grp["__order__"].notna()].sort_values("__order__"),
    grp[grp["__order__"].isna()].sort_values("N", ascending=False)  # unexpected labels: sorted by N
], ignore_index=True).drop(columns="__order__")

# Helper for formatting numbers
def f3(x): 
    return f"{x:.{DEC}f}"

# Build the result table
table_rows = []

# Add overall row
table_rows.append({
    "Emotion": "All data",
    "N": overall_N,
    "WB Mean": f3(overall_mu),
    "WB SD": f3(overall_sd),
    "Delta vs overall mean": "--"
})

# Add rows for each emotion
for _, r in grp.iterrows():
    table_rows.append({
        "Emotion": r["Emotion"],
        "N": int(r["N"]),
        "WB Mean": f3(r["Mean"]),
        "WB SD": f3(r["SD"]),
        "Delta vs overall mean": f3(r["Delta"])
    })

result_df = pd.DataFrame(table_rows, columns=["Emotion", "N", "WB Mean", "WB SD", "Delta vs overall mean"])

# ===== Print preview =====
print(result_df)
