"""
Gravitational Magnification, Jacobian, Critical Curves, and Caustics
===================================================================

Calculates image magnification, Jacobian matrices, convergence (kappa),
shear (gamma), critical curves in the image plane, and caustics in the source plane.

Formulas:
    A = d(beta) / d(theta)
    det(A) = (1 - kappa)^2 - gamma^2
    mu = 1 / det(A)
"""

from typing import Tuple, Dict, Any, Union
import numpy as np


def point_mass_magnification_analytical(beta: float, theta_e: float) -> Dict[str, float]:
    """
    Calculate analytical point-mass magnifications for a source at offset beta.

    Parameters:
        beta: Source offset from lens center (same angular units as theta_e).
        theta_e: Einstein radius.

    Returns:
        Dict containing:
            u: dimensionless impact parameter beta / theta_e
            mu_plus: magnification of primary image (> 1)
            mu_minus: absolute magnification of secondary image (> 0)
            mu_tot: total magnification (|mu_+| + |mu_-|)
            mu_signed_minus: -mu_minus (negative parity)
    """
    if beta <= 0.0 or theta_e <= 0.0:
        return {
            "u": 0.0,
            "mu_plus": float("inf"),
            "mu_minus": float("inf"),
            "mu_tot": float("inf"),
            "mu_signed_minus": -float("inf")
        }

    u = beta / theta_e
    u_term = np.sqrt(u**2 + 4.0)
    base = (u**2 + 2.0) / (2.0 * u * u_term)
    mu_plus = base + 0.5
    mu_minus = base - 0.5
    mu_tot = (u**2 + 2.0) / (u * u_term)

    return {
        "u": float(u),
        "mu_plus": float(mu_plus),
        "mu_minus": float(mu_minus),
        "mu_tot": float(mu_tot),
        "mu_signed_minus": float(-mu_minus)
    }


def compute_jacobian_and_magnification_grid(beta_x_grid: np.ndarray,
                                            beta_y_grid: np.ndarray,
                                            theta_x_grid: np.ndarray,
                                            theta_y_grid: np.ndarray,
                                            clip_mu: float = 100.0) -> Dict[str, np.ndarray]:
    """
    Compute Jacobian components and magnification map via numerical finite differences.

    Parameters:
        beta_x_grid, beta_y_grid: 2D arrays of source coordinates mapped from theta.
        theta_x_grid, theta_y_grid: 2D meshgrid arrays of image coordinates.
        clip_mu: Maximum absolute magnification to clip for visual stability.

    Returns:
        Dict with keys:
            det_A: Jacobian determinant map
            magnification: Signed magnification map
            abs_magnification: Absolute magnification map (clipped)
            convergence: Kappa map
            shear: Gamma magnitude map
    """
    # Grid steps
    dx = float(theta_x_grid[0, 1] - theta_x_grid[0, 0])
    dy = float(theta_y_grid[1, 0] - theta_y_grid[0, 0])

    # Partial derivatives using np.gradient
    # axis 0 corresponds to y, axis 1 corresponds to x
    dbeta_x_dy, dbeta_x_dx = np.gradient(beta_x_grid, dy, dx)
    dbeta_y_dy, dbeta_y_dx = np.gradient(beta_y_grid, dy, dx)

    # Jacobian matrix components
    # A_xx = dbeta_x / dtheta_x
    # A_xy = dbeta_x / dtheta_y
    # A_yx = dbeta_y / dtheta_x
    # A_yy = dbeta_y / dtheta_y
    a_xx = dbeta_x_dx
    a_xy = dbeta_x_dy
    a_yx = dbeta_y_dx
    a_yy = dbeta_y_dy

    det_a = a_xx * a_yy - a_xy * a_yx

    # Convergence (kappa) and Shear (gamma)
    kappa = 1.0 - 0.5 * (a_xx + a_yy)
    gamma1 = 0.5 * (a_yy - a_xx)
    gamma2 = -0.5 * (a_xy + a_yx)
    gamma = np.sqrt(gamma1**2 + gamma2**2)

    # Regularize determinant near zero to avoid ZeroDivisionError
    safe_det = np.where(np.abs(det_a) < 1e-5, np.sign(det_a) * 1e-5 + 1e-5, det_a)
    magnification = 1.0 / safe_det

    abs_magnification = np.clip(np.abs(magnification), 0.0, clip_mu)

    return {
        "det_a": det_a,
        "magnification": magnification,
        "abs_magnification": abs_magnification,
        "convergence": kappa,
        "shear": gamma
    }


def find_critical_curves_and_caustics(theta_x_grid: np.ndarray,
                                      theta_y_grid: np.ndarray,
                                      beta_x_grid: np.ndarray,
                                      beta_y_grid: np.ndarray,
                                      det_a: np.ndarray) -> Dict[str, Any]:
    """
    Extract critical curve points where det(A) ~ 0, and map them to caustics.
    """
    # Use zero-crossing contour detection
    import matplotlib.pyplot as plt
    # Extract contour lines without displaying
    fig, ax = plt.subplots()
    cs = ax.contour(theta_x_grid, theta_y_grid, det_a, levels=[0.0])
    critical_segments = []
    caustic_segments = []

    # Map critical points through lens equation
    # To interpolate beta for contour paths:
    from scipy.interpolate import RegularGridInterpolator
    x_1d = theta_x_grid[0, :]
    y_1d = theta_y_grid[:, 0]

    interp_bx = RegularGridInterpolator((y_1d, x_1d), beta_x_grid, bounds_error=False, fill_value=None)
    interp_by = RegularGridInterpolator((y_1d, x_1d), beta_y_grid, bounds_error=False, fill_value=None)

    for path in cs.allsegs[0] if len(cs.allsegs) > 0 else []:
        if len(path) > 2:
            critical_segments.append(path)
            # Evaluate beta along contour
            pts_y = path[:, 1]
            pts_x = path[:, 0]
            pts = np.column_stack((pts_y, pts_x))
            bx_vals = interp_bx(pts)
            by_vals = interp_by(pts)
            caustic_segments.append(np.column_stack((bx_vals, by_vals)))

    plt.close(fig)
    return {
        "critical_curves": critical_segments,
        "caustics": caustic_segments
    }

