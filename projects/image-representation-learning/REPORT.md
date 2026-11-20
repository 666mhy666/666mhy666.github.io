# Methods and interpretation

## Original coursework

The original notebook loaded the first 10,000 sorted files from the course copy of CelebA. It resized RGB images to 64 × 64, converted them to grayscale and scaled the flattened 4,096 pixels to [0, 1]. Full PCA on those images retained 218 components and a cumulative explained-variance fraction of 0.95009404. The autoencoder and VAE used 128 and 64 latent dimensions, respectively, and logged losses over ten training epochs. The original models reconstructed training examples.

The VAE encoder produced a mean and log variance. The decoder generated ten examples from 64-dimensional standard-normal draws. For the latent perturbation exercise, both networks decoded the same code before and after adding Gaussian noise with SD 0.5. The AE began from a deterministic encoder output and the VAE from a posterior sample. These examples qualitatively explore what happens when latent coordinates change. They do not establish semantic disentanglement or a quantitative robustness advantage.

### Recover the aggregate PCA curve

The [coursework variance script](pca_variance.py) uses the original order of operations, resizing in RGB before converting to grayscale. It computes cumulative explained variance from the spectrum of the centered pixel scatter matrix. The release exports only an aggregate fraction for each component count through 512. Run it with the same authorized original image sample, then regenerate figures in the same directory as the benchmark tables:

```sh
python pca_variance.py --images /path/to/authorized/images --output data/reproduced-results/pca-variance.csv
python plot_results.py --results data/reproduced-results
```

The historical curve uses all 10,000 original images. The benchmark PCA is fit separately using only its training split and a fixed 64-component projection.

## September 2026 controlled experiment

[analysis.py](analysis.py) sorts the input files, uses the first 10,000, converts to grayscale, and resizes them to 64 × 64 by bilinear interpolation. Seed 42 selects a random split of 8,000 training, 1,000 validation and 1,000 test images. All methods use 64 dimensions. PCA uses a randomized SVD fit on the training images. The two dense neural networks use Adam with a learning rate of 0.001 and a batch size of 128 for ten epochs.

The AE trains with mean pixel-squared error. The VAE uses a per-image sum of squared pixel differences plus a KL penalty toward the standard normal prior. Both checkpoints are selected by the same validation pixel MSE. For VAE validation and test, the decoder receives the posterior mean. The lowest saved validation MSE for each network occurred at epoch 10. The training-objective columns represent different quantities, so the validation figure compares pixel MSE only.

| Model | Test pixel MSE |
| --- | ---: |
| PCA | 0.007495934143662453 |
| AE | 0.01676837992668152 |
| VAE | 0.0359960868358612 |

## Interpretation and boundaries

PCA had the smallest pixel error under the shared representation size, image split, preprocessing, and test metric. The methods use different objectives and parameter counts. Their fitting procedures also differ: PCA uses a decomposition, while the neural models learn by iterative optimization within the ten-epoch budget. The result does not establish neural convergence or rank perceptual quality, prior samples, or generalization to other data.

A random image-level split may place images of the same identity in multiple sets. The reported MSE describes held-out images. Identity-level generalization remains untested. The dataset provider restricts redistribution. The release contains aggregate numerical summaries and diagrams, while photos, individual reconstructions, generated faces, and fitted weights remain private. [CelebA dataset terms](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)

## Outputs

- [Held-out scores](results/reconstruction-metrics.csv) and [comparison chart](results/reconstruction-comparison.png)
- [AE history](results/ae-history.csv), [VAE history](results/vae-history.csv) and [validation chart](results/validation-history.png)
- [Coursework PCA variance](results/pca-variance.csv) and [coursework variance chart](results/pca-variance.png)
- [Run metadata](results/run.json), [authorized inputs](DATA_ACCESS.md) and [revision history](REVISION_NOTES.md)
