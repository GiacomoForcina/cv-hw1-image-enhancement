# Image Enhancement and Restoration

This project compares simple image-enhancement methods on four photographs. It evaluates results in two ways: against known originals after applying a reproducible synthetic degradation, and visually on the original photographs, where no ground-truth reference is available.

## Requirements

Use Python 3 and install the dependencies listed in `requirements.txt`:
    Tested with Python 3.14.3 on Windows 11.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the commands below from the project root. On macOS or Linux, activate the environment with `source .venv/bin/activate` instead.

## Prepare the images


The processed originals are already included in `data/original/`, so this step is
not needed to reproduce the results. `src/prepare_images.py` was run once to resize
the source photographs (longest side ≤ 1000 px) and save them as PNG; the source
folder `foto_raw/` is not included in the repository. The photographs are
attributed in [data/SOURCES.md](data/SOURCES.md).

## Run the experiment

```powershell
python src/run.py
```

For each processed original, the script creates a synthetic degraded image using contrast factor `0.5` and Gaussian noise with standard deviation `8`. The random generator uses seed `42`, making the degradation reproducible for a stable input set.

The methods in `src/methods.py` are:

| Method | Operation |
| --- | --- |
| `baseline` | Leaves the input unchanged. |
| `stretch_rgb` | Stretches each BGR color channel between its 1st and 99th percentiles. |
| `stretch_lab` | Stretches the lightness channel between its 1st and 99th percentiles in Lab color space. |
| `equalize_lab` | Equalizes the lightness-channel histogram in Lab color space. |
| `denoise_equalize` | Applies colored non-local-means denoising, then Lab lightness equalization.      (h=6, template window 7, search window 21) |

For the **synthetic test**, each method processes the degraded image. PSNR and SSIM are measured against the corresponding original and saved in `results/metrics.csv`. For the **real-image comparison**, enhancement methods process the original photographs; comparison figures are saved without reference metrics because there is no separate ground truth.

## Output files

- `data/original/`: resized input PNGs.
- `data/degraded/`: synthetically degraded PNGs.
- `results/images/`: per-method output PNGs for degraded and original inputs.
- `results/figures/`: synthetic-test and real-image comparison figures.
- `results/metrics.csv`: per-image and per-method PSNR and SSIM for the synthetic test.

Generated outputs are overwritten when the experiment is run again.

## Project layout

```text
data/original/      Resized PNG inputs
data/degraded/      Synthetic degraded images
src/prepare_images.py
src/degrade.py      Synthetic degradation
src/methods.py      Enhancement methods
src/metrics.py      PSNR and SSIM calculations
src/run.py          Experiment and output generation
results/            Metrics, processed images, and figures
```
