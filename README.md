# IEM5063 Network Project

# Modified Stoer-Wagner Image Segmentation

An implementation of the Stoer-Wagner global minimum cut algorithm, modified for unsupervised binary image segmentation.

## Overview

The standard Stoer-Wagner algorithm finds the global minimum cut of an undirected weighted graph. Applied naively to a pixel adjacency graph, it always produces a degenerate result, peeling off a single corner pixel rather than finding a meaningful boundary. This project modifies the algorithm with a new edge weight function and a volume-normalized scoring criterion to make it produce useful segmentations.

## Files

- `read.py` — loads a grayscale PNG and builds a weighted pixel adjacency graph
- `stoer_wagner.py` — the modified algorithm
- `main.ipynb` — loads an image, runs the algorithm, and displays the result

## Requirements

```
pip install networkx pillow matplotlib numpy
```

## Usage

```bash
python main.py dat/circle.png
python main.py dat/circle.png 32   # optional size argument, default 16
```

The size argument controls the resolution the image is downsampled to before building the graph. Larger values produce better results but are significantly slower due to the O(n³) complexity.

## How It Works

Each pixel becomes a node. Edges connect 4-connected neighbors with weight:

```
w(u, v) = 1 / (epsilon + |I_u - I_v|)
```

This makes interior edges (identical pixels) very expensive to cut and boundary edges cheap, which steers the algorithm toward real image boundaries.

Candidate cuts are scored by:

```
score = cut_weight / min(vol(S), vol(T))
```

where vol is the total incident edge weight of a partition. This penalizes small isolated cuts and is inspired by the normalized cut criterion of Shi and Malik (2000).

## Limitations

- Works best on simply connected shapes with clear intensity boundaries
- Fails on images with multiple disconnected foreground regions (single cut only)
- Slow above 32×32 due to O(n³) complexity
- Tuned for binary images, not natural grayscale images

## Results

| Image | Result |
|---|---|
| Circle | Clean segmentation |
| Star | Good, minor errors at tips |
| Circle in rectangle | Fails, multiply connected foreground |
| Smiley face | Fails, disconnected components |

## References

- Stoer, M. and Wagner, F. (1997). A simple min-cut algorithm. *Journal of the ACM*, 44(4):585–591.
- Shi, J. and Malik, J. (2000). Normalized cuts and image segmentation. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 22(8):888–905.
