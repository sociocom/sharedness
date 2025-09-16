# Sharedness Index Project

Repository for the paper _“Social harmony at work: A sharedness index linking team atmosphere to individual well-being in a Japanese company”

---

## Directory Structure

### `/data`
Contains the minimal anonymized datasets required for reproducibility.  
- See [`data/README.md`](data/README.md) for detailed descriptions of each file.  
- Includes team-by-week indices, Interdependent Happiness Scale scores, emotion-labeled entries, and token frequency tables for odds ratio analyses.  
- All files are anonymized and provided in `.xlsx` format. No raw text data is included, in accordance with ethics approval.

### `/code`
Contains the analysis scripts used to generate the reported results.  
- See [`code/README.md`](code/README.md) for detailed descriptions of each script.  
- Includes correlation analyses (SSI, TSI, IHS), odds ratio calculations, and emotion distribution analyses.  
- Scripts are written in Python and assume input from `/data` and outputs to `/results` (if applicable).

---

## Reproducibility Notes
- All analyses can be reproduced using the datasets provided in `/data` and the scripts in `/code`.  
- No raw diary texts are distributed due to privacy restrictions; all datasets are statistically processed and anonymized.  
- For environment details and usage examples, refer to the instructions in `code/README.md`.

---

## Citation
If you use this repository, please cite the manuscript once published.
