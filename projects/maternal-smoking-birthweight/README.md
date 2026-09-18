# Maternal Smoking and Birth Weight

Compare unadjusted and adjusted birth weight differences, with explicit confounding limits and consistent analysis cohorts.

**Author:** Heyang Ma · Independent UCLA graduate course project, revised for this portfolio.
**Tools:** Python / statsmodels, Regression adjustment, Robust uncertainty. **Scope:** 4,642 observations.

## Question and result

How does the association between maternal smoking and birth weight change after measured covariate adjustment?

The unadjusted difference was −275 g (HC3 95% CI −317 to −234). Adjusting for maternal age, race, education, marital status, and alcohol use gave −233 g (−277 to −189). Both fits use the same 4,642 observations.

![Main result](results/birthweight-associations.png)

## What the analysis does

The executable analysis is [analysis.py](analysis.py). [Methods and interpretation](REPORT.md) explains the scope; [revision notes](REVISION_NOTES.md) distinguish the original analysis from the portfolio revision.

## Run locally

Install Python dependencies with `python -m pip install -r requirements.txt`.
Read [data access and input requirements](DATA_ACCESS.md), then run from this repository:

```sh
python analysis.py --data data/bweight.csv --output results
```

## Results and limits

This is observational evidence. Adjustment does not eliminate unmeasured confounding, exposure misclassification, or selection bias. Intensity categories are treated as categorical; the analysis does not claim a causal dose-response relationship. No formal sensitivity analysis was performed.

The committed `results/` files are generated summaries from the portfolio revision. Source records, credentials, fitted models, and original notebook outputs are excluded.

## Checks

Run `python -m unittest test_analysis.py`. These tests cover the corrected failure cases; they do not replace statistical validation.
