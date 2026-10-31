"""
Unit and Scientific Validation Tests for Lens Equation
======================================================
"""

import math
from physics.lens_equation import solve_point_mass_images_1d, solve_point_mass_images_2d


def test_collinear_images_lens_equation():
    """Verify that theta_+ and theta_- satisfy the lens equation: beta = theta - theta_E^2 / theta."""
    theta_e = 2.0
    beta = 1.5

    theta_plus, theta_minus = solve_point_mass_images_1d(beta, theta_e)

    # Check primary image
    beta_calc_plus = theta_plus - (theta_e**2) / theta_plus
    assert math.isclose(beta_calc_plus, beta, rel_tol=1e-10)

    # Check secondary image
    beta_calc_minus = theta_minus - (theta_e**2) / theta_minus
    assert math.isclose(beta_calc_minus, beta, rel_tol=1e-10)


def test_einstein_ring_at_zero_beta():
    """Verify that when beta = 0, an Einstein ring solution is returned."""
    theta_e = 1.8
    solutions = solve_point_mass_images_2d(0.0, 0.0, theta_e)
    assert len(solutions) == 1
    assert solutions[0]["is_ring"] is True
    assert math.isclose(solutions[0]["radius"], theta_e, rel_tol=1e-10)


def test_image_separation():
    """Verify image separation: theta_+ - theta_- = sqrt(beta^2 + 4 theta_E^2)."""
    theta_e = 1.5
    beta = 0.8
    t_plus, t_minus = solve_point_mass_images_1d(beta, theta_e)
    sep = t_plus - t_minus
    expected_sep = math.sqrt(beta**2 + 4.0 * theta_e**2)
    assert math.isclose(sep, expected_sep, rel_tol=1e-10)

