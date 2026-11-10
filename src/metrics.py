from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def psnr(ref, img):
    """PSNR in dB based on the original image."""
    return peak_signal_noise_ratio(ref, img, data_range=255)


def ssim(ref, img):
    """SSIM on color image (1 = identical)."""
    return structural_similarity(ref, img, channel_axis=-1, data_range=255)