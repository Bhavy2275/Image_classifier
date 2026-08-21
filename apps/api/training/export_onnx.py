"""
Export a trained PyTorch model checkpoint to ONNX.

Usage:
    python training/export_onnx.py \
        --checkpoint checkpoints/best_model.pt \
        --output model_cache/efficientnet_b0.onnx \
        --num_classes 1000
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import torch
import timm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export PyTorch model to ONNX")
    p.add_argument("--checkpoint", default=None, help="Path to .pt checkpoint (state_dict)")
    p.add_argument("--model_name", default="efficientnet_b0", help="timm model name")
    p.add_argument("--num_classes", type=int, default=1000)
    p.add_argument("--image_size", type=int, default=224)
    p.add_argument("--output", default="model_cache/efficientnet_b0.onnx")
    return p.parse_args()


def export(args: argparse.Namespace) -> None:
    logger.info(f"Building model: {args.model_name} (num_classes={args.num_classes})")
    model = timm.create_model(
        args.model_name,
        pretrained=(args.checkpoint is None),
        num_classes=args.num_classes,
    )

    if args.checkpoint:
        logger.info(f"Loading checkpoint: {args.checkpoint}")
        state_dict = torch.load(args.checkpoint, map_location="cpu")
        model.load_state_dict(state_dict)

    model.eval()

    dummy_input = torch.randn(1, 3, args.image_size, args.image_size)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Exporting to ONNX: {output_path}")
    torch.onnx.export(
        model,
        dummy_input,
        str(output_path),
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "output": {0: "batch_size"},
        },
    )

    # Validate exported model
    import onnx
    onnx_model = onnx.load(str(output_path))
    onnx.checker.check_model(onnx_model)
    logger.info(f"✅ ONNX model validated and saved: {output_path}")


if __name__ == "__main__":
    export(parse_args())
