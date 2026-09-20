# Medicaid Lottery and Health Measures

Estimate differences in blood pressure and HbA1c by lottery assignment, with household clustering and a check of outcome definitions.

**Author:** Heyang Ma · Independent UCLA graduate course project, revised for this portfolio.
**Tools:** Python / statsmodels, Randomized assignment, Clustered inference. **Scope:** 12,134 individuals.

## Question

In the supplied Oregon Health Insurance Experiment teaching extract, how do measured health outcomes differ by lottery assignment?

## What I did

I estimated unadjusted and covariate-adjusted assignment differences with household-clustered uncertainty, checked baseline balance and missingness, and verified the definition of a composite variable before choosing the outcomes.

## Main finding

Adjusted assignment differences were 0.145 for systolic blood pressure (95% CI −0.373 to 0.663), 0.216 for diastolic pressure (−0.184 to 0.616), and −0.0027 for HbA1c (−0.0203 to 0.0149), on the supplied dataset scales. All intervals include zero; this is not evidence that insurance has no health effects.

![Lottery-assignment differences with 95% household-clustered confidence intervals.](results/assignment-effects.png)

_Lottery-assignment differences with 95% household-clustered confidence intervals._

## Important limitations

The estimand is lottery assignment, not insurance receipt. This unweighted teaching-data reanalysis is not a full replication of the original study’s sampling design, weights, missingness treatment, or estimand. The source extract’s transformation and sampling documentation are incomplete.

## Code and reproducibility

Install Python dependencies with `python -m pip install -r requirements.txt`.
Read [data access and input requirements](DATA_ACCESS.md), then run from this repository:

```sh
python analysis.py --data data/ohie.csv --output results
```


The executable analysis is [analysis.py](analysis.py). See [REPORT.md](REPORT.md) for model details and interpretation, [DATA_ACCESS.md](DATA_ACCESS.md) for inputs, and [REVISION_NOTES.md](REVISION_NOTES.md) for the distinction between the course project and portfolio revision. The committed `results/` files are generated summaries from the revision.

