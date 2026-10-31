"""
Einstein Radius Calculations
============================

Formulas and utilities for computing the angular and physical Einstein radius
for point-mass and singular isothermal sphere lenses.

Angular Einstein Radius:
    theta_E = sqrt((4 * G * M / c^2) * (D_LS / (D_L * D_S)))

Physical Einstein Radius in Lens Plane:
    R_E = D_L * theta_E
"""

import math
from typing import Union
import numpy as np
from physics.constants import G, C_SQ, RAD_TO_ARCSEC, MPC


def calculate_einstein_radius_rad(mass_kg: Union[float, np.ndarray],
                                  d_l_m: float,
                                  d_s_m: float,
                                  d_ls_m: float) -> Union[float, np.ndarray]:
    """
    Calculate angular Einstein radius theta_E in radians.

    Parameters:
        mass_kg: Deflector mass in kilograms.
        d_l_m: Observer-to-lens angular diameter distance in meters.
        d_s_m: Observer-to-source angular diameter distance in meters.
        d_ls_m: Lens-to-source angular diameter distance in meters.

    Returns:
        theta_E in radians.
    """
    if d_l_m <= 0.0 or d_s_m <= 0.0 or d_ls_m <= 0.0:
        raise ValueError("Distances must be strictly positive.")
    if d_s_m < d_l_m and abs(d_s_m - d_l_m) > 1e-6:
        # Physical consistency warning/note: source should generally be behind lens
        pass

    geometric_factor = d_ls_m / (d_l_m * d_s_m)
    m = np.asarray(mass_kg, dtype=np.float64)
    # 4 G M / c^2
    schwarzschild_like = (4.0 * G * m) / C_SQ
    theta_e_sq = np.maximum(0.0, schwarzschild_like * geometric_factor)
    theta_e = np.sqrt(theta_e_sq)

    if isinstance(mass_kg, (float, int)):
        return float(theta_e)
    return theta_e


def calculate_einstein_radius_arcsec(mass_kg: Union[float, np.ndarray],
                                     d_l_mpc: float,
                                     d_s_mpc: float,
                                     d_ls_mpc: float) -> Union[float, np.ndarray]:
    """
    Convenience function taking distances in Megaparsecs (Mpc) and returning
    the Einstein radius in arcseconds.
    """
    d_l_m = d_l_mpc * MPC
    d_s_m = d_s_mpc * MPC
    d_ls_m = d_ls_mpc * MPC
    theta_rad = calculate_einstein_radius_rad(mass_kg, d_l_m, d_s_m, d_ls_m)
    return theta_rad * RAD_TO_ARCSEC


def physical_einstein_radius_m(mass_kg: float,
                               d_l_m: float,
                               d_s_m: float,
                               d_ls_m: float) -> float:
    """
    Physical radius R_E = D_L * theta_E in the lens plane in meters.
    """
    theta_rad = calculate_einstein_radius_rad(mass_kg, d_l_m, d_s_m, d_ls_m)
    return float(d_l_m * theta_rad)


def sis_einstein_radius_rad(velocity_dispersion_kms: float,
                            d_ls_m: float,
                            d_s_m: float) -> float:
    """
    Singular Isothermal Sphere (SIS) angular Einstein radius in radians:
        theta_E = 4 * pi * (sigma_v / c)^2 * (D_LS / D_S)
    """
    sigma_v_ms = velocity_dispersion_kms * 1000.0
    from physics.constants import C
    theta_e = 4.0 * math.pi * (sigma_v_ms / C)**2 * (d_ls_m / d_s_m)
    return float(theta_e)


def sis_einstein_radius_arcsec(velocity_dispersion_kms: float,
                               d_ls_mpc: float,
                               d_s_mpc: float) -> float:
    """
    SIS angular Einstein radius in arcseconds.
    """
    theta_rad = sis_einstein_radius_rad(velocity_dispersion_kms, d_ls_mpc * MPC, d_s_mpc * MPC)
    return float(theta_rad * RAD_TO_ARCSEC)

