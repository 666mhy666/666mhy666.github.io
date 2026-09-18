# Methods and interpretation

## Question

How does the association between maternal smoking and birth weight change after measured covariate adjustment?

## Data

4,642 observations. The course-supplied bweight.csv is not redistributed because its redistribution terms were not supplied. Reproduction requires an authorized copy of the same extract. Do not substitute a similarly named dataset and expect identical results.

## Analysis

Preserved missing smoking status rather than coding it as nonsmoking. Used a common complete-case cohort for model comparison and HC3 uncertainty. Removed unsupported claims that the association is robust to unmeasured confounding.

The entry point is `analysis.py`. Parameters and analysis cohorts are recorded in the code and result files.

## Findings

The unadjusted difference was −275 g (HC3 95% CI −317 to −234). Adjusting for maternal age, race, education, marital status, and alcohol use gave −233 g (−277 to −189). Both fits use the same 4,642 observations.

![Main result](results/birthweight-associations.png)

## Limits

This is observational evidence. Adjustment does not eliminate unmeasured confounding, exposure misclassification, or selection bias. Intensity categories are treated as categorical; the analysis does not claim a causal dose-response relationship. No formal sensitivity analysis was performed.

## Result files

- [balance.csv](results/balance.csv)
- [birthweight-associations.png](results/birthweight-associations.png)
- [estimates.csv](results/estimates.csv)
- [overlap-counts.csv](results/overlap-counts.csv)
- [run.json](results/run.json)
