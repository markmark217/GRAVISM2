"""
Black Hole Shadow and Visual Ray Tracing
=======================================

Generates 2D intensity maps for black hole shadow, photon sphere, and gravitationally
lensed background or accretion ring.
"""

import math
from typing import Tuple
import numpy as np


def generate_black_hole_image(grid_size: int = 150,
                              fov_rs: float = 12.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate synthetic black-hole shadow image in Schwarzschild spacetime.

    Parameters:
        grid_size: Number of pixels per axis (N x N)
        fov_rs: Total field of view in units of Schwarzschild radius r_s

    Returns:
        (x_grid, y_grid, image_rgb)
    """
    x = np.linspace(-fov_rs / 2.0, fov_rs / 2.0, grid_size)
    y = np.linspace(-fov_rs / 2.0, fov_rs / 2.0, grid_size)
    xx, yy = np.meshgrid(x, y)
    b = np.hypot(xx, yy)  # impact parameter in units of r_s

    # Critical impact parameter for Schwarzschild: b_crit = 3*sqrt(3)/2 ~ 2.598076
    b_crit = 1.5 * math.sqrt(3.0)

    # Initialize RGB canvas: Dark navy space
    img = np.zeros((grid_size, grid_size, 3), dtype=np.float32)
    # Background space glow
    img[:, :, 0] = 0.05
    img[:, :, 1] = 0.07
    img[:, :, 2] = 0.15

    # Event horizon shadow: b <= b_crit
    shadow_mask = b <= b_crit
    img[shadow_mask] = [0.0, 0.0, 0.0]

    # Photon Ring: sharp bright peak near b_crit
    ring_mask = (b > b_crit) & (b < b_crit * 1.15)
    ring_intensity = np.exp(-((b[ring_mask] - b_crit) / 0.12)**2)
    for c, factor in enumerate([0.9, 0.7, 0.4]):  # Gold / orange glow
        img[ring_mask, c] += ring_intensity * factor

    # Lensed Accretion Disk / background grid
    # Inner disk from r_isco = 3.0 to r = 6.0
    disk_mask = (b >= b_crit * 1.15) & (b <= 5.5)
    # Disk Doppler/brightness profile
    disk_rad = b[disk_mask]
    disk_brightness = (5.5 - disk_rad) / (5.5 - b_crit * 1.15)
    img[disk_mask, 0] += disk_brightness * 0.7
    img[disk_mask, 1] += disk_brightness * 0.4
    img[disk_mask, 2] += disk_brightness * 0.2

    # Add deflected background stars / grid pattern
    grid_lines = (np.sin(xx * 2.0) > 0.95) | (np.sin(yy * 2.0) > 0.95)
    outside_mask = b > b_crit
    img[grid_lines & outside_mask] += 0.25

    return xx, yy, np.clip(img, 0.0, 1.0)

