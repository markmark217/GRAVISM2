"""
Scientific Numerical Methods and Laboratory Calculators
======================================================

Implements dedicated laboratory calculators for:
- Weak-field deflection angle
- Einstein radius
- Point-mass lens equation
- Image magnification
- Time delays
"""

from typing import Dict, Any, List
import numpy as np
from physics.constants import G, C, C_SQ, M_SUN, MPC, KPC, RAD_TO_ARCSEC
from physics.deflection import weak_field_deflection_angle_arcsec
from physics.einstein_radius import calculate_einstein_radius_arcsec, calculate_einstein_radius_rad
from physics.lens_equation import solve_point_mass_images_2d
from physics.magnification import point_mass_magnification_analytical


def run_deflection_lab(mass_solar: float, impact_kpc: float) -> Dict[str, Any]:
    """
    Calculate deflection angle for given mass and impact parameter.
    """
    mass_kg = mass_solar * M_SUN
    impact_m = impact_kpc * KPC
    alpha_arcsec = float(weak_field_deflection_angle_arcsec(mass_kg, impact_m))
    alpha_rad = alpha_arcsec / RAD_TO_ARCSEC

    return {
        "mass_solar": mass_solar,
        "impact_kpc": impact_kpc,
        "deflection_arcsec": alpha_arcsec,
        "deflection_rad": alpha_rad,
        "deflection_microarcsec": alpha_arcsec * 1e6
    }


def run_einstein_radius_lab(mass_solar: float, d_l_mpc: float, d_s_mpc: float,
                            d_ls_mpc: float) -> Dict[str, Any]:
    """
    Calculate angular and physical Einstein radius.
    """
    mass_kg = mass_solar * M_SUN
    theta_e_arcsec = float(calculate_einstein_radius_arcsec(mass_kg, d_l_mpc, d_s_mpc, d_ls_mpc))
    theta_e_rad = theta_e_arcsec / RAD_TO_ARCSEC
    r_e_kpc = (d_l_mpc * 1000.0) * theta_e_rad  # D_L * theta_E in kpc

    return {
        "mass_solar": mass_solar,
        "d_l_mpc": d_l_mpc,
        "d_s_mpc": d_s_mpc,
        "d_ls_mpc": d_ls_mpc,
        "theta_e_arcsec": theta_e_arcsec,
        "theta_e_rad": theta_e_rad,
        "physical_radius_kpc": r_e_kpc
    }

