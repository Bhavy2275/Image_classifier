"""
Dataset loader for transfer learning training.
Wraps torchvision.datasets.ImageFolder with augmentation pipelines.
"""
from __future__ import annotations

import os
from typing import Tuple

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


def build_dataloaders(
    data_dir: str,
    image_size: int = 300,
    batch_size: int = 32,
    val_split: float = 0.2,
    num_workers: int = 4,
) -> Tuple[DataLoader, DataLoader, int]:
    """
    Build train and validation DataLoaders from an ImageFolder-structured directory.

    Returns:
        (train_loader, val_loader, num_classes)
    """
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(image_size, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    val_transform = transforms.Compose([
        transforms.Resize(int(image_size * 1.14)),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    full_dataset = datasets.ImageFolder(root=data_dir)
    num_classes = len(full_dataset.classes)

    # Train/val split by index
    total = len(full_dataset)
    val_size = int(total * val_split)
    train_size = total - val_size
    train_ds, val_ds = torch.utils.data.random_split(
        full_dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(42),
    )

    # Apply transforms separately
    train_ds.dataset.transform = train_transform
    val_ds.dataset.transform = val_transform

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    return train_loader, val_loader, num_classes
