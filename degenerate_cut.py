import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
 
size = 16
pixels = np.array(Image.open("dat/circle.png").convert("L").resize((size, size))) / 255.0
 
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
 
for ax in axes:
    ax.imshow(pixels, cmap="gray", interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
 
axes[0].set_title("Degenerate cut (weight $\\approx 2$)")
axes[0].plot([0.5, 0.5], [-0.5, 0.5], color="red", linewidth=3)
axes[0].plot([-0.5, 0.5], [0.5, 0.5], color="red", linewidth=3)
 
axes[1].set_title("Boundary cut (weight $\\approx 33$)")
for r in range(size):
    for c in range(size):
        for dr, dc in [(0,1),(1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < size and 0 <= nc < size:
                if (pixels[r,c] > 0.5) != (pixels[nr,nc] > 0.5):
                    if dr == 0:
                        axes[1].plot([c+0.5, c+0.5], [r-0.5, r+0.5], "r-", linewidth=2)
                    else:
                        axes[1].plot([c-0.5, c+0.5], [r+0.5, r+0.5], "r-", linewidth=2)
 
plt.tight_layout()
plt.savefig("figures/degenerate_cut.png", dpi=150, bbox_inches="tight")