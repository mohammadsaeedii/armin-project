from pathlib import Path
import numpy as np
import torch

from .config import Config
from .model import ResidualCNN, predict


def infer_file(checkpoint_path, input_path, output_path, batch_size=32):
    """Inference on provided arrays only; this command never synthesizes noise."""
    output_path = Path(output_path)
    if output_path.exists():
        raise FileExistsError(output_path)
    if output_path.suffix != ".npy" or batch_size < 1:
        raise ValueError("Output must end in .npy and batch_size must be positive.")
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    cfg = Config(**checkpoint["config"]).validate()
    scale = float(checkpoint["scale"])
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError("Invalid training-fitted scale in checkpoint.")
    values = np.load(input_path, allow_pickle=False)
    if values.dtype.kind not in "fiu" or values.ndim not in (1, 2) or values.shape[-1] != cfg.length or not np.isfinite(values).all() or values.size == 0:
        raise ValueError(f"Expected finite numeric [N, {cfg.length}] or [{cfg.length}] input.")
    torch.set_num_threads(1)
    model = ResidualCNN(cfg.channels, cfg.layers, cfg.kernel_size)
    model.load_state_dict(checkpoint["state_dict"])
    batch = values[None, :] if values.ndim == 1 else values
    parts = [predict(model, batch[i:i+batch_size], scale) for i in range(0, len(batch), batch_size)]
    result = np.concatenate(parts)
    if values.ndim == 1:
        result = result[0]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("xb") as handle:
        np.save(handle, result, allow_pickle=False)
    print(f"Saved {result.shape} CPU denoising output to {output_path}")
