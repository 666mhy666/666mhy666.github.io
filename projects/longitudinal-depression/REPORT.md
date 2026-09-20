# Methods and interpretation

## Question

How are changes in depression scores associated with diagnosis and measured drug concentration after accounting for repeated observations?

## Data

66 subjects · 250 observations. Use the riesby dataset distributed with multilevelmod. In R: install.packages("multilevelmod"); data("riesby", package="multilevelmod"); dir.create("data", showWarnings=FALSE); write.csv(riesby, "data/riesby.csv", row.names=FALSE). The analysis itself uses nlme. The package describes depr_score as change in depression scores, not a raw symptom score. It is a historical teaching dataset, not data collected by the author.

## Analysis

I compared longitudinal mean and covariance structures with mixed effects models, then estimated the association between week, diagnosis, and observed plasma desipramine concentration while accounting for repeated measurements.

The entry point is `analysis.R`. Parameters, variables, assumptions, and analysis cohorts are recorded in the code and generated result files.

## Findings

For the selected random intercept and slope model, the week × desipramine coefficient was −0.887 (95% CI −1.551 to −0.224; p = 0.009). This coefficient is on the dataset’s recorded concentration scale; it is not a treatment effect or a dosing recommendation.

![Descriptive weekly means by diagnosis group; the reported week × desipramine coefficient comes from the mixed effects model.](results/depression-trajectories.png)

_Descriptive weekly means by diagnosis group; the reported week × desipramine coefficient comes from the mixed effects model._

## Assumptions and interpretation

Drug concentrations are observed, time-varying measurements. The model does not establish causation or separate within-person from between-person concentration effects. The sample is small, and reported intervals do not account for model selection.

## Result files

- [coefficients.csv](results/coefficients.csv)
- [covariance-models.csv](results/covariance-models.csv)
- [depression-trajectories.png](results/depression-trajectories.png)
- [diagnostics.png](results/diagnostics.png)
- [mean-models-ml.csv](results/mean-models-ml.csv)
- [run.txt](results/run.txt)
- [session-info.txt](results/session-info.txt)
- [weekly-means.csv](results/weekly-means.csv)
Source context: [https://multilevelmod.tidymodels.org/reference/riesby.html](https://multilevelmod.tidymodels.org/reference/riesby.html)

