"""Revised analysis of lottery assignment; not an effect of insurance receipt."""

from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

COVARIATES = [
    "age_inp",
    "gender_inp",
    "numhh_list",
    "ast_dx_pre_lottery",
    "dia_dx_pre_lottery",
    "hbp_dx_pre_lottery",
    "chl_dx_pre_lottery",
    "ami_dx_pre_lottery",
    "chf_dx_pre_lottery",
    "emp_dx_pre_lottery",
    "kid_dx_pre_lottery",
    "cancer_dx_pre_lottery",
    "dep_dx_pre_lottery",
    "HSorGED",
    "someCollege",
    "collegeGrad",
    "hispanic_inp",
    "race_black_inp",
    "race_nwother_inp",
    "english_list",
    "have_phone_list",
]
# lessHS and race_white_inp are reference categories. num_conditions is excluded
# because it aggregates diagnosis indicators already in the design matrix.
OUTCOMES = ["sbp", "dbp", "a1c"]


def welch_difference(treated, control):
    a = np.asarray(treated, dtype=float)
    b = np.asarray(control, dtype=float)
    if min(len(a), len(b)) < 2:
        raise ValueError("At least two observed outcomes per group required")
    v1 = a.var(ddof=1) / len(a)
    v0 = b.var(ddof=1) / len(b)
    se = np.sqrt(v1 + v0)
    df = (v1 + v0) ** 2 / (v1 * v1 / (len(a) - 1) + v0 * v0 / (len(b) - 1))
    diff = a.mean() - b.mean()
    margin = stats.t.ppf(0.975, df) * se
    return dict(
        estimate=diff,
        se=se,
        lower=diff - margin,
        upper=diff + margin,
        p_value=stats.ttest_ind(a, b, equal_var=False).pvalue,
        n_treated=len(a),
        n_control=len(b),
    )


def run(data, out):
    out.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(data)
    required = set(
        OUTCOMES + COVARIATES + ["randassign", "household_id", "cvd_risk_composite"]
    )
    if not required.issubset(d):
        raise ValueError(f"Missing columns: {sorted(required-set(d))}")
    if (
        not set(d.randassign.dropna().unique()).issubset({0, 1})
        or d.randassign.isna().any()
    ):
        raise ValueError("randassign must be complete and coded 0/1")
    components = [
        "dia_dx_pre_lottery",
        "hbp_dx_pre_lottery",
        "chl_dx_pre_lottery",
        "ami_dx_pre_lottery",
        "chf_dx_pre_lottery",
    ]
    complete = d[["cvd_risk_composite"] + components].dropna()
    composite_is_baseline = bool(
        np.allclose(complete.cvd_risk_composite, complete[components].sum(axis=1))
    )
    if not composite_is_baseline:
        raise ValueError("Composite definition changed; review before interpreting it")
    estimates = []
    missing = []
    balance = []
    for var in COVARIATES:
        a = d.loc[d.randassign.eq(1), var].dropna()
        b = d.loc[d.randassign.eq(0), var].dropna()
        pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
        balance.append(
            dict(
                variable=var,
                assigned_mean=a.mean(),
                control_mean=b.mean(),
                standardized_difference=(
                    (a.mean() - b.mean()) / pooled if pooled else np.nan
                ),
            )
        )
    for y in OUTCOMES:
        for g in [0, 1]:
            s = d.loc[d.randassign.eq(g), y]
            missing.append(
                dict(
                    outcome=y,
                    assignment=g,
                    total=len(s),
                    observed=s.notna().sum(),
                    missing_rate=s.isna().mean(),
                )
            )
        unadj = d[[y, "randassign", "household_id"]].dropna()
        fit0 = sm.OLS(unadj[y], sm.add_constant(unadj[["randassign"]])).fit(
            cov_type="cluster", cov_kwds={"groups": unadj.household_id}, use_t=True
        )
        ci0 = fit0.conf_int().loc["randassign"]
        estimates.append(
            dict(
                outcome=y,
                model="Unadjusted (household clustered)",
                estimate=fit0.params["randassign"],
                se=fit0.bse["randassign"],
                lower=ci0.iloc[0],
                upper=ci0.iloc[1],
                p_value=fit0.pvalues["randassign"],
                n_treated=int(unadj.randassign.sum()),
                n_control=int((unadj.randassign == 0).sum()),
            )
        )
        rows = d[[y, "randassign", "household_id"] + COVARIATES].dropna()
        X = sm.add_constant(
            pd.get_dummies(
                rows[["randassign"] + COVARIATES],
                columns=["numhh_list"],
                drop_first=True,
                dtype=float,
            ).astype(float)
        )
        if np.linalg.matrix_rank(X) < X.shape[1]:
            raise ValueError("Adjusted design matrix is rank deficient")
        fit = sm.OLS(rows[y], X).fit(
            cov_type="cluster", cov_kwds={"groups": rows.household_id}, use_t=True
        )
        ci = fit.conf_int().loc["randassign"]
        estimates.append(
            dict(
                outcome=y,
                model="Adjusted (household clustered)",
                estimate=fit.params["randassign"],
                se=fit.bse["randassign"],
                lower=ci.iloc[0],
                upper=ci.iloc[1],
                p_value=fit.pvalues["randassign"],
                n_treated=int(rows.randassign.sum()),
                n_control=int((rows.randassign == 0).sum()),
            )
        )
    results = pd.DataFrame(estimates)
    results.to_csv(out / "estimates.csv", index=False)
    pd.DataFrame(missing).to_csv(out / "missingness.csv", index=False)
    pd.DataFrame(balance).to_csv(out / "balance.csv", index=False)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), layout="constrained")
    for ax, y in zip(axes, OUTCOMES):
        r = results.loc[results.outcome.eq(y)]
        ax.errorbar(
            r.estimate,
            [0, 1],
            xerr=[r.estimate - r.lower, r.upper - r.estimate],
            fmt="o",
            color="#23597a",
            capsize=4,
        )
        ax.axvline(0, color="#999", lw=1)
        ax.set_yticks([0, 1], ["Unadjusted", "Adjusted"])
        ax.set_title(y)
        ax.set_xlabel("Assignment difference (95% CI)")
        ax.set_ylim(-0.6, 1.6)
    fig.savefig(out / "assignment-effects.png", dpi=170)
    plt.close(fig)
    meta = {
        "rows": len(d),
        "assigned": int(d.randassign.sum()),
        "controls": int((d.randassign == 0).sum()),
        "excluded_outcome": "cvd_risk_composite exactly equals five pre-lottery diagnosis indicators; retained as a baseline characteristic, not a follow-up endpoint.",
        "inference": "Household-clustered intervals; adjusted for household-list size categories. Unweighted educational reanalysis, not a full replication of the original trial estimand/design.",
    }
    (out / "run.json").write_text(json.dumps(meta, indent=2))
    print(
        results[["outcome", "model", "estimate", "lower", "upper"]].to_string(
            index=False
        )
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("results"))
    a = p.parse_args()
    run(a.data, a.output)
