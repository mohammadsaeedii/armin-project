import numpy as np


def snr(clean, error):
    signal_energy = np.sum(np.square(clean))
    error_energy = np.sum(np.square(error))
    if signal_energy == 0:
        return float("nan")
    return float("inf") if error_energy == 0 else float(10*np.log10(signal_energy/error_energy))


def evaluate(clean, noisy, estimate, features, boundary=32):
    x, y, z = [np.asarray(v, dtype=np.float64) for v in (clean, noisy, estimate)]
    if x.ndim != 1 or y.shape != x.shape or z.shape != x.shape or not all(np.isfinite(v).all() for v in (x, y, z)):
        raise ValueError("Metric inputs must be finite, equally shaped 1D arrays.")
    if not 0 < boundary < len(x)//2:
        raise ValueError("Invalid boundary width.")
    error = z-x
    input_snr = snr(x, y-x)
    output_snr = snr(x, error)
    r = float(np.corrcoef(x, z)[0, 1]) if np.std(x)>1e-12 and np.std(z)>1e-12 else float("nan")
    px, pz = np.abs(np.fft.rfft(x))**2, np.abs(np.fft.rfft(z))**2
    result = {
        "rmse": float(np.sqrt(np.mean(error**2))),
        "input_snr_db": input_snr,
        "output_snr_db": output_snr,
        "snr_improvement_db": output_snr-input_snr if np.isfinite(input_snr) else float("nan"),
        "correlation": r,
        "interior_rmse": float(np.sqrt(np.mean(error[boundary:-boundary]**2))),
        "boundary_rmse": float(np.sqrt(np.mean(np.r_[error[:boundary], error[-boundary:]]**2))),
        "spectral_power_relative_error": float(np.sum(np.abs(pz-px))/np.sum(px)) if np.sum(px)>0 else float("nan"),
    }
    if "pulses" in features:
        amplitude, timing, missing = [], [], []
        for peak in features["pulses"]:
            left, right, center = peak["left"], peak["right"], peak["center"]
            found = left + int(np.argmax(z[left:right]))
            amplitude.append(abs(z[found]-x[center]))
            timing.append(abs(found-center))
            missing.append(float(z[found] < 0.25*x[center]))
        result.update(pulse_amplitude_mae=float(np.mean(amplitude)), pulse_timing_mae_samples=float(np.mean(timing)), pulse_miss_rate=float(np.mean(missing)))
    if "steps" in features:
        jumps, overshoots = [], []
        width = max(8, len(x)//32)
        for edge in features["steps"]:
            a, b = slice(edge-width, edge-2), slice(edge+2, edge+width)
            true_jump = np.mean(x[b])-np.mean(x[a])
            recovered_jump = np.mean(z[b])-np.mean(z[a])
            jumps.append(abs(recovered_jump-true_jump))
            low, high = sorted((x[edge-1], x[edge]))
            region = z[edge-width:edge+width]
            overshoots.append(max(0, float(np.max(region)-high), float(low-np.min(region))))
        result.update(step_jump_mae=float(np.mean(jumps)), step_overshoot=float(np.mean(overshoots)))
    return result
