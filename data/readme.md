# Data Directory

This directory contains the minimal anonymized datasets required to reproduce the results reported in the manuscript. All files are provided in `.xlsx` format.

## Files

### `score_indices.xlsx`
Contains the core dataset used to reproduce the main results.  
- Unit: team-by-week  
- Variables:  
  - Individual well-being scores  
  - Score-based sharedness index (SSI)  
  - Text-based sharedness index (TSI)  

### `score_ihs.xlsx`
Used to examine the correlation between the proposed sharedness indices and the Interdependent Happiness Scale (IHS).  
- Unit: team  
- Variables: team-level IHS scores  

### `score_emo.xlsx`
Dataset for reproducing the results in the **Emotion** section.  
- Unit: diary entry  
- Variables:  
  - Individual well-being scores  
  - Emotion labels predicted from diary texts by a BERT model  

### `token_counts_welbe.xlsx`
Dataset for reproducing the results of the **Word (odds ratio)** analysis with respect to individual well-being.  
- Groups:  
  - High well-being (≥ 3rd quartile)  
  - Low well-being (≤ 1st quartile)  
- Variables: frequency of each token in diary texts for each group  

### `token_counts_SSI.xlsx`
Dataset for reproducing the **Word (odds ratio)** analysis with respect to the score-based sharedness index (SSI).  
- Groups:  
  - High SSI (≥ 3rd quartile)  
  - Low SSI (≤ 1st quartile)  
- Variables: frequency of each token in diary texts for each group  

### `class_sizes.xlsx`
Provides the group sizes used in the odds ratio analysis.  
- Variables:  
  - Number of entries in the high/low groups for individual well-being  
  - Number of entries in the high/low groups for SSI  

