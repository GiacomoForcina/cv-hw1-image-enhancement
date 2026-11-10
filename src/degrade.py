import numpy as np

# degradation parameters
ALPHA = 0.5   # 1 = same, 0.5 = half contrast
SIGMA = 8.0    
SEED = 42     #fixed


def degrade(img, rng, alpha=ALPHA, sigma=SIGMA):
    """

    img: image BGR uint8
    rng: numpy generator (np.random.default_rng(SEED))
    """
    f = img.astype(np.float32)                    # no overflow
    mean = f.mean()
    g = alpha * (f - mean) + mean                 # compression
    g = g + rng.normal(0.0, sigma, size=f.shape)  # gaussian noise
    return np.clip(g, 0, 255).astype(np.uint8)    # valid range