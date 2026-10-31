"""
Numerical Grid Resolution and Convergence Tests
===============================================

Evaluates simulation stability and convergence as a function of grid resolution (N x N).
Conforms to Thesis Test 6 specification.
"""

from typing import List, Dict, Any
import time
import numpy as np
from simulation.point_mass import PointMassSimulation


def run_grid_convergence_test(resolutions: List[int] = None) -> Dict[str, Any]:
    """
    Run simulation over multiple grid resolutions to verify numerical convergence.
    """
    if resolutions is None:
        resolutions = [60, 100, 140, 180, 220]

    times = []
    fluxes = []
    effective_mags = []

    for res in resolutions:
        sim = PointMassSimulation(
            mass_solar=1e11,
            source_x=0.4,
            source_y=0.2,
            source_radius=0.15,
            resolution=res
        )
        res_data = sim.run()
        times.append(res_data["computation_time_seconds"])
        fluxes.append(float(np.sum(res_data["lensed_image"])))
        effective_mags.append(res_data["effective_magnification"])

    # Compute relative error compared to highest resolution
    ref_flux = fluxes[-1]
    rel_errors_pct = [abs(f - ref_flux) / ref_flux * 100.0 if ref_flux > 0 else 0.0 for f in fluxes]

    return {
        "resolutions": resolutions,
        "computation_times": times,
        "total_fluxes": fluxes,
        "effective_magnifications": effective_mags,
        "relative_errors_pct": rel_errors_pct
    }

