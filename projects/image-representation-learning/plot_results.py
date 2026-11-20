"""Plot aggregate metrics only; no source images are exported."""

import argparse
import json
from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def plot_benchmark(results):
    metrics = pd.read_csv(results / "reconstruction-metrics.csv")
    fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
    ax.bar(metrics.model, metrics.test_pixel_mse, color=["#23597a", "#7898aa", "#ad6b34"])
    ax.set(
        ylabel="Held-out pixel MSE (lower is better)",
        title="64-dimensional representations; 1,000 test images",
    )
    for i, value in enumerate(metrics.test_pixel_mse):
        ax.text(i, value + 0.0006, f"{value:.4f}", ha="center")
    ax.set_ylim(0, metrics.test_pixel_mse.max() * 1.18)
    fig.savefig(results / "reconstruction-comparison.png", dpi=170)
    plt.close(fig)


def plot_validation(results, epochs):
    fig, ax = plt.subplots(figsize=(6.7, 3.65), layout="constrained")
    for model, color in (("AE", "#23597a"), ("VAE", "#ad6b34")):
        history = pd.read_csv(results / f"{model.lower()}-history.csv")
        best = history.loc[history.validation_mse.idxmin()]
        ax.plot(history.epoch, history.validation_mse, lw=2, color=color, label=model)
        ax.scatter(best.epoch, best.validation_mse, s=40, color=color, zorder=3)
    ax.set(
        xlabel="Training epoch",
        ylabel="Validation pixel MSE",
        xticks=range(1, epochs + 1),
        ylim=(0, None),
    )
    ax.legend(frameon=False)
    fig.savefig(results / "validation-history.png", dpi=170)
    plt.close(fig)


def plot_variance(results):
    curve = pd.read_csv(results / "pca-variance.csv")
    fig, ax = plt.subplots(figsize=(6.7, 3.65), layout="constrained")
    ax.plot(curve.components, curve.cumulative_variance, lw=2.25, color="#23597a")
    ax.axhline(0.95, ls="--", lw=1, color="#7898aa", label="95% variance")
    qualifying = curve.loc[curve.cumulative_variance.ge(0.95)]
    if not qualifying.empty:
        first = qualifying.iloc[0]
        ax.scatter(first.components, first.cumulative_variance, s=38, color="#23597a")
        ax.annotate(
            f"{int(first.components)} components",
            (first.components, first.cumulative_variance),
            xytext=(16, -30),
            textcoords="offset points",
            arrowprops={"arrowstyle": "-", "color": "#586f80"},
        )
    ax.set(
        xlabel="Principal components kept",
        ylabel="Cumulative variance explained",
        xlim=(0, curve.components.max()),
        ylim=(0, 1.03),
    )
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.legend(loc="lower right", frameon=False)
    fig.savefig(results / "pca-variance.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=Path(__file__).parent / "results")
    results = parser.parse_args().results
    run = json.loads((results / "run.json").read_text(encoding="utf-8"))
    if run["data"] != "user supplied images":
        raise ValueError("Presentation plots require formal results, not a smoke test")
    plot_benchmark(results)
    plot_validation(results, run["epochs"])
    if (results / "pca-variance.csv").is_file():
        plot_variance(results)
