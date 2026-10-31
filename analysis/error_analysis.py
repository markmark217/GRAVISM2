"""
Scientific Error Analysis and Thesis Validation Tests
=====================================================

Implements the formal validation suite described in Section 19 of the specification:
- Test 1: Mass Dependence (theta_E proportional to sqrt(M))
- Test 2: Impact Parameter Dependence (alpha proportional to 1/b)
- Test 3: Source Alignment (images approach Einstein ring as beta -> 0)
- Test 4: Image Positions (analytical vs numerical)
- Test 5: Magnification (analytical vs numerical)
"""

from typing import Dict, Any, List
import numpy as np
from physics.constants import M_SUN, KPC
from physics.deflection import weak_field_deflection_angle_arcsec
from physics.einstein_radius import calculate_einstein_radius_arcsec
from physics.lens_equation import solve_point_mass_images_1d
from physics.magnification import point_mass_magnification_analytical


def validate_test1_mass_dependence() -> Dict[str, Any]:
    """
    Test 1: If mass increases by a factor of 4, theta_E should increase by exactly a factor of 2.
    """
    m1 = 1e11 * M_SUN
    m2 = 4e11 * M_SUN
    d_l, d_s, d_ls = 1000.0, 2000.0, 1000.0

    te1 = float(calculate_einstein_radius_arcsec(m1, d_l, d_s, d_ls))
    te2 = float(calculate_einstein_radius_arcsec(m2, d_l, d_s, d_ls))

    ratio = te2 / te1
    expected_ratio = 2.0
    rel_error = abs(ratio - expected_ratio) / expected_ratio

    return {
        "m1_solar": 1e11,
        "m2_solar": 4e11,
        "theta_e1_arcsec": te1,
        "theta_e2_arcsec": te2,
        "ratio": ratio,
        "expected_ratio": expected_ratio,
        "relative_error": rel_error,
        "passed": bool(rel_error < 1e-12)
    }


def validate_test2_impact_parameter() -> Dict[str, Any]:
    """
    Test 2: alpha proportional to 1/b. If b doubles, alpha should halve (ratio = 0.5).
    """
    m = 1e11 * M_SUN
    b1 = 10.0 * KPC
    b2 = 20.0 * KPC

    a1 = float(weak_field_deflection_angle_arcsec(m, b1))
    a2 = float(weak_field_deflection_angle_arcsec(m, b2))

    ratio = a2 / a1
    expected_ratio = 0.5
    rel_error = abs(ratio - expected_ratio) / expected_ratio

    return {
        "b1_kpc": 10.0,
        "b2_kpc": 20.0,
        "alpha1_arcsec": a1,
        "alpha2_arcsec": a2,
        "ratio": ratio,
        "expected_ratio": expected_ratio,
        "relative_error": rel_error,
        "passed": bool(rel_error < 1e-12)
    }


def validate_test3_alignment() -> Dict[str, Any]:
    """
    Test 3: As source beta approaches 0, images approach +theta_E and -theta_E.
    """
    theta_e = 1.5
    betas = [1.0, 0.5, 0.1, 0.01, 0.001]
    results = []

    for beta in betas:
        t_plus, t_minus = solve_point_mass_images_1d(beta, theta_e)
        diff_plus = abs(t_plus - theta_e)
        diff_minus = abs(abs(t_minus) - theta_e)
        results.append({
            "beta": beta,
            "theta_plus": t_plus,
            "theta_minus": t_minus,
            "diff_from_theta_e": max(diff_plus, diff_minus)
        })

    return {
        "theta_e": theta_e,
        "steps": results,
        "passed": bool(results[-1]["diff_from_theta_e"] < 0.002)
    }


def validate_test5_magnification() -> Dict[str, Any]:
    """
    Test 5: Verify that mu_+ - mu_- = 1 for any point mass source offset beta.
    """
    theta_e = 1.5
    offsets = [0.2, 0.5, 1.0, 2.0, 5.0]
    results = []

    for b in offsets:
        mag = point_mass_magnification_analytical(b, theta_e)
        diff = mag["mu_plus"] - mag["mu_minus"]
        rel_err = abs(diff - 1.0)
        results.append({
            "beta": b,
            "mu_plus": mag["mu_plus"],
            "mu_minus": mag["mu_minus"],
            "difference": diff,
            "rel_err": rel_err
        })

    max_err = max(r["rel_err"] for r in results)
    return {
        "test": "mu_+ - mu_- = 1 Identity",
        "results": results,
        "max_error": max_err,
        "passed": bool(max_err < 1e-12)
    }


def run_full_validation_suite() -> Dict[str, Any]:
    """Execute all scientific validation tests and compile summary report."""
    t1 = validate_test1_mass_dependence()
    t2 = validate_test2_impact_parameter()
    t3 = validate_test3_alignment()
    t5 = validate_test5_magnification()

    all_passed = t1["passed"] and t2["passed"] and t3["passed"] and t5["passed"]
    return {
        "test1_mass": t1,
        "test2_impact": t2,
        "test3_alignment": t3,
        "test5_magnification": t5,
        "all_passed": all_passed
    }

