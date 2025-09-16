import pandas as pd
import numpy as np

# ===============================
# Paths (adjust if needed)
# ===============================
TOKEN_SSI_PATH   = "../data/token_counts_ssi.csv"  # columns: token, class, count
CLASS_SIZES_PATH = "class_sizes.xlsx"      # columns: class, n_docs

# ===============================
# Config
# ===============================
SMOOTH = 0.5   # Haldane–Anscombe correction (+0.5)
ZVAL   = 1.96  # for 95% CI
TOKEN_COL = "token"
CLASS_COL = "class"
COUNT_COL = "count"

# Canonical class labels (must match class_sizes.xlsx)
HIGH_LABEL = "SSI_high"
LOW_LABEL  = "SSI_low"

# Optional alias mapping for robustness
CLASS_ALIAS = {
    "ssi_high": HIGH_LABEL, "SSI_High": HIGH_LABEL,
    "ssi_low":  LOW_LABEL,  "SSI_Low":  LOW_LABEL,
    HIGH_LABEL: HIGH_LABEL, LOW_LABEL:  LOW_LABEL,
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
    """
    Read class_sizes.xlsx and return (N_high, N_low) for SSI classes.
    Requires columns: 'class', 'n_docs'.
    """
    sizes = pd.read_excel(path)
    if "class" not in sizes.columns or "n_docs" not in sizes.columns:
        raise ValueError("class_sizes.xlsx must contain columns: 'class', 'n_docs'.")
    try:
        N_high = int(sizes.loc[sizes["class"] == HIGH_LABEL, "n_docs"].iloc[0])
        N_low  = int(sizes.loc[sizes["class"] == LOW_LABEL,  "n_docs"].iloc[0])
    except IndexError:
        raise ValueError(f"Could not find both '{HIGH_LABEL}' and '{LOW_LABEL}' in class_sizes.xlsx.")
    return N_high, N_low

def ci_flag(lo: float, hi: float) -> str:
    """Return significance flag based on 95% CI relative to 1."""
    if lo > 1.0:
        return "upper"   # enriched in HIGH
    elif hi < 1.0:
        return "lower"   # enriched in LOW
    else:
        return "n.s."

# ===============================
# Main
# ===============================
# 1) Load minimal public token counts and normalize class labels
tok = pd.read_csv(TOKEN_SSI_PATH)
tok = normalize_class_labels(tok, CLASS_COL)

# 2) Remove 1-character tokens (per your requirement)
tok = tok[tok[TOKEN_COL].astype(str).str.len() > 1]

# 3) Load class sizes (N_high, N_low)
N_high, N_low = load_class_sizes(CLASS_SIZES_PATH)

# 4) Build a token x class matrix of document counts
piv = tok.pivot_table(index=TOKEN_COL, columns=CLASS_COL, values=COUNT_COL, aggfunc="sum").fillna(0)

# Ensure both class columns exist
if HIGH_LABEL not in piv.columns:
    piv[HIGH_LABEL] = 0
if LOW_LABEL not in piv.columns:
    piv[LOW_LABEL] = 0

# 5) 2x2 counts per token (document-unique presence):
#    a = present in HIGH,  b = absent in HIGH
#    c = present in LOW,   d = absent in LOW
a = piv[HIGH_LABEL].astype(float)
c = piv[LOW_LABEL].astype(float)
b = (N_high - a).astype(float)
d = (N_low  - c).astype(float)

# Sanity check: per-token present counts cannot exceed class sizes
if (a > N_high).any() or (c > N_low).any():
    raise ValueError("Some token counts exceed the number of documents in a class.")

# 6) Odds ratio and 95% CI (aligned with your method)
# OR = (a+0.5)*(d+0.5) / ((b+0.5)*(c+0.5))
# SE = sqrt(1/(a+0.5) + 1/(b+0.5) + 1/(c+0.5) + 1/(d+0.5))
# CI95 = exp( log(OR) ± 1.96 * SE )
a_s, b_s, c_s, d_s = a + SMOOTH, b + SMOOTH, c + SMOOTH, d + SMOOTH
OR = (a_s * d_s) / (b_s * c_s)
logOR = np.log(OR)
SE = np.sqrt(1.0/a_s + 1.0/b_s + 1.0/c_s + 1.0/d_s)
ci_low  = np.exp(logOR - ZVAL * SE)
ci_high = np.exp(logOR + ZVAL * SE)

# 7) Flag significance (CI not crossing 1) and direction
flags = [ci_flag(lo, hi) for lo, hi in zip(ci_low, ci_high)]

out = pd.DataFrame({
    "Word": piv.index,
    "OR": OR.values,
    "CI95_low": ci_low.values,
    "CI95_high": ci_high.values,
    "CI95_flag": flags
})

# 8) Keep significant tokens only and print,
#    showing HIGH-enriched first (descending OR), then LOW-enriched (ascending OR)
sig = out[out["CI95_flag"].isin(["upper", "lower"])]

high_side = sig[sig["CI95_flag"] == "upper"].sort_values("OR", ascending=False)
low_side  = sig[sig["CI95_flag"] == "lower"].sort_values("OR", ascending=True)

print("=== Significant tokens for SSI (95% CI does not cross 1; tokens longer than 1 character) ===\n")

print("[Enriched in HIGH (upper): sorted by descending OR]")
if not high_side.empty:
    print(high_side.to_string(
        index=False,
        formatters={
            "OR": lambda x: f"{x:.3f}",
            "CI95_low": lambda x: f"{x:.3f}",
            "CI95_high": lambda x: f"{x:.3f}"
        }
    ))
else:
    print("(none)")

print("\n[Enriched in LOW (lower): sorted by ascending OR]")
if not low_side.empty:
    print(low_side.to_string(
        index=False,
        formatters={
            "OR": lambda x: f"{x:.3f}",
            "CI95_low": lambda x: f"{x:.3f}",
            "CI95_high": lambda x: f"{x:.3f}"
        }
    ))
else:
    print("(none)")
