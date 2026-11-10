"""Pipeline completed: degradation, restoration, metrics, figures."""
import csv
from pathlib import Path

import cv2
import matplotlib
matplotlib.use("Agg")            # save figures without X server
import matplotlib.pyplot as plt
import numpy as np

from degrade import degrade, ALPHA, SIGMA, SEED
from methods import METHODS
from metrics import psnr, ssim

ORIG_DIR = Path("data/original")
DEG_DIR = Path("data/degraded")
IMG_DIR = Path("results/images")
FIG_DIR = Path("results/figures")
CSV_PATH = Path("results/metrics.csv")


def rgb(img):
    """BGR (OpenCV) -> RGB (matplotlib)."""
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def save_figure(panels, title, path):
    """Figure nearest. panels = array of (titolo, immagine BGR)."""
    fig, axes = plt.subplots(1, len(panels), figsize=(3.2 * len(panels), 4.5))
    for ax, (name, im) in zip(axes, panels):
        ax.imshow(rgb(im), vmin=0, vmax=255)   # same scale for all images
        ax.set_title(name, fontsize=10)
        ax.axis("off")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    for d in (DEG_DIR, IMG_DIR, FIG_DIR):
        d.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEED)
    rows = []
    print(f"Degradation: alpha={ALPHA}, sigma={SIGMA}, seed={SEED}")

    for path in sorted(ORIG_DIR.glob("*.png")):
        name = path.stem
        orig = cv2.imread(str(path))
        deg = degrade(orig, rng)
        cv2.imwrite(str(DEG_DIR / f"{name}.png"), deg)

        # 1) Sintetic test: methods on degraded image, reference is original
        panels = [("originale", orig), ("degradata", deg)]
        for m_name, fn in METHODS.items():
            out = fn(deg)
            cv2.imwrite(str(IMG_DIR / f"{name}__deg__{m_name}.png"), out)
            rows.append({"image": name, "method": m_name,
                         "psnr": round(psnr(orig, out), 2),
                         "ssim": round(ssim(orig, out), 4)})
            if m_name != "baseline":
                panels.append((m_name, out))
        save_figure(panels, f"{name} - degradazione sintetica",
                    FIG_DIR / f"{name}_synthetic.png")

        # 2) Real test: methods on original image, no reference
        panels = [("originale", orig)]
        for m_name, fn in METHODS.items():
            if m_name == "baseline":
                continue
            out = fn(orig)
            cv2.imwrite(str(IMG_DIR / f"{name}__orig__{m_name}.png"), out)
            panels.append((m_name, out))
        save_figure(panels, f"{name} - immagine reale (senza referenza)",
                    FIG_DIR / f"{name}_real.png")
        print(f"  {name}: fatto")

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["image", "method", "psnr", "ssim"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Metrics saved in {CSV_PATH}")


if __name__ == "__main__":
    main()