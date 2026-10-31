"""
Schwarzschild Spacetime Metrics and Radii
========================================

General relativistic parameters for non-rotating (Schwarzschild) black holes:
- Schwarzschild radius: r_s = 2 * G * M / c^2
- Photon sphere radius: r_ph = 3 * G * M / c^2 = 1.5 * r_s
- Critical impact parameter: b_crit = (3 * sqrt(3) / 2) * r_s ~ 2.598 * r_s
- Innermost Stable Circular Orbit (ISCO for massive particles): r_isco = 3 * r_s = 6 * G * M / c^2
"""

import math
from typing import Dict, Any
from physics.constants import G, C_SQ, M_SUN


def schwarzschild_radius_m(mass_kg: float) -> float:
    """
    Event horizon radius for a non-rotating black hole:
        r_s = 2 * G * M / c^2
    """
    return (2.0 * G * mass_kg) / C_SQ


def photon_sphere_radius_m(mass_kg: float) -> float:
    """
    Photon sphere radius:
        r_ph = 1.5 * r_s = 3 * G * M / c^2
    """
    return 1.5 * schwarzschild_radius_m(mass_kg)


def critical_impact_parameter_m(mass_kg: float) -> float:
    """
    Critical impact parameter separating photon capture from escape:
        b_crit = (3 * sqrt(3) / 2) * r_s ~ 2.598076 * r_s
    """
    r_s = schwarzschild_radius_m(mass_kg)
    return 0.5 * 3.0 * math.sqrt(3.0) * r_s


def isco_radius_m(mass_kg: float) -> float:
    """
    Innermost stable circular orbit (ISCO) for massive matter:
        r_isco = 3 * r_s
    """
    return 3.0 * schwarzschild_radius_m(mass_kg)


def black_hole_summary(mass_solar: float) -> Dict[str, Any]:
    """
    Compute full summary of black hole characteristics for a given mass in solar masses.
    """
    mass_kg = mass_solar * M_SUN
    r_s = schwarzschild_radius_m(mass_kg)
    r_ph = photon_sphere_radius_m(mass_kg)
    b_crit = critical_impact_parameter_m(mass_kg)
    r_isco = isco_radius_m(mass_kg)

    return {
        "mass_solar": mass_solar,
        "mass_kg": mass_kg,
        "schwarzschild_radius_km": r_s / 1000.0,
        "photon_sphere_radius_km": r_ph / 1000.0,
        "critical_impact_parameter_km": b_crit / 1000.0,
        "isco_radius_km": r_isco / 1000.0,
        "shadow_angular_diameter_factor": 2.0 * b_crit / r_s  # ~ 5.196 r_s apparent diameter
    }

