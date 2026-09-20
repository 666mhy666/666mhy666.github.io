# Methods and interpretation

## Question

In the supplied Oregon Health Insurance Experiment teaching extract, how do measured health outcomes differ by lottery assignment?

## Data

12,134 individuals. The course-supplied ohie.csv is not redistributed. An authorized copy of that exact teaching extract is needed to reproduce these numbers. The original study’s public materials provide context, but are not asserted to be the identical extract.

## Analysis

I estimated unadjusted and covariate-adjusted assignment differences with household-clustered uncertainty, checked baseline balance and missingness, and verified the definition of a composite variable before choosing the outcomes.

The entry point is `analysis.py`. Parameters, variables, assumptions, and analysis cohorts are recorded in the code and generated result files.

## Findings

Adjusted assignment differences were 0.145 for systolic blood pressure (95% CI −0.373 to 0.663), 0.216 for diastolic pressure (−0.184 to 0.616), and −0.0027 for HbA1c (−0.0203 to 0.0149), on the supplied dataset scales. All intervals include zero; this is not evidence that insurance has no health effects.

![Lottery-assignment differences with 95% household-clustered confidence intervals.](results/assignment-effects.png)

_Lottery-assignment differences with 95% household-clustered confidence intervals._

## Assumptions and interpretation

The estimand is lottery assignment, not insurance receipt. This unweighted teaching-data reanalysis is not a full replication of the original study’s sampling design, weights, missingness treatment, or estimand. The source extract’s transformation and sampling documentation are incomplete.

## Result files

- [assignment-effects.png](results/assignment-effects.png)
- [balance.csv](results/balance.csv)
- [estimates.csv](results/estimates.csv)
- [missingness.csv](results/missingness.csv)
- [run.json](results/run.json)
Source context: [https://www.nber.org/research/data/oregon-health-insurance-experiment-data](https://www.nber.org/research/data/oregon-health-insurance-experiment-data)

