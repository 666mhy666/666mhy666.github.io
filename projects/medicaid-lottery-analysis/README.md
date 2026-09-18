# Medicaid Lottery and Health Measures

Estimate differences in blood pressure and HbA1c by lottery assignment, with household clustering and a check of outcome definitions.

**Author:** Heyang Ma · Independent UCLA graduate course project, revised for this portfolio.
**Tools:** Python / statsmodels, Randomized assignment, Clustered inference. **Scope:** 12,134 individuals.

## Question and result

In the supplied Oregon Health Insurance Experiment teaching extract, how do measured health outcomes differ by lottery assignment?

Adjusted assignment differences were 0.145 for systolic blood pressure (95% CI −0.373 to 0.663), 0.216 for diastolic pressure (−0.184 to 0.616), and −0.0027 for HbA1c (−0.0203 to 0.0149), on the supplied dataset scales. All intervals include zero; this is not evidence that insurance has no health effects.

![Main result](results/assignment-effects.png)

## What the analysis does

The executable analysis is [analysis.py](analysis.py). [Methods and interpretation](REPORT.md) explains the scope; [revision notes](REVISION_NOTES.md) distinguish the original analysis from the portfolio revision.

## Run locally

Install Python dependencies with `python -m pip install -r requirements.txt`.
Read [data access and input requirements](DATA_ACCESS.md), then run from this repository:

```sh
python analysis.py --data data/ohie.csv --output results
```

## Results and limits

The estimand is lottery assignment, not insurance receipt. This unweighted teaching-data reanalysis is not a full replication of the original study’s sampling design, weights, missingness treatment, or estimand. The source extract’s transformation and sampling documentation are incomplete.

The committed `results/` files are generated summaries from the portfolio revision. Source records, credentials, fitted models, and original notebook outputs are excluded.

