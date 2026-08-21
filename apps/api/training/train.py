"""
Transfer learning training script for EfficientNetV2-S.

Usage:
    python training/train.py --data_dir /path/to/dataset --config training/configs/effnetv2_s.yaml

Dataset expected in ImageFolder format:
    data_dir/
        class_a/
            img1.jpg
        class_b/
            img1.jpg
"""
from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

import torch
import torch.nn as nn
import yaml
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train EfficientNetV2-S with transfer learning")
    p.add_argument("--data_dir", required=True, help="Root of ImageFolder dataset")
    p.add_argument("--config", default="training/configs/effnetv2_s.yaml")
    p.add_argument("--output_dir", default="checkpoints")
    return p.parse_args()


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def build_model(num_classes: int, freeze_backbone: bool = True) -> nn.Module:
    import timm

    model = timm.create_model("efficientnetv2_s", pretrained=True, num_classes=num_classes)

    if freeze_backbone:
        # Freeze all parameters except the classifier head
        for name, param in model.named_parameters():
            if "classifier" not in name:
                param.requires_grad = False
        logger.info("Backbone frozen — training classifier head only.")

    return model


def unfreeze_last_n_blocks(model: nn.Module, n: int = 2) -> None:
    """Unfreeze the last N blocks of the EfficientNetV2-S backbone for fine-tuning."""
    try:
        blocks = list(model.blocks)
        for block in blocks[-n:]:
            for param in block.parameters():
                param.requires_grad = True
        logger.info(f"Unfrozen last {n} backbone blocks for fine-tuning.")
    except AttributeError:
        logger.warning("Could not unfreeze last N blocks — model structure differs.")


def train(args: argparse.Namespace) -> None:
    from training.dataset import build_dataloaders

    cfg = load_config(args.config)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Device: {device}")

    train_loader, val_loader, num_classes = build_dataloaders(
        data_dir=args.data_dir,
        image_size=cfg["image_size"],
        batch_size=cfg["batch_size"],
    )

    model = build_model(num_classes=num_classes, freeze_backbone=True)
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=cfg["lr"],
        weight_decay=cfg.get("weight_decay", 1e-4),
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=cfg["epochs"])

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    best_val_acc = 0.0

    for epoch in range(1, cfg["epochs"] + 1):
        # ── Fine-tune: unfreeze backbone partway through ──
        if epoch == cfg.get("unfreeze_epoch", cfg["epochs"] // 2):
            unfreeze_last_n_blocks(model, n=cfg.get("unfreeze_last_n", 2))
            # Re-create optimizer with all trainable params
            optimizer = AdamW(
                filter(lambda p: p.requires_grad, model.parameters()),
                lr=cfg["lr"] / 10,
                weight_decay=cfg.get("weight_decay", 1e-4),
            )

        # ── Train ───────────────────────────────────────────
        model.train()
        train_loss, correct, total = 0.0, 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
            total += images.size(0)

        scheduler.step()
        train_acc = correct / total

        # ── Validate ─────────────────────────────────────────
        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                val_correct += (outputs.argmax(1) == labels).sum().item()
                val_total += images.size(0)
        val_acc = val_correct / val_total

        logger.info(
            f"Epoch {epoch}/{cfg['epochs']} | "
            f"Train Loss: {train_loss/total:.4f} | "
            f"Train Acc: {train_acc:.4f} | "
            f"Val Acc: {val_acc:.4f}"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            ckpt_path = output_dir / "best_model.pt"
            torch.save(model.state_dict(), ckpt_path)
            logger.info(f"✅ Best model saved: {ckpt_path} (val_acc={val_acc:.4f})")

    logger.info(f"Training complete. Best val accuracy: {best_val_acc:.4f}")


if __name__ == "__main__":
    train(parse_args())
