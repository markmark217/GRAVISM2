"""
Lens Equation and Image Solutions
=================================

Calculates image positions, ray mappings, and deflection solutions.
Lens equation:
    beta = theta - alpha(theta)
For point mass:
    beta = theta - theta_E^2 * (theta - theta_L) / |theta - theta_L|^2
"""

from typing import List, Tuple, Dict, Any, Union
import numpy as np


def solve_point_mass_images_1d(beta: float, theta_e: float) -> Tuple[float, float]:
    """
    Solve for collinear image positions for a 1D source distance beta >= 0.
        theta_+ = (beta + sqrt(beta^2 + 4 * theta_E^2)) / 2  (> 0)
        theta_- = (beta - sqrt(beta^2 + 4 * theta_E^2)) / 2  (< 0)

    Returns:
        (theta_plus, theta_minus)
    """
    disc = np.sqrt(beta**2 + 4.0 * theta_e**2)
    theta_plus = 0.5 * (beta + disc)
    theta_minus = 0.5 * (beta - disc)
    return float(theta_plus), float(theta_minus)


def solve_point_mass_images_2d(beta_x: float,
                               beta_y: float,
                               theta_e: float,
                               lens_x: float = 0.0,
                               lens_y: float = 0.0) -> List[Dict[str, Any]]:
    """
    Solve for 2D image coordinates and properties for a point-mass lens.

    Returns:
        List of dicts: [
            {"x": ..., "y": ..., "parity": +1/-1, "is_ring": False}, ...
        ]
        If beta == 0, returns a representative Einstein ring indicator.
    """
    # Offset relative to lens
    dx = beta_x - lens_x
    dy = beta_y - lens_y
    beta_dist = np.hypot(dx, dy)

    if beta_dist < 1e-12:
        # Perfect alignment -> Einstein Ring!
        return [{
            "x": lens_x,
            "y": lens_y,
            "radius": theta_e,
            "is_ring": True,
            "parity": 0,
            "magnification": float("inf"),
            "description": "Continuous Einstein Ring"
        }]

    # Unit vector pointing from lens to source
    ux = dx / beta_dist
    uy = dy / beta_dist

    theta_plus, theta_minus = solve_point_mass_images_1d(beta_dist, theta_e)

    # Positive parity image: along +u (outside Einstein ring)
    im1_x = lens_x + theta_plus * ux
    im1_y = lens_y + theta_plus * uy

    # Negative parity image: along -u (inside Einstein ring, theta_minus is negative)
    im2_x = lens_x + theta_minus * ux
    im2_y = lens_y + theta_minus * uy

    # Parity and magnification formulas:
    # u_norm = beta / theta_e
    u = beta_dist / theta_e
    u_term = np.sqrt(u**2 + 4.0)
    mu_plus = (u**2 + 2.0) / (2.0 * u * u_term) + 0.5
    mu_minus = (u**2 + 2.0) / (2.0 * u * u_term) - 0.5  # magnitude, signed is -mu_minus

    return [
        {
            "x": float(im1_x),
            "y": float(im1_y),
            "distance_from_lens": float(theta_plus),
            "parity": +1,
            "magnification": float(mu_plus),
            "signed_magnification": float(mu_plus),
            "is_ring": False,
            "type": "Primary (positive parity)"
        },
        {
            "x": float(im2_x),
            "y": float(im2_y),
            "distance_from_lens": float(abs(theta_minus)),
            "parity": -1,
            "magnification": float(mu_minus),
            "signed_magnification": float(-mu_minus),
            "is_ring": False,
            "type": "Secondary (negative parity)"
        }
    ]


def ray_trace_point_mass(theta_x_grid: np.ndarray,
                         theta_y_grid: np.ndarray,
                         theta_e: float,
                         lens_x: float = 0.0,
                         lens_y: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Inverse ray tracing mapping: for every image-plane coordinate (theta_x, theta_y),
    compute corresponding source-plane coordinate (beta_x, beta_y).
    """
    dx = theta_x_grid - lens_x
    dy = theta_y_grid - lens_y
    r_sq = dx**2 + dy**2
    # Regularize near center to avoid NaN
    safe_r_sq = np.where(r_sq < 1e-14, 1e-14, r_sq)
    factor = (theta_e**2) / safe_r_sq

    beta_x_grid = theta_x_grid - factor * dx
    beta_y_grid = theta_y_grid - factor * dy
    return beta_x_grid, beta_y_grid


def sis_lens_mapping(theta_x_grid: np.ndarray,
                     theta_y_grid: np.ndarray,
                     theta_e: float,
                     lens_x: float = 0.0,
                     lens_y: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Singular Isothermal Sphere (SIS) ray trace:
        beta = theta - theta_E * theta / |theta|
    """
    dx = theta_x_grid - lens_x
    dy = theta_y_grid - lens_y
    r = np.hypot(dx, dy)
    safe_r = np.where(r < 1e-14, 1e-14, r)
    factor = theta_e / safe_r

    beta_x_grid = theta_x_grid - factor * dx
    beta_y_grid = theta_y_grid - factor * dy
    return beta_x_grid, beta_y_grid

