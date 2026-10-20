import numpy as np
from scipy.signal import lfilter

NOISE_IDS = {"white": 1, "colored": 2, "impulsive": 3}
NOISE_SPEC = {
    "white": "independent standard Gaussian before per-realization scaling",
    "colored": "Gaussian AR(1), rho=0.8, 256-sample burn-in before scaling",
    "impulsive": "Gaussian background SD=0.05 plus Bernoulli(p=0.01) times Gaussian SD=1 before scaling",
    "normalization": "exact finite-sequence energy SNR; includes signal DC; no clipping",
}


def corrupt(clean, noise_type, snr_db, seed_parts):
    x = np.asarray(clean, dtype=np.float64)
    if x.ndim != 1 or not np.all(np.isfinite(x)) or np.linalg.norm(x) == 0:
        raise ValueError("Noise scaling requires a finite nonzero 1D signal.")
    if not np.isfinite(snr_db):
        raise ValueError("SNR must be finite.")
    rng = np.random.default_rng(np.random.SeedSequence([*seed_parts, NOISE_IDS[noise_type]]))
    if noise_type == "white":
        n = rng.standard_normal(x.size)
    elif noise_type == "colored":
        n = lfilter([np.sqrt(1-0.8**2)], [1, -0.8], rng.standard_normal(x.size+256))[256:]
    else:
        n = 0.05*rng.standard_normal(x.size)
        n += (rng.random(x.size) < 0.01) * rng.standard_normal(x.size)
    norm = np.linalg.norm(n)
    if norm == 0:
        raise ValueError("Zero-energy noise realization.")
    n *= np.linalg.norm(x) / norm * 10**(-float(snr_db)/20)
    return x + n
