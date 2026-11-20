# Revision notes

## Original coursework

The clustering work compared k-means, nearest-neighbor graphs and Gaussian affinities on Halfmoon and Bullseye. It used a Laplacian embedding for the unweighted examples and a degree-normalized affinity for the weighted analysis. Parts of the original notebook used the same tuning parameter for embedding dimension and cluster count. Unrelated image exercises stay outside this project.

## September 2026 analysis revision

The revised pipeline fixes the known cluster counts at two and three while varying graph neighbors. It uses k leading normalized-affinity eigenvectors, normalizes the embedding rows and diagnoses disconnected components and isolated nodes. Both Gaussian affinity evaluations and the full nearest-neighbor grid are preserved.

## November 2026 presentation revision

The new figures show the same coordinates colored by supplied reference labels, k-means or the 10-neighbor spectral assignments. They reuse the existing fits. The original comparison including RBF and the saved result table are preserved. The report documents the numerical sensitivity of the over-fragmented five-neighbor Bullseye embedding. Coding-assistant support was used for documentation, figure presentation and reproduction checks.
