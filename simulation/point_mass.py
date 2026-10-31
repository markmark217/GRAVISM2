"""
Point Mass Lens Simulation Runner
=================================
"""

from typing import Dict, Any, List
import numpy as np
from physics.mass_profiles import PointMassProfile
from physics.lens_equation import solve_point_mass_images_2d
from physics.einstein_radius import calculate_einstein_radius_arcsec
from simulation.source_models import GaussianSource
from simulation.ray_tracing import RayTracingEngine


class PointMassSimulation:
    def __init__(self,
                 mass_solar: float = 1e11,
                 d_l_mpc: float = 1000.0,
                 d_s_mpc: float = 2000.0,
                 d_ls_mpc: float = 1000.0,
                 source_x: float = 0.5,
                 source_y: float = 0.3,
                 source_radius: float = 0.2,
                 lens_x: float = 0.0,
                 lens_y: float = 0.0,
                 resolution: int = 160):
        self.mass_solar = float(mass_solar)
        self.d_l_mpc = float(d_l_mpc)
        self.d_s_mpc = float(d_s_mpc)
        self.d_ls_mpc = float(d_ls_mpc)
        self.source_x = float(source_x)
        self.source_y = float(source_y)
        self.source_radius = float(source_radius)
        self.lens_x = float(lens_x)
        self.lens_y = float(lens_y)
        self.resolution = int(resolution)

    def run(self) -> Dict[str, Any]:
        from physics.constants import M_SUN
        mass_kg = self.mass_solar * M_SUN
        theta_e_arcsec = float(calculate_einstein_radius_arcsec(
            mass_kg, self.d_l_mpc, self.d_s_mpc, self.d_ls_mpc
        ))

        # Dynamic FOV based on theta_E and source position
        dist_src = np.hypot(self.source_x - self.lens_x, self.source_y - self.lens_y)
        fov = max(5.0, 3.5 * max(theta_e_arcsec, dist_src))

        # Analytical image positions
        images = solve_point_mass_images_2d(
            self.source_x, self.source_y, theta_e_arcsec, self.lens_x, self.lens_y
        )

        # Profile and Ray tracing
        lens_profile = PointMassProfile(theta_e_arcsec, self.lens_x, self.lens_y)
        source = GaussianSource(self.source_x, self.source_y, sigma=self.source_radius)
        engine = RayTracingEngine(fov_arcsec=fov, resolution=self.resolution)
        results = engine.simulate(lens_profile, source)

        results.update({
            "model_type": "point_mass",
            "theta_e_arcsec": theta_e_arcsec,
            "images": images,
            "mass_solar": self.mass_solar,
            "source_pos": (self.source_x, self.source_y),
            "lens_pos": (self.lens_x, self.lens_y)
        })
        return results

