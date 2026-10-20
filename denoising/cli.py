import argparse
import json
import os
from pathlib import Path

from .config import Config


def main():
    parser = argparse.ArgumentParser(description="CPU development pilot; no final experiment is enabled.")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("pilot", help="Run bounded training, tuning and development evaluation")
    run.add_argument("--config", type=Path, default=Path("configs/pilot.json"))
    run.add_argument("--output", type=Path, required=True, help="New directory; existing paths are refused")
    inspect = commands.add_parser("validate-config", help="Check configuration without generating data or training")
    inspect.add_argument("--config", type=Path, default=Path("configs/pilot.json"))
    infer = commands.add_parser("infer", help="Apply a pilot CNN checkpoint to a numeric .npy array")
    infer.add_argument("--checkpoint", type=Path, required=True)
    infer.add_argument("--input", type=Path, required=True)
    infer.add_argument("--output", type=Path, required=True)
    infer.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()
    if args.command == "infer":
        for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
            os.environ[name] = "1"
        from .inference import infer_file
        infer_file(args.checkpoint, args.input, args.output, args.batch_size)
        return
    cfg = Config.load(args.config)
    if args.command == "validate-config":
        print(json.dumps(cfg.to_dict(), indent=2))
        return
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[name] = str(cfg.threads)
    # Import numerical libraries only after configuring native thread pools.
    from .runner import run_pilot
    run_pilot(cfg, args.output)


if __name__ == "__main__":
    main()
