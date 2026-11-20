# Methods and interpretation

## Exposure, outcome and cohort

The coursework asked how birth weight in grams differs with reported smoking during pregnancy. In the extract, `msmoke` stores ordered daily cigarette-use categories. Code 0 indicates no reported smoking and codes 1–3 indicate increasing levels. The original cross-tabulation against `mbsmoke` showed exact agreement with the binary exposure, as well as 200, 337 and 327 records in categories 1, 2 and 3. The available documentation gives codes but does not specify their cutoffs. Timing and duration are unavailable.

The coursework plotted the birth weight distributions by smoking status. They overlapped, with a shift toward lower birth weight among smokers. Group means were 3,137.66 g for records with reported smoking and 3,412.91 g for the others. All three revised models use the same 4,642 complete records. The revised encoder retains missing smoking codes as missing.

## DAG and adjustment

The [redrawn DAG](results/coursework-dag.svg) follows the [written arrow list](results/coursework-dag.dot) in the original coursework. It includes maternal age, race, education, marital status and alcohol use as possible common causes of smoking and birth weight. Race in this graph can reflect social and structural conditions. The diagram is a set of assumptions about the data, including relationships among background variables. The original discussion separately considered alternative assumptions about when prenatal care occurs.

I adjusted for the five measured background variables. Prenatal care was left out because the graph places it downstream of smoking and upstream of birth weight. Conditioning on it could block a pathway of interest. The coursework distinguished an overall causal contrast from a contrast among mothers who smoked. In the revised analysis I report regression associations, with no identification claim for either causal contrast.

## Baseline comparison and overlap

The [balance output](results/balance.csv) shows group means and standardized differences. On average, mothers who reported smoking were younger, had fewer years of education, were less often married, and reported alcohol use more often.

The [overlap table](results/overlap-counts.csv) crosses education (≤11, 12, 13–15 and ≥16 years) with the two race categories as coded in the extract. Both smoking groups were present in each of those strata. In the ≥16-years strata, the counts were 3 smokers out of 77 and 39 out of 819. The check covers education and race, and does not establish positivity over the full adjustment set.

## Regression estimates

[analysis.py](analysis.py) fits an unadjusted binary regression, a binary regression with the five covariates, and a regression with categorical smoking intensity and those same covariates. Estimates are in grams and all intervals use HC3 heteroskedasticity-robust standard errors.

| Comparison | Estimate (g) | 95% CI (g) |
| --- | ---: | ---: |
| Any smoking, unadjusted | −275.25 | −316.86 to −233.64 |
| Any smoking, adjusted | −233.03 | −277.14 to −188.92 |
| Level 1 vs. level 0, adjusted | −157.98 | −230.83 to −85.13 |
| Level 2 vs. level 0, adjusted | −224.96 | −290.54 to −159.37 |
| Level 3 vs. level 0, adjusted | −288.67 | −355.70 to −221.63 |

The estimates were more negative at higher recorded levels. A causal interpretation would require conditional exchangeability, positivity, and a well-defined exposure. The original coursework also considered no interference, which assumes that one mother’s smoking status does not change another infant’s birth weight. Unmeasured factors such as stress and nutrition, coarse exposure categories, possible misclassification, and selection can affect interpretation. A formal sensitivity analysis was not performed.

## Supporting files

- [Estimates](results/estimates.csv) and [confidence interval figure](results/birthweight-associations.png)
- [Balance](results/balance.csv), [overlap](results/overlap-counts.csv) and [run metadata](results/run.json)
- [DAG](results/coursework-dag.svg) and [Graphviz source](results/coursework-dag.dot)
- [Data access](DATA_ACCESS.md) and [revision history](REVISION_NOTES.md)
