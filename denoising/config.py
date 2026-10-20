from dataclasses import asdict, dataclass, field
import json
from pathlib import Path


@dataclass
class Config:
    stage: str = "development_pilot"
    length: int = 1024
    train_count: int = 200
    validation_count: int = 40
    evaluation_count: int = 40
    dataset_seed: int = 20261018
    model_seed: int = 42
    training_noise: list[str] = field(default_factory=lambda: ["white"])
    training_snrs: list[float] = field(default_factory=lambda: [0, 5, 10])
    evaluation_noise: list[str] = field(default_factory=lambda: ["white", "colored", "impulsive"])
    evaluation_snrs: list[float] = field(default_factory=lambda: [-5, 0, 2.5, 5, 7.5, 10, 15])
    noise_repetitions: int = 1
    epochs: int = 5
    batch_size: int = 32
    channels: int = 24
    layers: int = 5
    kernel_size: int = 7
    learning_rate: float = 0.001
    patience: int = 5
    threads: int = 1
    runtime_limit_seconds: float = 300
    timing_warmup: int = 20
    timing_repeats: int = 100
    boundary_width: int = 32

    def validate(self):
        import math
        if self.stage != "development_pilot":
            raise ValueError("Only development_pilot is supported; main experiments are not enabled.")
        if self.length < 256 or self.length > 4096:
            raise ValueError("Pilot length must be between 256 and 4096.")
        for name in ("train_count", "validation_count", "evaluation_count"):
            n = getattr(self, name)
            if n < 4 or n % 4 or n > 2000:
                raise ValueError(f"{name} must be a positive multiple of four, at most 2000.")
        for name in ("epochs", "batch_size", "channels", "threads", "patience", "noise_repetitions", "timing_repeats"):
            if getattr(self, name) < 1:
                raise ValueError(f"{name} must be positive.")
        if not 2 <= self.layers <= 6 or not 4 <= self.channels <= 32:
            raise ValueError("Use 2–6 layers and 4–32 channels in the pilot.")
        if self.kernel_size < 3 or self.kernel_size % 2 != 1 or self.kernel_size > 9:
            raise ValueError("kernel_size must be odd, between 3 and 9.")
        if not 1 <= self.boundary_width < self.length // 2:
            raise ValueError("Invalid boundary_width.")
        if self.timing_warmup < 0 or self.dataset_seed < 0 or self.model_seed < 0:
            raise ValueError("Seeds and timing_warmup must be nonnegative.")
        for name in ("learning_rate", "runtime_limit_seconds"):
            if not math.isfinite(getattr(self, name)) or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be finite and positive.")
        for name in ("training_noise", "evaluation_noise"):
            values = getattr(self, name)
            if not values or len(set(values)) != len(values) or not set(values) <= {"white", "colored", "impulsive"}:
                raise ValueError(f"Invalid {name}.")
        for name in ("training_snrs", "evaluation_snrs"):
            values = getattr(self, name)
            if not values or len(set(values)) != len(values) or not all(math.isfinite(v) and -30 <= v <= 60 for v in values):
                raise ValueError(f"Invalid {name}.")
        return self

    def to_dict(self):
        return asdict(self)

    @classmethod
    def load(cls, path):
        return cls(**json.loads(Path(path).read_text())).validate()
