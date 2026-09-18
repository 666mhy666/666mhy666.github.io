# Methods and interpretation

## Question

How does GCC thickness change during follow-up, and which covariance structure describes repeated measurements?

## Data

107 subjects · 786 visits. The course-supplied retinal measurement file is not redistributed. Use an authorized local copy. Public artifacts contain model summaries and aggregate trajectories, not the source visit table.

## Analysis

Compared mean structures using ML and covariance structures using an identical fixed-effects formula. Used continuous-time correlation for irregular visits. Computed the baseline median once per subject rather than weighting subjects by visit count, and estimated the exploratory interaction from the fitted model.

The entry point is `analysis.R`. Parameters and analysis cohorts are recorded in the code and result files.

## Findings

A quadratic mean trajectory was preferred among the tested mean structures by BIC. With that fixed mean, random intercepts and slopes plus continuous-time AR(1) residuals had the lowest BIC (4078.6). The fitted time terms were −1.634 × time + 0.221 × time².

![Main result](results/gcc-trajectory.png)

## Limits

Model comparisons are exploratory; intervals omit model-selection uncertainty. Baseline severity groups can show regression to the mean even when the baseline visit is removed from follow-up modeling. The fitted curve should not be extrapolated beyond observed follow-up or interpreted as a treatment effect.

## Result files

- [age-models-ml.csv](results/age-models-ml.csv)
- [coefficients.csv](results/coefficients.csv)
- [covariance-models.csv](results/covariance-models.csv)
- [diagnostics.png](results/diagnostics.png)
- [exploratory-baseline-interaction.csv](results/exploratory-baseline-interaction.csv)
- [gcc-trajectory.png](results/gcc-trajectory.png)
- [mean-models-ml.csv](results/mean-models-ml.csv)
- [mean-trajectory.csv](results/mean-trajectory.csv)
- [run.txt](results/run.txt)
- [session-info.txt](results/session-info.txt)
