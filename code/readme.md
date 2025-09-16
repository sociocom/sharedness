# Code Directory

This folder contains analysis scripts used to reproduce the results reported in the manuscript.  
Unless otherwise noted, scripts read input files from `../data/` and (optionally) write outputs to `../results/`.

> **Note:** If your environment does not use command-line arguments, edit the file paths at the top of each script to point to the files under `../data/`.

## Environment

- Python 3.9+  
- Recommended packages: `pandas`, `numpy`, `scipy` (for correlations and basic stats), `openpyxl` (Excel I/O), `matplotlib` (if plots are produced)

---

## Files

### `index_score.py`
Computes correlation coefficients between **individual well-being** and the **score-based sharedness index (SSI)**.  
- **Input:** `../data/score_indices.xlsx` (team-by-week records with well-being and SSI)  
- **Output:** Table of correlation coefficients (e.g., team-by-week and team-level aggregates), typically saved to `../results/` and/or printed to stdout.  
- **Purpose:** Reproduce the main association between well-being and SSI.

### `index_text.py`
Computes correlation coefficients between **individual well-being** and the **text-based sharedness index (TSI)**.  
- **Input:** `../data/score_indices.xlsx` (team-by-week records with well-being and TSI)  
- **Output:** Table of correlation coefficients (team-by-week and team-level), saved to `../results/` and/or printed to stdout.  
- **Purpose:** Reproduce the association between well-being and TSI.

### `ihs.py`
Computes correlation coefficients between **individual well-being** and the **Interdependent Happiness Scale (IHS)**.  
- **Input:** `../data/score_ihs.xlsx` (team-level IHS) and, if needed, `../data/score_indices.xlsx` (well-being)  
- **Output:** Team-level correlation summary saved to `../results/` and/or printed to stdout.  
- **Purpose:** Validate convergent validity of the sharedness indices against IHS.

### `odds_wellbeing.py`
Computes **token-level odds ratios** comparing **high** vs **low** individual well-being groups.  
- **Input:**  
  - `../data/token_counts_welbe.xlsx` (token frequencies per group)  
  - `../data/class_sizes.xlsx` (group sizes for high/low well-being)  
- **Output:** Odds-ratio table (e.g., `token_odds_welbe.xlsx`) saved to `../results/`.  
- **Purpose:** Reproduce the word-level (odds-ratio) analysis for well-being.

### `odds_sharedness.py`
Computes **token-level odds ratios** comparing **high** vs **low** score-based sharedness index (SSI) groups.  
- **Input:**  
  - `../data/token_counts_SSI.xlsx` (token frequencies per group)  
  - `../data/class_sizes.xlsx` (group sizes for high/low SSI)  
- **Output:** Odds-ratio table (e.g., `token_odds_SSI.xlsx`) saved to `../results/`.  
- **Purpose:** Reproduce the word-level (odds-ratio) analysis for SSI.

### `emotion.py`
Summarizes the distribution of **emotion labels** predicted from diary entries and links them to **individual well-being**.  
- **Input:** `../data/score_emo.xlsx` (entry-level well-being and BERT-predicted emotion labels)  
- **Output:** Distribution tables and/or figures saved to `../results/`.  
- **Purpose:** Reproduce the analyses reported in the *Emotion* section.

---

## Typical Usage

From the repository root (or `code/`), run:

```bash
# Correlations (SSI / TSI / IHS)
python code/index_score.py
python code/index_text.py
python code/ihs.py

# Odds-ratio analyses
python code/odds_wellbeing.py
python code/odds_sharedness.py

# Emotion distributions
python code/emotion.py

