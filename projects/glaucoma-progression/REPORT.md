# Methods and interpretation

## Question

How does GCC thickness change during follow-up, and which covariance structure describes repeated measurements?

## Data

107 subjects · 786 visits. The course-supplied retinal measurement file is not redistributed. Use an authorized local copy. Public artifacts contain model summaries and aggregate trajectories, not the source visit table.

## Analysis

I compared linear and quadratic time trends, then evaluated random effects and residual correlation structures for repeated GCC measurements with a common fixed-effects specification.

The entry point is `analysis.R`. Parameters, variables, assumptions, and analysis cohorts are recorded in the code and generated result files.

## Findings

A quadratic mean trajectory was preferred among the tested mean structures by BIC. With that fixed mean, random intercepts and slopes plus continuous-time AR(1) residuals had the lowest BIC (4078.6). The fitted time terms were −1.634 × time + 0.221 × time².

![Observed GCC measurements and the fitted quadratic mean trajectory.](results/gcc-trajectory.png)

_Observed GCC measurements and the fitted quadratic mean trajectory._

## Assumptions and interpretation

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
