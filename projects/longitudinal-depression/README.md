# Depression Trajectories and Drug Concentration

Model changes in depression scores over four weeks and examine how trajectories vary with plasma desipramine concentration.

**Author:** Heyang Ma · Independent UCLA graduate course project, revised for this portfolio.
**Tools:** R / nlme, Mixed effects models, Repeated measurements. **Scope:** 66 subjects · 250 observations.

## Question and result

How are changes in depression scores associated with diagnosis and measured drug concentration after accounting for repeated observations?

For the selected random intercept and slope model, the week × desipramine coefficient was −0.887 (95% CI −1.551 to −0.224; p = 0.009). This coefficient is on the dataset’s recorded concentration scale; it is not a treatment effect or a dosing recommendation.

![Main result](results/depression-trajectories.png)

## What the analysis does

The executable analysis is [analysis.R](analysis.R). [Methods and interpretation](REPORT.md) explains the scope; [revision notes](REVISION_NOTES.md) distinguish the original analysis from the portfolio revision.

## Run locally

Use R 4.5.2; the recommended package `nlme` is required.
Read [data access and input requirements](DATA_ACCESS.md), then run from this repository:

```sh
Rscript analysis.R data/riesby.csv results
```

## Results and limits

Drug concentrations are observed, time-varying measurements. The model does not establish causation or separate within-person from between-person concentration effects. The sample is small, and reported intervals do not account for model selection.

The committed `results/` files are generated summaries from the portfolio revision. Source records, credentials, fitted models, and original notebook outputs are excluded.

