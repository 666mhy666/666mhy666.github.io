# Data access

The historical depression trial dataset is distributed as `riesby` in the R package `multilevelmod`. The recorded outcome, `depr_score`, is change in depression score. [Dataset documentation](https://multilevelmod.tidymodels.org/reference/riesby.html)

Run from the repository root in R:

```r
install.packages("multilevelmod")
data("riesby", package = "multilevelmod")
dir.create("data", showWarnings = FALSE)
write.csv(riesby, "data/riesby.csv", row.names = FALSE)
```

The analysis script uses `nlme`. The saved [session information](results/session-info.txt) has the original R and package versions.

## Input contract

subject, week, depr_score, endogenous, imipramine, desipramine

Keep inputs in a local `data/` directory. Input data and model files are excluded from the public release. Course access is not assumed to confer redistribution permission.
