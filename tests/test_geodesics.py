"""
Unit and Scientific Validation Tests for Schwarzschild Geodesics
================================================================
"""

import math
from relativity.schwarzschild import (
    schwarzschild_radius_m,
    photon_sphere_radius_m,
    critical_impact_parameter_m
)
from relativity.geodesics import integrate_null_geodesic
from physics.constants import M_SUN


def test_schwarzschild_radii_ratios():
    """Verify r_ph = 1.5 * r_s and b_crit = (3*sqrt(3)/2) * r_s."""
    mass = 10.0 * M_SUN
    r_s = schwarzschild_radius_m(mass)
    r_ph = photon_sphere_radius_m(mass)
    b_crit = critical_impact_parameter_m(mass)

    assert math.isclose(r_ph / r_s, 1.5, rel_tol=1e-12)
    expected_b_crit_ratio = 1.5 * math.sqrt(3.0)  # ~ 2.598076
    assert math.isclose(b_crit / r_s, expected_b_crit_ratio, rel_tol=1e-12)


def test_photon_capture_below_b_crit():
    """Verify photon with b < b_crit is captured by event horizon."""
    # b_crit ~ 2.598
    res_captured = integrate_null_geodesic(b_over_rs=2.2)
    assert res_captured["status"] == "captured"
    assert res_captured["r_min"] <= 1.05  # Reached near or inside event horizon


def test_photon_escape_above_b_crit():
    """Verify photon with b > b_crit escapes to infinity."""
    res_escaped = integrate_null_geodesic(b_over_rs=4.0)
    assert res_escaped["status"] == "escaped"
    assert res_escaped["deflection_rad"] is not None
    assert res_escaped["deflection_rad"] > 0.0

