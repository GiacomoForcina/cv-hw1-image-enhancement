import cv2
import numpy as np

# Parameters 
P_LOW, P_HIGH = 1, 99   # stretching  
NLM_H = 6             # denoising non-local means


def baseline(img):
    """No elaboration"""
    return img.copy()


def _stretch_channel(c):
    """Linear stretching between P_LOW and P_HIGH."""
    c = c.astype(np.float32)
    lo, hi = np.percentile(c, [P_LOW, P_HIGH])
    out = (c - lo) / max(hi - lo, 1e-6) * 255.0   # g = a*f + b
    return np.clip(out, 0, 255).astype(np.uint8)


def stretch_rgb(img):
    """Stretching for each channel independently."""
    return cv2.merge([_stretch_channel(c) for c in cv2.split(img)])


def stretch_lab(img):
    """Stretching only on L, a and b remain unchanged."""
    L, a, b = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))
    return cv2.cvtColor(cv2.merge([_stretch_channel(L), a, b]), cv2.COLOR_LAB2BGR)


def equalize_lab(img):
    """Equalization of the histogram only on L."""
    L, a, b = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))
    return cv2.cvtColor(cv2.merge([cv2.equalizeHist(L), a, b]), cv2.COLOR_LAB2BGR)


def denoise_equalize(img):
    """Denoising (non-local means), than equalization"""
    den = cv2.fastNlMeansDenoisingColored(img, None, NLM_H, NLM_H, 7, 21)
    return equalize_lab(den)


METHODS = {
    "baseline": baseline,
    "stretch_rgb": stretch_rgb,
    "stretch_lab": stretch_lab,
    "equalize_lab": equalize_lab,
    "denoise_equalize": denoise_equalize,
}