# Revision notes

## Original coursework

The notebook analyzed PCA variance, compared training-image reconstructions at unequal dimensions (PCA 218, AE 128, VAE 64), generated VAE samples and compared clean and noise-perturbed codes. The original work and face examples remain in the private archive.

## September 2026 benchmark

The revised analysis uses an 80/10/10 random image split with seed 42, matched 64-dimensional representations and ten epochs for both neural models. Checkpoints are selected by validation pixel MSE. The VAE is decoded at the posterior mean for validation and test. All reported test metrics are mean squared pixel errors on the held-out images. The smoke test uses generated noise and a separate output directory.

## November 2026 presentation revision

The case study now separates the original qualitative exercises from the held-out benchmark. The coursework PCA variance curve was recomputed from the matching authorized inputs using the original preprocessing. The validation figure is generated from the saved September histories. No benchmark model was refit, and its numerical files and original comparison chart were preserved. Coding-assistant support was used for documentation, aggregate plots and validation checks.
