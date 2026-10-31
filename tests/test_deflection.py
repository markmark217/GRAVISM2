"""
Unit and Scientific Validation Tests for Deflection Angle
=========================================================
"""

import pytest
import math
from physics.constants import G, C_SQ, M_SUN, KPC
from physics.deflection import (
    weak_field_deflection_angle,
    weak_field_deflection_angle_arcsec,
    deflection_vector_2d,
    solar_limb_deflection_arcsec
)


def test_solar_limb_deflection():
    """Verify Einstein 1915 solar limb deflection prediction ~ 1.751 arcsec."""
    alpha_arcsec = solar_limb_deflection_arcsec()
    assert 1.74 < alpha_arcsec < 1.76, f"Expected ~1.751 arcsec, got {alpha_arcsec}"


def test_deflection_inverse_b():
    """Verify alpha is strictly inversely proportional to impact parameter b."""
    mass = 1e11 * M_SUN
    b1 = 10.0 * KPC
    b2 = 20.0 * KPC

    a1 = weak_field_deflection_angle(mass, b1)
    a2 = weak_field_deflection_angle(mass, b2)

    ratio = a1 / a2
    assert math.isclose(ratio, 2.0, rel_tol=1e-10)


def test_deflection_vector_direction():
    """Verify deflection vector points radially outwards from lens to impact point."""
    mass = 1e11 * M_SUN
    ax, ay = deflection_vector_2d(mass, x_m=1e20, y_m=0.0, x_lens_m=0.0, y_lens_m=0.0)
    assert ax > 0.0
    assert ay == 0.0

    ax_neg, ay_neg = deflection_vector_2d(mass, x_m=-1e20, y_m=0.0, x_lens_m=0.0, y_lens_m=0.0)
    assert ax_neg < 0.0
    assert ay_neg == 0.0

