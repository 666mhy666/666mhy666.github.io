# Methods and interpretation

## Hypothetical design

Two independent arms have equal sample size n and normally distributed outcomes with known within-arm SD 4.5. Define the observed difference D so that larger values favor the new LDL-lowering treatment over the active comparator. Under an assumed true difference δ, D is normal with mean δ and variance 2σ²/n. The analysis prior for δ is N(0, 100²).

## Evidence rule and design probability

The posterior is normal. Its variance is (1/100² + n/(2σ²))⁻¹ and its mean is that variance times nD/(2σ²). A result clears the evidence rule if the posterior probability that δ is positive exceeds the selected threshold.

[analysis.R](analysis.R) converts the posterior rule to an observed-difference cutoff. It computes the upper normal tail above that cutoff at each candidate n and each fixed true δ. The required n is the first whole number for which that probability reaches 0.95. The design target is held fixed when the posterior threshold changes. The separate `design_assurance()` helper integrates the success probability over a normal design prior for δ. The main table uses the fixed-δ calculation.

## Matched frequentist comparison

The comparison uses one-sided normal tests with α = 0.05 or 0.025 and a 95% power target. These α values correspond to the posterior cutoffs of 0.95 and 0.975 in the flat-prior limit. The implemented prior is diffuse but finite. It gives a cutoff close to the corresponding normal-test cutoff, and the two calculations gave the same rounded sample sizes in all four scenarios. The agreement depends on these assumptions. [Sample-size table](results/sample-sizes.csv)

## Monte Carlo check

At each required n for the 0.95 posterior rule, the script uses seed 203 to draw 100,000 trial-level estimates from the normal sampling distribution for that scenario. It computes the fraction with posterior probability above 0.95 and records the Monte Carlo standard error. For δ = 5 at n = 18 per arm, the probabilities were 95.432% by the exact calculation and 95.455% by simulation. The largest absolute gap across the four checks was about 0.10 percentage points. [Simulation results](results/simulation-check.csv)

## Scope and revision

Variance is assumed known. Several assumed differences are large relative to the within-arm SD. There is no dropout allowance, minimum enrollment rule, or operational planning constraint. The sample sizes are illustrations from this hypothetical normal model.

The original report used an 80% planning target in its description. The original code used 95% for its Bayesian design probability and frequentist power target, with posterior cutoff 0.95 and one-sided α = 0.025. The revised analysis makes the 95% design target explicit, matches the decision cutoffs and verifies the exact probabilities by simulation. [Revision notes](REVISION_NOTES.md)

## Outputs

- [Sample sizes](results/sample-sizes.csv)
- [Simulation verification](results/simulation-check.csv)
- [Design probability curves](results/success-probability.png)
- [R session information](results/session-info.txt)
