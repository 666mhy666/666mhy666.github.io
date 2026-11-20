# Data access

The benchmark uses the first 10,000 filenames in sorted order from an authorized local copy of the CelebA course images. It accepts JPEG or PNG, converts the images to grayscale, resizes to 64 × 64 and scales pixel values to [0, 1]. Exact reproduction depends on the same source copy and preprocessing. The separate coursework PCA variance script uses the original resize-before-grayscale preprocessing order.

Review the provider’s terms before obtaining or using the images. Course access does not establish permission to redistribute individual images or derivative examples. Keep the inputs in a local data directory. The portfolio includes aggregate figures and summaries. Source photos, reconstructions, generated faces and trained model weights remain private. [CelebA dataset and terms](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)
