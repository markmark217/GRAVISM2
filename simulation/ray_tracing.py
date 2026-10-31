"""
Ray Tracing Simulation Engine
=============================

Core computational engine performing backward ray-tracing from observer image plane
to background source plane using Liouville's theorem (surface brightness conservation).
"""

from typing import Dict, Any, Tuple
import time
import numpy as np
from simulation.source_models import SourceModel, GaussianSource
from physics.magnification import compute_jacobian_and_magnification_grid, find_critical_curves_and_caustics


class RayTracingEngine:
    """
    Simulates gravitational lensing images, ray grids, and magnification maps.
    """

    def __init__(self, fov_arcsec: float = 6.0, resolution: int = 160):
        self.fov = float(fov_arcsec)
        self.resolution = int(resolution)
        self._setup_grid()

    def set_grid(self, fov_arcsec: float, resolution: int):
        self.fov = float(fov_arcsec)
        self.resolution = int(resolution)
        self._setup_grid()

    def _setup_grid(self):
        half = self.fov / 2.0
        x = np.linspace(-half, half, self.resolution)
        y = np.linspace(-half, half, self.resolution)
        self.theta_x, self.theta_y = np.meshgrid(x, y)

    def simulate(self, lens_profile, source_model: SourceModel,
                 compute_caustics: bool = True) -> Dict[str, Any]:
        """
        Run the ray-tracing simulation for the provided lens profile and source model.
        """
        t0 = time.perf_counter()

        # Deflection angles in image plane
        alpha_x, alpha_y = lens_profile.deflection(self.theta_x, self.theta_y)

        # Source coordinates via lens equation: beta = theta - alpha
        beta_x = self.theta_x - alpha_x
        beta_y = self.theta_y - alpha_y

        # Source brightness evaluated at source plane
        source_image = source_model.brightness(self.theta_x, self.theta_y)

        # Lensed image brightness via Liouville's theorem
        lensed_image = source_model.brightness(beta_x, beta_y)

        # Jacobian and Magnification Map
        jac_data = compute_jacobian_and_magnification_grid(
            beta_x, beta_y, self.theta_x, self.theta_y
        )

        curves = {"critical_curves": [], "caustics": []}
        if compute_caustics:
            curves = find_critical_curves_and_caustics(
                self.theta_x, self.theta_y, beta_x, beta_y, jac_data["det_a"]
            )

        elapsed = time.perf_counter() - t0

        # Calculate total unlensed flux vs total lensed flux
        flux_unlensed = float(np.sum(source_image))
        flux_lensed = float(np.sum(lensed_image))
        effective_magnification = (flux_lensed / flux_unlensed) if flux_unlensed > 0 else 1.0

        return {
            "theta_x": self.theta_x,
            "theta_y": self.theta_y,
            "beta_x": beta_x,
            "beta_y": beta_y,
            "source_image": source_image,
            "lensed_image": lensed_image,
            "magnification_map": jac_data["abs_magnification"],
            "signed_magnification": jac_data["magnification"],
            "convergence_map": jac_data["convergence"],
            "shear_map": jac_data["shear"],
            "critical_curves": curves["critical_curves"],
            "caustics": curves["caustics"],
            "computation_time_seconds": elapsed,
            "grid_resolution": self.resolution,
            "effective_magnification": effective_magnification,
            "fov_arcsec": self.fov
        }

