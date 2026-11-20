"""Recover the coursework PCA variance curve from authorized local images."""

import argparse
import csv
from pathlib import Path

import numpy as np
from PIL import Image


def cumulative_variance(directory):
    files = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )[:10000]
    if len(files) != 10000:
        raise ValueError("The coursework calculation requires 10,000 images")

    pixels = np.empty((len(files), 64 * 64), dtype=np.float64)
    for row, path in enumerate(files):
        with Image.open(path) as image:
            # Match the notebook: resize in RGB before converting to grayscale.
            gray = image.convert("RGB").resize((64, 64), Image.Resampling.BILINEAR)
            pixels[row] = np.asarray(gray.convert("L"), dtype=np.float32).ravel() / 255

    pixels -= pixels.mean(axis=0)
    scatter = pixels.T @ pixels
    total = np.trace(scatter)
    if not np.isfinite(total) or total <= 0:
        raise ValueError("The input images have no usable pixel variance")
    variance = np.linalg.eigvalsh(scatter)[::-1]
    return np.r_[0.0, np.cumsum(variance) / total]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="Aggregate CSV path.")
    args = parser.parse_args()

    curve = cumulative_variance(args.images)
    first = int(np.searchsorted(curve, 0.95))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("components", "cumulative_variance"))
        writer.writerows(
            (n, f"{fraction:.10f}") for n, fraction in enumerate(curve[:513])
        )
    print(f"95% threshold: {first} components ({curve[first]:.8f} cumulative variance)")
