# Data access

Use the riesby dataset distributed with multilevelmod. In R: install.packages("multilevelmod"); data("riesby", package="multilevelmod"); dir.create("data", showWarnings=FALSE); write.csv(riesby, "data/riesby.csv", row.names=FALSE). The analysis itself uses nlme. The package describes depr_score as change in depression scores, not a raw symptom score. It is a historical teaching dataset, not data collected by the author.

## Input contract

subject, week, depr_score, endogenous, imipramine, desipramine

Source context: [https://multilevelmod.tidymodels.org/reference/riesby.html](https://multilevelmod.tidymodels.org/reference/riesby.html)

Keep inputs in a local `data/` directory. Input data and model files are excluded from the public release. Course access is not assumed to confer redistribution permission.
