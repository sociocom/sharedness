import pandas as pd
import numpy as np

# ===============================
# Paths (adjust if needed)
# ===============================
TOKEN_WELBE_PATH = "../data/token_counts_welbe.csv"  # columns: token, class, count
CLASS_SIZES_PATH = "../data/class_sizes.xlsx"        # columns: class, n_docs

# ===============================
# Config
# ===============================
SMOOTH = 0.5   # Haldane–Anscombe correction
TOKEN_COL = "token"
CLASS_COL = "class"
COUNT_COL = "count"

# Expected class labels
HIGH_LABEL = "well-being_high"
LOW_LABEL  = "well-being_low"

# Alias mapping for flexibility
CLASS_ALIAS = {
    "WB_high": HIGH_LABEL,
    "WB_low": LOW_LABEL,
    "welbe_high": HIGH_LABEL,
    "welbe_low": LOW_LABEL,
    "wellbeing_high": HIGH_LABEL,
    "wellbeing_low": LOW_LABEL,
    HIGH_LABEL: HIGH_LABEL,
    LOW_LABEL: LOW_LABEL,
}

# ===============================
# Helpers
# ===============================
def normalize_class_labels(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Map class labels to canonical names if aliases are present."""
    df = df.copy()
    df[col] = df[col].map(lambda x: CLASS_ALIAS.get(str(x), str(x)))
    return df

def load_class_sizes(path: str) -> tuple[int, int]:
    """Read class_sizes.xlsx and return (N_high, N_low)."""
    sizes = pd.read_excel(path)
    if "class" not in sizes.columns or "n_docs" not in sizes.columns:
        raise ValueError("class_sizes.xlsx must contain columns: 'class', 'n_docs'.")
    N_high = int(sizes.loc[sizes["class"] == HIGH_LABEL, "n_docs"].iloc[0])
    N_low  = int(sizes.loc[sizes["class"] == LOW_LABEL,  "n_docs"].iloc[0])
    return N_high, N_low

def ci_flag(lo, hi):
    """Return significance flag based on 95% CI."""
    if lo > 1.0:
        return "upper"
    elif hi < 1.0:
        return "lower"
    else:
        return "n.s."

# ===============================
# Main
# ===============================
# Load token counts
tok = pd.read_csv(TOKEN_WELBE_PATH)
tok = normalize_class_labels(tok, CLASS_COL)

# Remove tokens of length 1
tok = tok[tok[TOKEN_COL].astype(str).str.len() > 1]

# Load class sizes
N_high, N_low = load_class_sizes(CLASS_SIZES_PATH)

# Pivot to get counts per token
piv = tok.pivot_table(
    index=TOKEN_COL, columns=CLASS_COL, values=COUNT_COL, aggfunc="sum"
).fillna(0)

if HIGH_LABEL not in piv.columns:
    piv[HIGH_LABEL] = 0
if LOW_LABEL not in piv.columns:
    piv[LOW_LABEL] = 0

a = piv[HIGH_LABEL].astype(float)
c = piv[LOW_LABEL].astype(float)
b = (N_high - a).astype(float)
d = (N_low  - c).astype(float)

# Odds ratio with smoothing
a_s, b_s, c_s, d_s = a + SMOOTH, b + SMOOTH, c + SMOOTH, d + SMOOTH
OR = (a_s * d_s) / (b_s * c_s)

logOR = np.log(OR)
se = np.sqrt(1.0/a_s + 1.0/b_s + 1.0/c_s + 1.0/d_s)
z = 1.96
ci_low = np.exp(logOR - z * se)
ci_high = np.exp(logOR + z * se)

flags = [ci_flag(lo, hi) for lo, hi in zip(ci_low, ci_high)]

# Build DataFrame
out = pd.DataFrame({
    "Word": piv.index,
    "OR": OR.values,
    "CI95_low": ci_low.values,
    "CI95_high": ci_high.values,
    "CI95_flag": flags
})

# Filter significant only
sig = out[out["CI95_flag"].isin(["upper", "lower"])]

# Print results
print("=== Significant tokens (95% CI does not cross 1, tokens longer than 1 character) ===")
print(sig.sort_values("OR", ascending=False).to_string(
    index=False,
    formatters={"OR": lambda x: f"{x:.3f}",
                "CI95_low": lambda x: f"{x:.3f}",
                "CI95_high": lambda x: f"{x:.3f}"}
))
