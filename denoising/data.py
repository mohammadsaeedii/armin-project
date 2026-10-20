"""Stateless development signals. No final-test namespace is implemented."""
from dataclasses import dataclass
import numpy as np
from scipy.signal import chirp

FAMILIES = ("sinusoids", "chirp", "pulses", "steps")
SPLITS = {"train": 11, "validation": 22, "development_evaluation": 33}


@dataclass
class Signal:
    identity: str
    family: str
    clean: np.ndarray
    features: dict


def make_signal(seed: int, split: str, index: int, length: int) -> Signal:
    rng = np.random.default_rng(np.random.SeedSequence([seed, SPLITS[split], index]))
    family = FAMILIES[index % len(FAMILIES)]
    t = np.arange(length) / length
    features = {}
    if family == "sinusoids":
        frequencies = rng.uniform(3, min(50, length / 8), size=3)
        amplitudes = rng.uniform(0.2, 1, size=3)
        phases = rng.uniform(0, 2 * np.pi, size=3)
        x = np.sum(amplitudes[:, None] * np.sin(2 * np.pi * frequencies[:, None] * t + phases[:, None]), axis=0)
    elif family == "chirp":
        f0, f1 = rng.uniform(2, 8), rng.uniform(20, min(60, length / 4))
        x = chirp(t, f0=f0, f1=f1, t1=1, phi=rng.uniform(0, 360))
        x *= 0.7 + 0.3 * np.sin(np.pi * t) ** 2
    elif family == "pulses":
        x = np.zeros(length)
        peaks = []
        grid = np.arange(length)
        for position in (0.2, 0.5, 0.8):
            center = int((position + rng.uniform(-0.03, 0.03)) * length)
            width = rng.uniform(0.008, 0.025) * length
            amplitude = rng.uniform(0.35, 1.3)
            x += amplitude * np.exp(-0.5 * ((grid - center) / width) ** 2)
            radius = int(np.ceil(3 * width))
            peaks.append({"center": center, "left": center-radius, "right": center+radius+1})
        features["pulses"] = peaks
    else:
        edges = [int((p + rng.uniform(-0.03, 0.03)) * length) for p in (0.25, 0.5, 0.75)]
        levels = [rng.uniform(-0.8, 0.8)]
        for _ in edges:
            levels.append(levels[-1] + rng.choice([-1, 1]) * rng.uniform(0.5, 1.2))
        x = np.empty(length)
        for left, right, level in zip([0]+edges, edges+[length], levels):
            x[left:right] = level
        features["steps"] = edges
    x *= rng.uniform(0.5, 1.5)
    return Signal(f"dev:{seed}:{split}:{index}", family, x.astype(np.float64), features)


def make_partition(seed, split, count, length):
    return [make_signal(seed, split, index, length) for index in range(count)]
