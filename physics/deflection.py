"""
Deflection Angle Calculations
=============================

Weak-field gravitational deflection of light by compact and extended masses.
Formula:
    alpha_hat = 4 * G * M / (c^2 * b)
"""

from typing import Union, Tuple
import numpy as np
from physics.constants import G, C_SQ, RAD_TO_ARCSEC, M_SUN


def weak_field_deflection_angle(mass_kg: Union[float, np.ndarray],
                                impact_parameter_m: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate the weak-field light deflection angle (in radians) for a point mass.

    Parameters:
        mass_kg: Mass of the deflector in kilograms.
        impact_parameter_m: Closest approach distance (impact parameter) in meters.

    Returns:
        Deflection angle in radians.
    """
    b = np.asarray(impact_parameter_m, dtype=np.float64)
    # Avoid division by zero: replace zero or negative with small epsilon
    safe_b = np.where(b <= 0.0, np.finfo(float).eps, b)
    alpha = (4.0 * G * mass_kg) / (C_SQ * safe_b)
    if isinstance(impact_parameter_m, (float, int)):
        return float(alpha)
    return alpha


def weak_field_deflection_angle_arcsec(mass_kg: Union[float, np.ndarray],
                                       impact_parameter_m: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate the weak-field deflection angle in arcseconds.
    """
    alpha_rad = weak_field_deflection_angle(mass_kg, impact_parameter_m)
    return alpha_rad * RAD_TO_ARCSEC


def deflection_vector_2d(mass_kg: float,
                         x_m: Union[float, np.ndarray],
                         y_m: Union[float, np.ndarray],
                         x_lens_m: float = 0.0,
                         y_lens_m: float = 0.0) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Calculate the 2D deflection vector components (alpha_x, alpha_y) in radians
    at impact coordinates (x_m, y_m) relative to a lens at (x_lens_m, y_lens_m).
    """
    dx = np.asarray(x_m, dtype=np.float64) - x_lens_m
    dy = np.asarray(y_m, dtype=np.float64) - y_lens_m
    r_sq = dx**2 + dy**2
    safe_r_sq = np.where(r_sq <= 0.0, np.finfo(float).eps, r_sq)
    factor = (4.0 * G * mass_kg) / (C_SQ * safe_r_sq)
    alpha_x = factor * dx
    alpha_y = factor * dy
    if isinstance(x_m, (float, int)) and isinstance(y_m, (float, int)):
        return float(alpha_x), float(alpha_y)
    return alpha_x, alpha_y


def solar_limb_deflection_arcsec() -> float:
    """
    Reference calculation: Deflection of starlight grazing the Sun's limb.
    M_sun ~ 1.9885e30 kg, R_sun ~ 6.9634e8 m.
    Einstein's 1915 prediction: ~1.751 arcseconds (verified by Eddington in 1919).
    """
    r_sun = 6.9634e8
    return float(weak_field_deflection_angle_arcsec(M_SUN, r_sun))

