# Methods and interpretation

## Geometry and evaluation

Halfmoon contains two interleaved arcs. Bullseye contains three concentric rings. K-means on the original coordinates assigns points to their nearest centroid. The straight boundaries cut across the curved and nested structures. The clustering fits use the coordinates and known cluster counts. Reference labels are used after fitting for adjusted Rand index (ARI) and to align display colors by largest total overlap. Display colors leave the fitted assignments and scores unchanged.

## Affinities and embedding

[analysis.py](analysis.py) builds an undirected nearest-neighbor graph by symmetrizing the binary neighbor matrix. It compares 5, 10, 15 and 20 neighbors. The separate Gaussian RBF graph weights point pairs by their squared distances with σ² = 0.01 for Halfmoon and 0.1 for Bullseye. Self edges are zero.

Given affinity A and its degree matrix D, the analysis takes the leading k eigenvectors of D⁻¹ᐟ² A D⁻¹ᐟ². These correspond to the smallest eigenvalues of the symmetric normalized Laplacian. It normalizes each row of the embedding and runs k-means on the resulting coordinates, with k = 2 for Halfmoon and k = 3 for Bullseye. The code counts connected components and rejects zero-degree nodes. The [tests](test_analysis.py) cover a three-block graph and the isolated-node failure case.

## Results

Ordinary k-means scored 0.253 and 0.004 for Halfmoon and Bullseye. The Gaussian RBF run scored 1.0 for both. The neighbor comparison makes the role of graph construction visible:

| Neighbors | Halfmoon components | Halfmoon ARI | Bullseye components | Bullseye ARI, saved |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 2 | 1.0 | 5 | 0.923 |
| 10 | 2 | 1.0 | 3 | 1.0 |
| 15 | 2 | 1.0 | 3 | 1.0 |
| 20 | 2 | 1.0 | 3 | 1.0 |

At five neighbors, Bullseye has five components but the embedding keeps three eigenvectors. The repeated leading eigenvalue leaves this three-dimensional selection non-unique. A rerun with the default local thread settings reproduced the saved score. When the numerical libraries used different thread settings, they returned different embeddings and ARIs for that cell. Each rerun recovered the five-component diagnosis. The 10, 15 and 20 neighbor runs and the RBF runs reproduced the saved scores.

## Scope and revision

The original notebook compared k-means, Laplacian eigenvectors, a neighbor grid and Gaussian affinities. Different original sections handled the embedding and cluster count differently. The portfolio revision fixes the cluster counts at two and three, separates the number of graph neighbors from the embedding dimension, and reports graph connectivity. The two benchmark scores describe recovery with known cluster counts and selected affinities. Generalization to other data and performance at large scale remain open. [Revision notes](REVISION_NOTES.md)

## Outputs

- [Run metadata](results/run.json) and [complete results](results/clustering-comparison.csv)
- [Halfmoon assignments](results/halfmoon-assignments.png) and [Bullseye assignments](results/bullseye-assignments.png)
- [Original comparison including RBF](results/clustering-comparison.png)
- [Input and access instructions](DATA_ACCESS.md)
