"""
Unit and Scientific Validation Tests for Magnification
======================================================
"""

import math
from physics.magnification import point_mass_magnification_analytical


def test_magnification_identity():
    """Verify the fundamental point-mass relation: mu_+ - mu_- = 1 for all beta > 0."""
    theta_e = 1.5
    for beta in [0.1, 0.5, 1.0, 2.5, 5.0]:
        mag = point_mass_magnification_analytical(beta, theta_e)
        diff = mag["mu_plus"] - mag["mu_minus"]
        assert math.isclose(diff, 1.0, rel_tol=1e-10)


def test_large_beta_magnification_asymptote():
    """As beta -> infinity, mu_+ -> 1, mu_- -> 0, mu_tot -> 1."""
    theta_e = 1.0
    beta = 100.0  # u = 100 >> 1
    mag = point_mass_magnification_analytical(beta, theta_e)
    assert math.isclose(mag["mu_plus"], 1.0, abs_tol=1e-3)
    assert math.isclose(mag["mu_minus"], 0.0, abs_tol=1e-3)
    assert math.isclose(mag["mu_tot"], 1.0, abs_tol=1e-3)


def test_small_beta_magnification_divergence():
    """As beta -> 0, magnification diverges as ~ 1/u."""
    theta_e = 1.0
    mag_small = point_mass_magnification_analytical(0.01, theta_e)
    assert mag_small["mu_tot"] > 50.0

