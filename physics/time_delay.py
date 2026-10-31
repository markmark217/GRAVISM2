"""
Gravitational Time Delay and Fermat Potential
=============================================

Calculates arrival time differences between multiple gravitationally lensed images.
Fermat Potential:
    tau(theta, beta) = 0.5 * |theta - beta|^2 - psi(theta)

Time Delay:
    t(theta) = (1 + z_L) / c * (D_L * D_S / D_LS) * tau(theta, beta)
             = (D_dt / c) * tau(theta, beta)
"""

from typing import Dict, Any, List
import numpy as np
from physics.constants import C, MPC, ARCSEC_TO_RAD


def fermat_potential_point_mass(theta_arcsec: float,
                                beta_arcsec: float,
                                theta_e_arcsec: float) -> float:
    """
    Dimensionless Fermat potential for a collinear point mass:
        tau = 0.5 * (theta - beta)^2 - theta_e^2 * ln(|theta| / theta_e)
    All angles in radians for dimensional consistency.
    """
    theta_rad = theta_arcsec * ARCSEC_TO_RAD
    beta_rad = beta_arcsec * ARCSEC_TO_RAD
    te_rad = theta_e_arcsec * ARCSEC_TO_RAD

    geom = 0.5 * (theta_rad - beta_rad)**2
    grav = (te_rad**2) * np.log(abs(theta_rad) / te_rad)
    return float(geom - grav)


def time_delay_days_between_images(theta_plus_arcsec: float,
                                   theta_minus_arcsec: float,
                                   beta_arcsec: float,
                                   theta_e_arcsec: float,
                                   time_delay_distance_mpc: float) -> Dict[str, float]:
    """
    Calculate arrival-time difference in days between primary (+) and secondary (-) images
    of a point-mass lens.

    Returns:
        Dict with delta_t_seconds, delta_t_days, and Fermat potential values.
    """
    tau_plus = fermat_potential_point_mass(theta_plus_arcsec, beta_arcsec, theta_e_arcsec)
    tau_minus = fermat_potential_point_mass(theta_minus_arcsec, beta_arcsec, theta_e_arcsec)

    delta_tau = tau_minus - tau_plus  # Secondary arrives later (or earlier depending on geometry)

    d_dt_meters = time_delay_distance_mpc * MPC
    delta_t_sec = (d_dt_meters / C) * abs(delta_tau)
    delta_t_days = delta_t_sec / 86400.0

    return {
        "delta_t_seconds": float(delta_t_sec),
        "delta_t_days": float(delta_t_days),
        "tau_plus": float(tau_plus),
        "tau_minus": float(tau_minus),
        "delta_tau": float(delta_tau)
    }

