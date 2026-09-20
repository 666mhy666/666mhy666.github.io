# Longitudinal Retinal Thickness in Glaucoma

Compare time trends and within-person correlation structures for retinal ganglion cell complex thickness.

**Author:** Heyang Ma · Independent UCLA graduate course project, revised for this portfolio.
**Tools:** R / nlme, Nonlinear trajectories, Residual correlation. **Scope:** 107 subjects · 786 visits.

## Question

How does GCC thickness change during follow-up, and which covariance structure describes repeated measurements?

## What I did

I compared linear and quadratic time trends, then evaluated random effects and residual correlation structures for repeated GCC measurements with a common fixed-effects specification.

## Main finding

A quadratic mean trajectory was preferred among the tested mean structures by BIC. With that fixed mean, random intercepts and slopes plus continuous-time AR(1) residuals had the lowest BIC (4078.6). The fitted time terms were −1.634 × time + 0.221 × time².

![Observed GCC measurements and the fitted quadratic mean trajectory.](results/gcc-trajectory.png)

_Observed GCC measurements and the fitted quadratic mean trajectory._

## Important limitations

Model comparisons are exploratory; intervals omit model-selection uncertainty. Baseline severity groups can show regression to the mean even when the baseline visit is removed from follow-up modeling. The fitted curve should not be extrapolated beyond observed follow-up or interpreted as a treatment effect.

## Code and reproducibility

Use R 4.5.2; the recommended package `nlme` is required.
Read [data access and input requirements](DATA_ACCESS.md), then run from this repository:

```sh
Rscript analysis.R data/ADAP_Macula_GCC_dataset.csv results
```


The executable analysis is [analysis.R](analysis.R). See [REPORT.md](REPORT.md) for model details and interpretation, [DATA_ACCESS.md](DATA_ACCESS.md) for inputs, and [REVISION_NOTES.md](REVISION_NOTES.md) for the distinction between the course project and portfolio revision. The committed `results/` files are generated summaries from the revision.

