"""
Unit and Scientific Validation Tests for Einstein Radius
========================================================
"""

import pytest
import math
from physics.constants import M_SUN, MPC
from physics.einstein_radius import (
    calculate_einstein_radius_rad,
    calculate_einstein_radius_arcsec,
    sis_einstein_radius_arcsec
)


def test_mass_dependence_sqrt():
    """Verify theta_E is strictly proportional to sqrt(M)."""
    m1 = 1e11 * M_SUN
    m2 = 4e11 * M_SUN  # 4x mass

    te1 = calculate_einstein_radius_rad(m1, 1000.0 * MPC, 2000.0 * MPC, 1000.0 * MPC)
    te2 = calculate_einstein_radius_rad(m2, 1000.0 * MPC, 2000.0 * MPC, 1000.0 * MPC)

    ratio = te2 / te1
    assert math.isclose(ratio, 2.0, rel_tol=1e-10)


def test_einstein_radius_positive_distances():
    """Verify negative or zero distances raise ValueError."""
    with pytest.raises(ValueError):
        calculate_einstein_radius_rad(1e11 * M_SUN, -100.0, 2000.0, 1000.0)


def test_sis_einstein_radius_scaling():
    """Verify SIS Einstein radius scales as velocity_dispersion^2."""
    te1 = sis_einstein_radius_arcsec(200.0, 1000.0, 2000.0)
    te2 = sis_einstein_radius_arcsec(400.0, 1000.0, 2000.0)

    ratio = te2 / te1
    assert math.isclose(ratio, 4.0, rel_tol=1e-10)

