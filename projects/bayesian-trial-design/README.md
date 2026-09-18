# Bayesian Planning for a Hypothetical LDL Trial

Compare Bayesian decision rules and frequentist power under matched thresholds, with exact calculations checked by simulation.

**Author:** Heyang Ma · Independent UCLA graduate course project, revised for this portfolio.
**Tools:** R, Normal conjugate model, Monte Carlo validation. **Scope:** Analytical calculations + simulation.

## Question and result

How do effect size and the posterior decision threshold change the required sample size in a hypothetical two-arm LDL trial?

With known SD 4.5, a diffuse N(0, 100²) effect prior, 95% target success probability, and posterior P(effect > 0) > 0.95, required n per arm was 18, 5, 2, and 2 for effects 5, 10, 15, and 20. A matched one-sided alpha 0.05 calculation gave the same rounded sizes. Tightening both thresholds to 0.975 / alpha 0.025 gave 22, 6, 3, and 2.

![Main result](results/success-probability.png)

## What the analysis does

The executable analysis is [analysis.R](analysis.R). [Methods and interpretation](REPORT.md) explains the scope; [revision notes](REVISION_NOTES.md) distinguish the original analysis from the portfolio revision.

## Run locally

Use R 4.5.2; only base R is required.
Read [data access and input requirements](DATA_ACCESS.md), then run from this repository:

```sh
Rscript analysis.R results
```

## Results and limits

This is a hypothetical known-variance design, not a clinical trial recommendation. Fixed-true-effect success probability is not assurance integrated over a design prior. Extremely small calculated sample sizes reflect the strong modeling assumptions; no practical minimum, dropout, or operational constraints are included.

The committed `results/` files are generated summaries from the portfolio revision. Source records, credentials, fitted models, and original notebook outputs are excluded.

