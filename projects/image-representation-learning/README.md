# Comparing PCA, Autoencoders, and VAEs

I used PCA, a dense autoencoder (AE), and a variational autoencoder (VAE) to represent 64 × 64 grayscale images. The coursework explored reconstruction, generation and changes in latent codes. A later experiment put all three methods at 64 dimensions and compared their pixel reconstruction error on the same held-out images.

[Read the case study](https://666mhy666.github.io/projects/image-representation-learning/) · [Open the Python analysis](analysis.py) · Independent UCLA graduate coursework

## Original coursework

With the first 10,000 sorted images from the course copy of CelebA, PCA reached 95% explained variance at 218 components. The original AE used 128 dimensions and the VAE used 64. The notebook included training-image reconstruction comparisons and training-loss logs. It decoded ten standard-normal VAE samples and compared reconstructions from clean and Gaussian-perturbed codes for both neural models. See the [coursework PCA curve](results/pca-variance.png) and the [methods report](REPORT.md).

## Controlled portfolio experiment

The September 2026 experiment used a shared random image split (8,000 train, 1,000 validation, 1,000 test), seed 42, and 64 dimensions for each method. Both networks trained for ten epochs. I selected checkpoints by validation pixel MSE and decoded the VAE posterior mean for validation and test.

| Model | Held-out pixel MSE |
| --- | ---: |
| PCA | 0.00750 |
| Dense autoencoder | 0.01677 |
| Variational autoencoder | 0.03600 |

PCA had the lowest error under this setup. Architecture and training budget affect neural-network results, and the VAE balances reconstruction with latent regularization. Pixel MSE measures pixel fidelity. Perceptual quality and generative usefulness are separate questions. The image-level split allows possible identity overlap across sets.

## Reproduce the benchmark

Use an authorized local copy of the images. Follow the [data access instructions](DATA_ACCESS.md) before running. The commands below create a separate reproduction directory:

```sh
python -m pip install -r requirements.txt
python analysis.py --images /path/to/authorized/images --limit 10000 --latent-dim 64 --epochs 10 --seed 42 --output data/reproduced-results
python plot_results.py --results data/reproduced-results
```

For a software check using generated noise, run `python analysis.py --smoke-test --epochs 1 --output data/reproduced-results`. It writes into the `smoke-test/` subdirectory. The formal figures use the saved benchmark outputs. The [report](REPORT.md) documents a separate command for the coursework variance curve.

[Metrics](results/reconstruction-metrics.csv) · [AE history](results/ae-history.csv) · [VAE history](results/vae-history.csv) · [Run metadata](results/run.json) · [Revision history](REVISION_NOTES.md)

The release uses aggregate summaries and method diagrams. Individual photos, reconstructions, generated faces, and fitted weights remain private.
