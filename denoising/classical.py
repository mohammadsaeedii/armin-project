"""Validation-selectable classical filters; no clean target at inference."""
import numpy as np
import pywt
from scipy.ndimage import median_filter, uniform_filter1d
from scipy.signal import savgol_filter


def candidates():
    return {
        "identity": [{}],
        "wavelet": [{"wavelet": w, "level": level} for w in ("haar", "db4", "sym4") for level in (2, 3, 4, 5)],
        "wiener": [{"window": w} for w in (5, 9, 15, 25, 41, 65)],
        "savgol": [{"window": w, "order": p} for w in (5, 9, 15, 25, 41, 65) for p in (2, 3)],
        "median": [{"window": w} for w in (3, 5, 7, 9, 15, 25)],
    }


def denoise(y, method, parameters):
    y = np.asarray(y, dtype=np.float64)
    if y.ndim != 1 or not np.isfinite(y).all():
        raise ValueError("Expected finite 1D input.")
    if method == "identity":
        return y.copy()
    if method == "wavelet":
        wavelet = parameters["wavelet"]
        level = min(parameters["level"], pywt.dwt_max_level(len(y), pywt.Wavelet(wavelet).dec_len))
        coeff = pywt.wavedec(y, wavelet, mode="symmetric", level=level)
        detail = coeff[-1]
        sigma = np.median(np.abs(detail - np.median(detail))) / 0.67448975
        threshold = sigma * np.sqrt(2*np.log(len(y)))
        # Explicit shrinkage avoids division by zero in thresholding constant arrays.
        filtered = [coeff[0]] + [np.sign(c)*np.maximum(np.abs(c)-threshold, 0) for c in coeff[1:]]
        return pywt.waverec(filtered, wavelet, mode="symmetric")[:len(y)]
    if method == "wiener":
        window = parameters["window"]
        mean = uniform_filter1d(y, window, mode="reflect")
        variance = np.maximum(uniform_filter1d(y*y, window, mode="reflect") - mean*mean, 0)
        diff = np.diff(y)
        sigma = np.median(np.abs(diff - np.median(diff))) / (np.sqrt(2)*0.67448975)
        gain = np.maximum(variance - sigma*sigma, 0) / np.maximum(variance, np.finfo(float).eps)
        return mean + gain*(y-mean)
    if method == "savgol":
        return savgol_filter(y, parameters["window"], parameters["order"], mode="mirror")
    if method == "median":
        return median_filter(y, parameters["window"], mode="reflect")
    raise ValueError(f"Unknown method {method}")
