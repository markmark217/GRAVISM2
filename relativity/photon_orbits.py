"""
Relativistic Photon Orbits and Deflection Comparison
===================================================

Compares exact general relativistic deflection with the weak-field approximation:
- Weak field: alpha_weak = 2 * r_s / b = 4 * G * M / (c^2 * b)
- Strong field (Bozza / Darwin): Logarithmic divergence near b_crit = (3*sqrt(3)/2) * r_s
"""

import math
from typing import Dict, Any, List, Tuple
import numpy as np
from relativity.schwarzschild import critical_impact_parameter_m, schwarzschild_radius_m
from relativity.geodesics import integrate_null_geodesic


def deflection_comparison_data(b_values: List[float]) -> Dict[str, Any]:
    """
    Compare numerical GR deflection with weak-field deflection:
        b_values: List of impact parameters in units of r_s (e.g. from 2.65 to 25.0)

    Returns:
        Dict with 'b', 'gr_deflection_rad', 'weak_deflection_rad', 'relative_diff_pct'
    """
    b_arr = []
    gr_arr = []
    weak_arr = []
    diff_arr = []

    for b in b_values:
        res = integrate_null_geodesic(b)
        if res["status"] == "escaped" and res["deflection_rad"] is not None:
            gr_def = res["deflection_rad"]
            weak_def = 2.0 / b  # 4GM / (c^2 b) = 2 r_s / b
            pct_diff = abs(gr_def - weak_def) / gr_def * 100.0

            b_arr.append(b)
            gr_arr.append(gr_def)
            weak_arr.append(weak_def)
            diff_arr.append(pct_diff)

    return {
        "b_over_rs": np.array(b_arr),
        "gr_deflection_rad": np.array(gr_arr),
        "weak_deflection_rad": np.array(weak_arr),
        "difference_pct": np.array(diff_arr)
    }

