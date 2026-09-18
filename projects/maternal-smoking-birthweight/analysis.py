"""Observational birth weight analysis with robust uncertainty and explicit cohorts."""

from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ADJUST = ["mage", "mrace", "medu", "mmarried", "alcohol"]


def encode_smoking(s):
    if not set(s.dropna().unique()).issubset({0, 1, 2, 3}):
        raise ValueError("Unexpected smoking intensity code")
    return s.gt(0).astype(float).where(s.notna())


def run(data, out):
    out.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(data)
    required = ["bweight", "msmoke"] + ADJUST
    if not set(required).issubset(d):
        raise ValueError("Required variables are missing")
    d["smoker"] = encode_smoking(d.msmoke)
    # Keep both fits on identical observations for an interpretable comparison.
    cohort = d[["bweight", "msmoke", "smoker"] + ADJUST].dropna().copy()
    fits = {
        "Unadjusted": smf.ols("bweight ~ smoker", cohort).fit(cov_type="HC3"),
        "Adjusted": smf.ols(
            "bweight ~ smoker + mage + mrace + medu + mmarried + alcohol", cohort
        ).fit(cov_type="HC3"),
        "Intensity": smf.ols(
            "bweight ~ C(msmoke) + mage + mrace + medu + mmarried + alcohol", cohort
        ).fit(cov_type="HC3"),
    }
    rows = []
    for name, fit in fits.items():
        if np.linalg.matrix_rank(fit.model.exog) < fit.model.exog.shape[1]:
            raise ValueError("Rank-deficient design")
        for term in fit.params.index:
            if term == "smoker" or term.startswith("C(msmoke)"):
                ci = fit.conf_int().loc[term]
                rows.append(
                    dict(
                        model=name,
                        term=term,
                        estimate=fit.params[term],
                        se=fit.bse[term],
                        lower=ci.iloc[0],
                        upper=ci.iloc[1],
                        p_value=fit.pvalues[term],
                        n=int(fit.nobs),
                    )
                )
    results = pd.DataFrame(rows)
    results.to_csv(out / "estimates.csv", index=False)
    balance = []
    for var in ADJUST:
        a = cohort.loc[cohort.smoker.eq(1), var]
        b = cohort.loc[cohort.smoker.eq(0), var]
        pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
        balance.append(
            dict(
                variable=var,
                smokers=a.mean(),
                nonsmokers=b.mean(),
                smd=(a.mean() - b.mean()) / pooled if pooled else np.nan,
            )
        )
    pd.DataFrame(balance).to_csv(out / "balance.csv", index=False)
    # Sparse observed strata are a diagnostic, not proof of positivity everywhere.
    categories = pd.cut(
        cohort.medu,
        [-np.inf, 11, 12, 15, np.inf],
        labels=["<=11", "12", "13-15", "16+"],
    )
    counts = pd.crosstab([categories, cohort.mrace], cohort.smoker).reindex(
        columns=[0.0, 1.0], fill_value=0
    )
    counts.columns = ["nonsmokers", "smokers"]
    counts.to_csv(out / "overlap-counts.csv")
    fig, ax = plt.subplots(figsize=(7, 3.7), layout="constrained")
    y = np.arange(len(results))
    ax.errorbar(
        results.estimate,
        y,
        xerr=[results.estimate - results.lower, results.upper - results.estimate],
        fmt="o",
        color="#23597a",
        capsize=4,
    )
    labels = ["Unadjusted", "Adjusted"] + [
        f"Smoking intensity {i} vs 0" for i in [1, 2, 3]
    ]
    ax.set_yticks(y, labels)
    ax.axvline(0, color="#999", lw=1)
    ax.set_xlabel("Birth weight difference in grams (HC3 95% CI)")
    ax.set_title("Maternal smoking and birth weight")
    fig.savefig(out / "birthweight-associations.png", dpi=170)
    plt.close(fig)
    (out / "run.json").write_text(
        json.dumps(
            {
                "input_rows": len(d),
                "complete_cases": len(cohort),
                "smokers": int(cohort.smoker.sum()),
                "interpretation": "Adjusted associations; no formal unmeasured-confounding sensitivity analysis.",
            },
            indent=2,
        )
    )
    print(results.to_string(index=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("results"))
    a = p.parse_args()
    run(a.data, a.output)
