import torch
from torch import nn


class ResidualCNN(nn.Module):
    """Predict noise and subtract it. CPU-only use is enforced by the runner."""

    def __init__(self, channels=24, layers=5, kernel_size=7):
        super().__init__()
        modules = []
        for i in range(layers):
            inc = 1 if i == 0 else channels
            outc = 1 if i == layers-1 else channels
            modules.append(nn.Conv1d(inc, outc, kernel_size, padding=kernel_size//2, padding_mode="reflect"))
            if i < layers-1:
                modules.append(nn.ReLU())
        self.network = nn.Sequential(*modules)
        nn.init.zeros_(self.network[-1].weight)
        nn.init.zeros_(self.network[-1].bias)

    def forward(self, noisy):
        return noisy - self.network(noisy)


def predict(model, noisy, scale):
    import numpy as np
    x = np.asarray(noisy)
    singleton = x.ndim == 1
    batch = x[None, :] if singleton else x
    tensor = torch.as_tensor(batch/scale, dtype=torch.float32).unsqueeze(1)
    model.eval()
    with torch.inference_mode():
        result = model(tensor).squeeze(1).cpu().numpy().astype(np.float64)*scale
    return result[0] if singleton else result
