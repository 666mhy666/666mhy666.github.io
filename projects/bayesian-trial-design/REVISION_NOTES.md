# Revision notes

## Original coursework

The original project compared Bayesian and frequentist sample-size planning for a hypothetical two-arm LDL trial. It used normal-normal updating, candidate effect sizes and simulation across an enrollment grid. The report described an 80% design target. The executable R Markdown used a 95% target and paired a 0.95 posterior cutoff with a one-sided frequentist α of 0.025.

## September 2026 analysis revision

The public analysis fixed the design target at 95% and paired each posterior cutoff with its corresponding one-sided frequentist threshold. It replaced the simulation grid for determining sample size with an exact normal tail calculation. A seeded simulation checks the resulting design probabilities. An unmet target returns NA. The separate design-prior assurance helper remains distinct from the fixed-effect calculations in the main results.

## November 2026 presentation revision

The case study separates the rule applied after observing data from the success probability used to plan enrollment. The probability figure now marks the first qualifying n on each curve. The sample-size and simulation outputs are unchanged. Coding-assistant support was used for documentation, figure presentation and reproduction checks.
